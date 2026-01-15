import random
from typing import TextIO

from BaseClasses import Tutorial, ItemClassification, Item, Region, Location, Entrance
import entrance_rando
from worlds.AutoWorld import WebWorld, World
from .Data import item_table, location_table
from .Layout import Tech, Connection, ExtraLevelInfo, levels, extra_levels
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

    def applyAccessRequirement(self, accessible, tech, region):
        # Applies the relevant access requirement to an accessible object
        match tech:
                case Tech.PURPLE_SWING, Tech.BAYOU_DAMAGE_BOOST, Tech.PURPLE_SWING_OR_BACKWARDS_JUMP, Tech.PURPLE_SWING_OR_GLM:
                    accessible.access_rule = lambda state: state.has("Silver Lum", self.player) and state.can_reach_region(region, self.player)
                    return
                case Tech.ELIXIR_AND_PURPLE_SWING:
                    accessible.access_rule = lambda state: state.has("Silver Lum", self.player) and state.has("Elixir of Life", self.player) and state.can_reach_region(region, self.player)
                    return
                case _:
                    accessible.access_rule = lambda state: state.can_reach_region(region, self.player)
                    return

    def create_regions(self) -> None:
        # Start by creating the menu
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        # Go through all levels to create regions and items
        regionsById: dict[str, Region] = {}
        lumGate = -1
        for levelInfo in levels:
            lastRegion = menu
            lastLevelName = None
            lastLevelInfo = None
            for subLevelName, subLevelInfo in levelInfo.sublevels.items():
                # Create this level and connect it
                region = Region(subLevelName, self.player, self.multiworld)
                self.multiworld.regions.append(region)
                regionsById[subLevelName] = region

                # Add exit requirements to whether this region can be left!
                exit = lastRegion.create_exit(subLevelName)
                entrance = region.create_er_target(subLevelName)

                if lastLevelInfo is not None:
                    entrance.randomization_group = Connection.INTERNAL
                    exit.randomization_group = Connection.INTERNAL
                    self.applyAccessRequirement(exit, lastLevelInfo.exitRequirement, lastLevelName)
                else:
                    entrance.randomization_group = Connection.ENTRY_PORTAL
                    exit.randomization_group = Connection.ENTRY_PORTAL

                    # Determine the lum requirement to reach this portal
                    if levelInfo.lumGate:
                        lumGate += 1

                    # Determine the lum requirement based on when the last lum gate was
                    lumRequirement = 0
                    match lumGate:
                        case 0:
                            lumRequirement = self.options.first_mask_required.value
                        case 1:
                            lumRequirement = self.options.second_mask_required.value
                        case 2:
                            lumRequirement = self.options.third_mask_required.value
                        case 3:
                            lumRequirement = self.options.fourth_mask_required.value

                    entrance.access_rule = lambda state: (self.prog_items[self.player]["Lum"] + (5 * self.prog_items[self.player]["Super Lum"])) >= lumRequirement

                lastRegion = region
                lastLevelName = subLevelName
                lastLevelInfo = subLevelInfo

            # Connect the last sub-level back to the menu directly always (through the exit portal, not randomised)
            if lastRegion.name != menu.name:
                exit = lastRegion.connect(menu)
                exit.randomization_group = Connection.EXIT_PORTAL
                if lastLevelInfo is not None:
                    self.applyAccessRequirement(exit, lastLevelInfo.exitRequirement, lastLevelName)

        # Connect all the optional levels
        extraLevelsById: dict[str, ExtraLevelInfo] = {}
        for level in extra_levels:
            extraLevelsById[level.mapName] = level

        # Add the cave of bad dreams side-entrance
        cobd1 = extraLevelsById["vulca_10"]
        cobd1Region =Region(cobd1.mapName, self.player, self.multiworld)
        self.multiworld.regions.append(cobd1Region)
        cobd2 = extraLevelsById["vulca_20"]
        cobd2Region = Region(cobd2.mapName, self.player, self.multiworld)
        self.multiworld.regions.append(cobd2Region)
        marshes = regionsById["Ski_10"]
        cobd1Exit = marshes.create_exit(cobd1.mapName)
        cobd1Exit.access_rule = lambda state: state.has("Knowledge of the Cave of Bad Dreams", self.player)
        cobd1Entrance = cobd1Region.create_er_target(cobd1.mapName)
        cobd1Entrance.randomization_group = Connection.INTERNAL
        cobd1Exit.randomization_group = Connection.INTERNAL
        cobd2Exit = cobd1Region.create_exit(cobd2.mapName)
        cobd2Entrance = cobd2Region.create_er_target(cobd2.mapName)
        cobd2Entrance.randomization_group = Connection.INTERNAL
        cobd2Exit.randomization_group = Connection.INTERNAL
        cobd2Region.connect(menu).randomization_group = Connection.EXIT_PORTAL

        # Add the side temple which requires a purple swing to access
        sideTemple = extraLevelsById["plum_20"]
        sideTempleRegion = Region(sideTemple.mapName, self.player, self.multiworld)
        self.multiworld.regions.append(sideTempleRegion)
        mainSanctuary = regionsById["plum_00"]
        sideTempleExit = mainSanctuary.create_exit(sideTemple.mapName)
        sideTempleEntrance = sideTempleRegion.create_er_target(sideTemple.mapName)
        sideTempleEntrance.randomization_group = Connection.INTERNAL
        sideTempleExit.randomization_group = Connection.INTERNAL
        self.applyAccessRequirement(sideTempleExit, Tech.PURPLE_SWING, sideTemple.mapName)
        # We pretend the side temple is a dead end, exiting it in-game will send you
        # to wherever the stone and fire portal took you. Since we can't rando entrances
        # in-game and instead rando maps if we hooked this up there might be two maps
        # we expect to send you to when entering plum_00.

        # Go through all location and create them
        for data in location_table:
            region = self.multiworld.get_region(data.region, self.player)
            location = Rayman2Location(self.player, data.displayName, data.id, region)
            location.progression_type = data.progressionType
            
            # Add an access rule based on the tech type and this region being accessible!
            self.applyAccessRequirement(location, data.tech, data.region)
            
            # Add this location to this region
            region.locations.append(location)

    # Run room randomization when we need to connect everything up
    def connect_entrances(self) -> None:
        placement = entrance_rando.randomize_entrances(
            self,
            False, 
            {
                Connection.ENTRY_PORTAL: [Connection.ENTRY_PORTAL],
                Connection.INTERNAL: [Connection.INTERNAL],
                Connection.EXIT_PORTAL: [Connection.EXIT_PORTAL]
            }
        )
        
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
