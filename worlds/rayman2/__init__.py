import random
from typing import Type, ClassVar, TextIO, List

from BaseClasses import Tutorial, ItemClassification, Item, Region, Location, Entrance
from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World
from .Data import item_table, location_table, idMap, silverLumItemNames
from .Layout import levels, SubLevelInfo, LevelInfo
from .Options import create_option_groups, Rayman2Options


class Rayman2Item(Item):
    game: str = "Rayman 2"


class Rayman2Location(Location):
    game: str = "Rayman 2"


class Rayman2Web(WebWorld):
    option_groups = create_option_groups()
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide for setting up Rayman 2 with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Aeltumn"]
    )]


class Rayman2World(World):
    """
    Rayman 2 is a classic 3D platformer where Rayman sets out on an adventure to obtain four
    masks to defeat an army of Robo-Pirates attacking the Glade of Dreams.
    """

    game = "Rayman 2"
    web = Rayman2Web()
    topology_present = True

    item_name_to_id = {item.displayName: item.id for item in item_table}
    location_name_to_id = {loc.displayName: loc.id for loc in location_table}

    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = Rayman2Options
    options: Rayman2Options

    def __init__(self, multiworld, player):
        super(Rayman2World, self).__init__(multiworld, player)

        # Store variables with the level shuffle and lum gates
        self.levelSwaps = {}
        self.lumGates = {}

    def create_regions(self) -> None:
        # Start by creating the menu
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        # Go through all levels to create regions and items
        for baseLevelName, levelInfo in levels.items():
            lastRegion = menu
            for subLevelName, subLevelInfo in levelInfo.sublevels.items():
                # Create this level and connect it
                region = Region(subLevelName, self.player, self.multiworld)
                self.multiworld.regions.append(region)
                lastRegion.exits.append(Entrance(self.player, f"{subLevelName} Entrance", lastRegion))
                lastRegion = region

            # Connect the last sub-level back to the menu directly always (through the exit portal)
            if lastRegion.name != menu.name:
                lastRegion.connect(menu)

        # Go through all location and create them
        for data in location_table:
            region = self.multiworld.get_region(data.region, self.player)
            location = Rayman2Location(self.player, data.displayName, data.id, region)
            location.progression_type = data.progressionType
            region.locations.append(location)

            if data.needsSilver:
                location.access_rule = lambda state: state.has_any(silverLumItemNames, self.player)

    # Run room randomization when we need to connect everything up
    def connect_entrances(self) -> None:
        usedSubLevels = []
        wouldHaveSilverLum = False
        for baseLevelName, levelInfo in levels.items():
            for subLevelName, subLevelInfo in levelInfo.sublevels.items():
                # Determine what level to swap this level with already, but
                # create the connections later!
                subLevelOptions = []
                for _, otherLevelInfo in levels.items():
                    for otherSubLevelName, otherSubLevelInfo in otherLevelInfo.sublevels.items():
                        # Ignore sub levels that are already taken
                        if otherSubLevelName in usedSubLevels:
                            continue

                        # Ignore levels that need a silver lum when you wouldn't yet have one
                        # in the base game. This adds a bit of a buffer at the start before you
                        # need to obtain a silver lum.
                        # TODO This should be rule-based!
                        if otherSubLevelInfo.needsSilver and not wouldHaveSilverLum:
                            continue

                        # We need exit portals to always stay as the last sub-levels!
                        if subLevelInfo.hasExitPortal != otherSubLevelInfo.hasExitPortal:
                            continue

                        # Add this as a valid option
                        subLevelOptions.append(otherSubLevelName)

                choice = random.choice(subLevelOptions)
                print(f"Connecting {subLevelName} -> {choice}")
                self.levelSwaps[subLevelName] = choice
                self.multiworld.get_entrance(f"{subLevelName} Entrance", self.player).connect(
                    self.multiworld.get_region(choice, self.player))
                usedSubLevels.append(choice)

                # If this sub level has a lum gate we need to
                # define how high it should be based on how many
                # lums have been obtained thus far.
                if subLevelInfo.lumGate:
                    # TODO Determine the value the lum gates should have later!
                    self.lumGates[subLevelName] = 0

                # Mark down when we've reached a level where there would be a silver lum.
                if subLevelInfo.silverLum:
                    wouldHaveSilverLum = True

    # Create basic items
    def create_item(self, item: str,
                    classification: ItemClassification = ItemClassification.progression) -> Rayman2Item:
        return Rayman2Item(item, classification, self.item_name_to_id[item], self.player)

    # Fill the item pool based on the item table
    def create_items(self):
        itempool = []
        for item in item_table:
            itempool.append(self.create_item(item.displayName, item.classification))
        self.multiworld.itempool += itempool

    # Include level swaps and lum gate information in the slot data
    # sent to the game on connection
    def fill_slot_data(self):
        slot_data = {}
        slot_data["level_swaps"] = self.levelSwaps
        slot_data["lum_gates"] = self.lumGates
        slot_data["id_map"] = idMap
        return slot_data

    # Write slot data to the spoiler file for testing
    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\nRayman 2 slot information:\n")
        spoiler_handle.write(f"Level Swaps: {self.levelSwaps}\n")
        spoiler_handle.write(f"Lum Gates: {self.lumGates}\n")
        spoiler_handle.write(f"ID Map: {idMap}\n")
