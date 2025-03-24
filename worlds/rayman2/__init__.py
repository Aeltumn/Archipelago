import random
from typing import Type, ClassVar, TextIO

from BaseClasses import Tutorial, ItemClassification, Item, Region, LocationProgressType, Location
from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World
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
    topology_present = False

    item_name_to_id = {}
    location_name_to_id = {}

    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = Rayman2Options
    options: Rayman2Options

    def __init__(self, multiworld, player):
        super(Rayman2World, self).__init__(multiworld, player)

        # Initialize initial values
        self.base_id = 1651615

        # Store variables with the level shuffle and lum gates
        self.levelSwaps = {}
        self.lumGates = {}
        self.idMap = {}
        self.item_pool = []
        self.silverLumItemNames = []

    def create_regions(self) -> None:
        # Go through all levels in the level layout and create item/location objects,
        # every location is an item and every item is a location in Rayman 2.

        # This is because the game engine has a set id for every single item and all
        # items are tracked individually as completion, so we want to properly track
        # which specific cage or super lum was picked up. For now we use the internal
        # engine names for them all so they are easily distinguished in the game which
        # can be changed later.

        # Start by creating the menu
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        usedSubLevels = []
        lumTally = 0
        silverLumTally = 0
        for vanillaLevelName, vanillaLevelInfo in levels.items():
            lastRegion = menu
            for vanillaSubLevel, _ in vanillaLevelInfo.sublevels.items():
                # Determine another level to swap this one with
                subLevelOptions = []
                for _, otherLevelInfo in levels.items():
                    index = 0
                    for otherSubLevelName, otherSubLevelInfo in otherLevelInfo.sublevels.items():
                        index += 1

                        # Ignore sub levels that are already taken
                        if otherSubLevelName in usedSubLevels:
                            continue

                        # Ignore levels that need a silver lum when none are acquired
                        if otherSubLevelInfo.needsSilver and silverLumTally == 0:
                            continue

                        # Add this as a valid option
                        subLevelOptions.append([otherLevelInfo, otherSubLevelName, otherSubLevelInfo, index])

                # Pick the level to place here and store it
                tuple = random.choice(subLevelOptions)
                levelInfo: LevelInfo = tuple[0]
                subLevelName: str = tuple[1]
                subLevelInfo: SubLevelInfo = tuple[2]
                subLevelIndex: int = tuple[3]
                levelName = f"{levelInfo.displayName} {subLevelIndex}"
                usedSubLevels.append(subLevelName)
                self.levelSwaps[vanillaSubLevel] = subLevelName

                # TODO Add access rules for masks to enter the Pirate Ship

                # Create this level and connect it
                region = Region(subLevelName, self.player, self.multiworld)
                self.multiworld.regions.append(region)
                lastRegion.connect(region)
                lastRegion = region

                # If this sub level has a lum gate we need to
                # define how high it should be based on how many
                # lums have been obtained thus far.
                if subLevelInfo.lumGate:
                    # TODO Determine the value the lum gate should have
                    self.lumGates[subLevelName] = 0

                # Update the lum tally based on the regular lums available here
                lumTally += subLevelInfo.regularLums

                # Add access requirements to any levels that need silver lums
                needsSilver = subLevelInfo.needsSilver

                # Create an item for the silver lum
                if subLevelInfo.silverLum:
                    silverLumTally += 1
                    self.create(region, f"{subLevelName}_SilverLum", f"{levelName} - Silver Lum", ItemClassification.progression,
                                LocationProgressType.PRIORITY, needsSilver)

                # Create checks for all super lums
                index = 1
                for superLum in subLevelInfo.superLums:
                    self.create(region, superLum, f"{levelName} - 5 Lum #{index}", ItemClassification.filler, LocationProgressType.DEFAULT, needsSilver)
                    index += 1

                # Create checks for all cages
                index = 1
                for cage, lumsInside in subLevelInfo.cages.items():
                    self.create(region, cage, f"{levelName} - Cage #{index}", ItemClassification.useful, LocationProgressType.PRIORITY, needsSilver)
                    index += 1
                    lumTally += lumsInside
                    # TODO Update the lum tally based on which cage gets swapped in as it may contain
                    # a different amount!

                # Create checks for all special checks
                for (specialItem, displayName) in subLevelInfo.special.items():
                    self.create(region, specialItem, f"{levelName} - {displayName}", ItemClassification.progression, LocationProgressType.PRIORITY, needsSilver)

            # Connect the last sub-level back to the menu
            if lastRegion.name != menu.name:
                lastRegion.connect(menu)

            # TODO Process the extra level

    def create_item(self, item: str,
                    classification: ItemClassification = ItemClassification.progression) -> Rayman2Item:
        return Rayman2Item(item, classification, self.item_name_to_id[item], self.player)

    def create_items(self):
        self.multiworld.itempool += self.item_pool

    # Creates items and locations for every input
    def create(self, region, internalName, name, classification: ItemClassification, progression: LocationProgressType, needsSilver: bool = False):
        id = self.claim_id()

        # Add the item to the mappings
        self.item_name_to_id[name] = id
        self.item_id_to_name[id] = name
        self.location_name_to_id[name] = id
        self.location_id_to_name[id] = name

        # Add the item to the item pool
        self.item_pool.append(self.create_item(name, classification))

        # Add the item to the region
        location = Rayman2Location(self.player, name, id, region)
        location.progression_type = progression
        region.locations.append(location)

        # Add a requirement to obtain at least one silver lum from the options
        if "Silver Lum" in name:
            self.silverLumItemNames.append(name)
        if needsSilver:
            location.access_rule = lambda state: state.has_any(self.silverLumItemNames, self.player)

        # Note down in the id map that this item exists
        self.idMap[id] = internalName

    # Claim a new id for an item and location
    def claim_id(self):
        result = self.base_id
        self.base_id = result + 1
        return result

    # Include level swaps and lum gate information in the slot data
    # sent to the game on connection
    def fill_slot_data(self):
        slot_data = {}
        slot_data["level_swaps"] = self.levelSwaps
        slot_data["lum_gates"] = self.lumGates
        slot_data["id_map"] = self.idMap
        return slot_data

    # Write slot data to the spoiler file for testing
    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\nRayman 2 slot information:\n")
        spoiler_handle.write(f"Level Swaps: {self.levelSwaps}\n")
        spoiler_handle.write(f"Lum Gates: {self.lumGates}\n")
        spoiler_handle.write(f"ID Map: {self.idMap}\n")
