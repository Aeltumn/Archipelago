import random
from typing import TextIO

from BaseClasses import Tutorial, ItemClassification, Item, Region, Location, Entrance
import entrance_rando
from worlds.AutoWorld import WebWorld, World
from .Data import item_table, location_table
from .Layout import Tech, levels
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

    options_dataclass = Rayman2Options
    options: Rayman2Options

    def __init__(self, multiworld, player):
        super(Rayman2World, self).__init__(multiworld, player)

        # Store variables with the level shuffle
        self.levelSwaps = {}

    def applyAccessRequirement(self, accessible, tech):
        # Applies the relevant access requirement to an accessible object
        match tech:
                case Tech.PURPLE_SWING, Tech.BAYOU_DAMAGE_BOOST, Tech.PURPLE_SWING_OR_BACKWARDS_JUMP:
                    accessible.access_rule = lambda state: state.has("Silver Lum", self.player)
                    return
                case Tech.EARLY_ECHOING_CAVES_OR_REVISIT:
                    accessible.access_rule = lambda state: state.can_reach_region("Cask_10", self.player)
                    return
                case _:
                    return

    def create_regions(self) -> None:
        # Start by creating the menu
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        # Go through all levels to create regions and items
        for levelInfo in levels:
            lastRegion = menu
            lastLevelInfo = None
            for subLevelName, subLevelInfo in levelInfo.sublevels.items():
                # Create this level and connect it
                region = Region(subLevelName, self.player, self.multiworld)
                self.multiworld.regions.append(region)

                # Add exit requirements to whether this region can be left!
                exit = lastRegion.create_exit(subLevelName)
                if lastLevelInfo is not None:
                    self.applyAccessRequirement(exit, lastLevelInfo.exitRequirement)

                region.create_er_target(subLevelName)
                lastRegion = region
                lastLevelInfo = subLevelInfo

            # Connect the last sub-level back to the menu directly always (through the exit portal, not randomised)
            if lastRegion.name != menu.name:
                exit = lastRegion.connect(menu)
                if lastLevelInfo is not None:
                    self.applyAccessRequirement(exit, lastLevelInfo.exitRequirement)

        # Go through all location and create them
        for data in location_table:
            region = self.multiworld.get_region(data.region, self.player)
            location = Rayman2Location(self.player, data.displayName, data.id, region)
            location.progression_type = data.progressionType
            
            # Add an access rule based on the tech type!
            self.applyAccessRequirement(location, data.tech)
            
            region.locations.append(location)

    # Run room randomization when we need to connect everything up
    def connect_entrances(self) -> None:
        placement = entrance_rando.randomize_entrances(self, False, {0: [0]})
        
        # Go through the decided entrances and determine for each base game
        # sub level what level should we actually send them to.
        for exit, entrance in placement.pairings:
            # Entrance is the level to actually be played, where we want
            # to send the player, exit is where they would normally go.
            self.levelSwaps[exit] = entrance

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

    # Include information the game needs in the slot data
    def fill_slot_data(self):        
        slot_data = {}
        slot_data["level_swaps"] = self.levelSwaps
        slot_data["lum_gates"] = [
            self.options.first_mask_required.value,
            self.options.second_mask_required.value,
            self.options.third_mask_required.value,
            self.options.fourth_mask_required.value,
            self.options.walk_of_life_required.value,
            self.options.walk_of_power_required.value
        ]
        slot_data["death_link"] = self.options.death_link.value
        slot_data["end_goal"] = self.options.end_goal.value
        return slot_data

    # Write slot data to the spoiler file for extra info
    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\nRayman 2 slot information:\n")
        spoiler_handle.write(f"Level Swaps: {self.levelSwaps}\n")
