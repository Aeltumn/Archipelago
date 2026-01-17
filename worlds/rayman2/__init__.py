import random
from typing import Any, Callable, TextIO

from BaseClasses import CollectionState, Tutorial, ItemClassification, Item, Region, Location, Entrance
import entrance_rando
from worlds.AutoWorld import WebWorld, World
from .Data import item_table, location_table
from .Layout import SubLevelInfo, Tech, Connection, LevelInfo, levels, extra_levels
from .Options import create_option_groups, Rayman2Options


class Rayman2Item(Item):
    game: str = "Rayman 2"


class Rayman2Location(Location):
    game: str = "Rayman 2"

class Rayman2Entrance(Entrance):
    openChecks: int
    isFinalLevel: bool

    def is_valid_source_transition(self, other, dead_end: bool, er_state: entrance_rando.ERPlacementState):
        """Adds additional restrictions to prevent invalid configurations."""
        # If we haven't placed checks yet, don't allow any entrances that
        # give access to zero checks!
        placedChecks = getattr(er_state, 'placedChecks', 0)
        if placedChecks == 0 and self.openChecks == 0:
            return False

        return super().is_valid_source_transition(other, dead_end, er_state)

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

    ut_can_gen_without_yaml = True

    def __init__(self, multiworld, player):
        super(Rayman2World, self).__init__(multiworld, player)

        # Initialize variables
        self.levelSwaps = {}
        self.pairings = {}
        self.thatOneSideTempleExitId = "Finish plum_10"
        self.generating = False

    def applyAccessRequirement(self, accessible, tech: Tech):
        """Applies the relevant access requirement to an accessible object."""
        match tech:
            case Tech.PURPLE_SWING | Tech.BAYOU_DAMAGE_BOOST | Tech.PURPLE_SWING_OR_BACKWARDS_JUMP | Tech.PURPLE_SWING_OR_GLM:
                accessible.access_rule = lambda state: self.generating or state.has("Silver Lum", self.player)
            case Tech.ELIXIR_AND_PURPLE_SWING:
                accessible.access_rule = lambda state: self.generating or (state.has("Silver Lum", self.player) and state.has("Elixir of Life", self.player))
            case Tech.HAS_REENTERED_FROM_THAT_ONE_SPECIFIC_EXIT:
                accessible.access_rule = lambda state: self.generating or state.has(self.thatOneSideTempleExitId, self.player)
            case Tech.NONE:
                return
            case _:
                raise KeyError(f"Invalid tech type {tech}")

    def create_level(
            self, 
            levelInfo: LevelInfo, 
            lastLevel: Region,
            isAtStartOfLevel: bool = False,
            entryType: Connection = Connection.ENTRY_PORTAL,
            extraRule: Callable[[CollectionState], bool] = None,
    ) -> Region:
        """Creates a new level from a level info that can be entered from source."""
        if len(levelInfo.sublevels) == 0:
            return lastLevel

        index = 0
        lastRegion: Region = lastLevel
        for subLevelName, subLevelInfo in levelInfo.sublevels.items():
            # Create this level and connect it
            index += 1
            isLast = index == len(levelInfo.sublevels)
            region = Region(subLevelName, self.player, self.multiworld)
            self.multiworld.regions.append(region)

            # Determine the amount of public checks in this level
            checks = subLevelInfo.checks.total()

            # Connect this to either the previous region or the menu, only include the level info's
            # rules on the initial entrance into this level!
            if index <= 1:
                self.connect_level_entrance(lastRegion, region, levelInfo, isLast, checks, entryType, extraRule, isAtStartOfLevel)
            else:
                self.connect_internal(lastRegion, region, isLast, checks)

            # Create an event for finishing this sub-region
            self.create_level_finish_event(region, subLevelInfo)

            # Update variables for next loop
            lastRegion = region
        return lastRegion
            
    def create_level_finish_event(self, region: Region, levelInfo: SubLevelInfo) -> Location:
        """Creates an event for finishing this level."""
        name = f"Finish {region.name}"
        event_location = Location(self.player, name, None, region)
        event_location.show_in_spoiler = True
        if levelInfo is not None:
            self.applyAccessRequirement(event_location, levelInfo.exitRequirement)
        event_item = Item(name, ItemClassification.progression, None, self.player)
        event_location.place_locked_item(event_item)
        region.locations.append(event_location)
        return event_location

    def connect_level_entrance(
            self, 
            lastLevel: Region, 
            region: Region, 
            levelInfo: LevelInfo,
            checks: int,
            isLast: bool,
            type: Connection = Connection.ENTRY_PORTAL,
            extraRule: Callable[[CollectionState], bool] = None,
            isAtStartOfLevel: bool = False,
        ):
        """Connects the menu to this region."""
        connection = f"{lastLevel.name} -> {region.name}"
        exit = lastLevel.create_exit(connection)

        # Mark down which exits are at the start of a level and don't require completing the level they are on!
        if isAtStartOfLevel:
            setattr(exit, 'isAtStartOfLevel', True)

        # If this is the final level it cannot be randomised!
        if region.name == "Rhop_10" or not self.options.room_randomisation.value:
            exit.connect(region)
            exit.randomization_group = Connection.NOT_RANDOM
        else:
            # Mark the exit as being in the right randomization groups
            exit.randomization_group = type

            # Create an entrance randomization target for this region!
            entrance = Rayman2Entrance(self.player, connection)
            entrance.openChecks = checks
            entrance.isFinalLevel = isLast
            entrance.connect(region)
            entrance.randomization_group = type

        # Determine the lum requirement to reach this portal
        if levelInfo.lumGate is not None:
            # Determine the lum requirement based on when the last lum gate was
            lumRequirement = 0
            match levelInfo.lumGate:
                case 0:
                    lumRequirement = self.options.first_gate_required.value
                case 1:
                    lumRequirement = self.options.second_gate_required.value
                case 2:
                    lumRequirement = self.options.third_gate_required.value
                case 3:
                    lumRequirement = self.options.fourth_gate_required.value
                case 4:
                    lumRequirement = self.options.walk_of_life_required.value
                case 5:
                    lumRequirement = self.options.walk_of_power_required.value

            base = exit.access_rule
            exit.access_rule = lambda state, base=base: self.generating or ((state.prog_items[self.player]["1000th Lum"] + 
                                              state.prog_items[self.player]["Lum"] + 
                                              (5 * state.prog_items[self.player]["Super Lum"])
                                            ) >= lumRequirement) and base(state)
        
        if levelInfo.requireAllMasks:
            # If this is a mask requiring level we add that as a requirement!
            base = exit.access_rule
            exit.access_rule = lambda state, base=base: self.generating or (state.has("Water Mask", self.player) and \
                                        state.has("Earth Mask", self.player) and \
                                        state.has("Fire Mask", self.player) and \
                                        state.has("Air Mask", self.player)) and \
                                        base(state)
            
        # Add the extra rule for this entrance if one is given.
        if extraRule is not None:
            base = exit.access_rule
            exit.access_rule = lambda state, base=base, extraRule=extraRule: extraRule(state) and base(state)

    def connect_internal(
            self,
            lastRegion: Region,
            region: Region,
            checks: int,
            isLast: bool,
        ):
        """Connects the given region to the previous one."""
        connection = f"{lastRegion.name} -> {region.name}"
        exit = lastRegion.create_exit(connection)

        # Create an entrance only if room randomisation is enabled
        if self.options.room_randomisation.value:
            entrance = Rayman2Entrance(self.player, connection)
            entrance.openChecks = checks
            entrance.isFinalLevel = isLast
            entrance.connect(region)
            entrance.randomization_group = Connection.INTERNAL
            exit.randomization_group = Connection.INTERNAL
        else:
            exit.connect(region)
            exit.randomization_group = Connection.NOT_RANDOM

    def create_regions(self) -> None:
        """Creates all regions available in the game."""
        # Start by creating the menu
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        # Go through all levels to create regions and items
        lastLevel = menu
        for levelInfo in levels:
            lastLevel = self.create_level(levelInfo, lastLevel)
         
        # Go through the extra levels and create them seperately
        for extraLevelInfo in extra_levels:
            lastLevel: Region = None
            extraRule: Callable[[CollectionState], bool] = None
            entryType: Connection = Connection.ENTRY_PORTAL

            # We consider the ability to enter some of these levels from the hall of doors as a convenience
            # feature the existance of which we'll omit for Archipelago. It should not think the player can
            # access any of these until their corresponding source level is reached.
            match extraLevelInfo.displayName:
                case "The Fairly Glade #2 - Revisit":
                    lastLevel = self.get_region("cask_10")
                    entryType = Connection.INTERNAL
                case "The Sanctuary of Stone and Fire - Side Temple":
                    lastLevel = self.get_region("plum_00")
                    entryType = Connection.INTERNAL
                case "The Cave of Bad Dreams":
                    lastLevel = self.get_region("Ski_10")
                    extraRule = lambda state: self.generating or state.has("Knowledge of the Cave of Bad Dreams", self.player)
                case "The Walk of Life":
                    lastLevel = self.get_region("chase_10")
                case "The Walk of Power":
                    lastLevel = self.get_region("earth_10")
                case "The Crow's Nest":
                    # The Crow's Nest is the only level to connect only to
                    # the Hall of Doors (aside from the first)!
                    lastLevel = menu
                case _:
                    raise KeyError(f"Unknown extra level {extraLevelInfo.displayName}")

            self.create_level(extraLevelInfo, lastLevel, True, entryType, extraRule)

        # Go through all location and create them
        for data in location_table:
            # If not on lumsanity, don't shuffle in the lums!
            if data.itemName == "Lum" and not self.options.lumsanity.value:
                continue

            region = self.multiworld.get_region(data.region, self.player)
            location = Rayman2Location(self.player, data.displayName, data.id, region)
            location.progression_type = data.progressionType
            
            # Add an access rule based on the tech type and this region being accessible!
            self.applyAccessRequirement(location, data.tech)
            
            # Add this location to this region
            region.locations.append(location)

        # Set the victory condition
        match self.options.end_goal.value:
            case 1:
                self.multiworld.completion_condition[self.player] = lambda state: state.has("Finish Rhop_10", self.player)
            case 2:
                self.multiworld.completion_condition[self.player] = lambda state: state.has("Finish vulca_20", self.player)
            case 3:
                if self.options.lumsanity.value:
                    self.multiworld.completion_condition[self.player] = lambda state: (
                        state.has("Finish Rhop_10", self.player) and
                            (state.prog_items[self.player]["1000th Lum"] + state.prog_items[self.player]["Lum"] + (5 * state.prog_items[self.player]["Super Lum"])) >= 1000 and
                            state.prog_items[self.player]["Cage"] >= 80
                    )
                else:
                    self.multiworld.completion_condition[self.player] = lambda state: (
                        state.has("Finish Rhop_10", self.player) and
                            # There's 58 super lums that can be collected!
                            state.prog_items[self.player]["Super Lum"] >= 58 and
                            state.prog_items[self.player]["Cage"] >= 80
                    )

    def connect_entrances(self) -> None:
        """Connect entrances of any disconnected regions in room randomisation mode."""
        # If we're in UT we don't re-randomize!
        is_ut = getattr(self.multiworld, "generation_is_fake", False)
        if not is_ut:
            def handlePlacement(state: entrance_rando.ERPlacementState, placed_exits: list[Entrance], placed_targets: list[Entrance]) -> bool:
                # Update the state with the latest selection, store it into the placement state object
                lastIndex = len(placed_targets) - 1
                lastPlacement = placed_targets[lastIndex]
                placedChecks = getattr(state, 'placedChecks', 0)
                placedChecks += lastPlacement.openChecks
                setattr(state, 'placedChecks', placedChecks)

                # Detect when we set the transition that lets you leave the side temple
                # and determine which level needs to be completed to use that door. Then
                # we can safely set that you require Finish X to get those lums.
                if placed_exits[lastIndex].name == "plum_10 -> plum_00":
                    first = placed_targets[lastIndex].split(" -> ", 1)[0]
                    self.thatOneSideTempleExitId = f"Finish {first}"
                    return True
                return False
            
            # Perform general entrance randomisation to build the map
            self.generating = True
            placement = entrance_rando.randomize_entrances(
                self,
                False, 
                {
                    Connection.ENTRY_PORTAL: [Connection.ENTRY_PORTAL],
                    Connection.INTERNAL: [Connection.INTERNAL]
                },
                on_connect=handlePlacement,
            )
            self.generating = False
            self.pairings = placement.pairings

            # Parse the pairings into the format the game needs
            for exit, entrance in self.pairings:
                # Entrance is the level to actually be played, where we want
                # to send the player, exit is where they would normally go.
                former = exit.split(" -> ", 1)[0]
                latter = entrance.split(" -> ", 1)[1]
                self.levelSwaps[former] = latter

        # Go through all decided levels and set access requirements on the exits properly to
        # require finishing the level the exit is in.
        entrances_by_name = {
            entrance.name: entrance
            for region in self.get_regions()
            for entrance in region.entrances
        }

        for exit, entrance in self.pairings:
            # The determine the original exit and then what it got shuffled into
            source_exit = entrances_by_name[exit]
            source_region = source_exit.parent_region

            # Capture variables for lambda then update it
            region_name = source_region.name
            if region_name == "Menu":
                continue

            base_rule = source_exit.access_rule
            source_exit.access_rule = lambda state, region_name=region_name,  base_rule=base_rule: base_rule(state) and state.has(f"Finish {region_name}", self.player)
            print(f"Entering {source_exit.connected_region} requires finishing {region_name}")

    def create_item(self, item: str,
                    classification: ItemClassification = ItemClassification.progression) -> Rayman2Item:
        """Creates a new Rayman 2 item using the item id table."""
        return Rayman2Item(item, classification, self.item_name_to_id[item], self.player)

    def create_items(self):
        """Creates all items based on the item table."""
        itempool = []
        for item in item_table:
            # If not on lumsanity, don't shuffle in the lums!
            if item.displayName == "Lum" and not self.options.lumsanity.value:
                continue
            itempool.append(self.create_item(item.displayName, item.classification))
        self.multiworld.itempool += itempool

    def interpret_slot_data(self, slot_data: dict[str, Any]) -> None:
        """Hook method used by Universal Tracker to load data from slot data back into Python so entrance randomisation is consistent."""
        self.thatOneSideTempleExitId = slot_data["side_temple_id"]

        entrances = {
            entrance.name: entrance
            for region in self.get_regions()
            for entrance in region.entrances
        }
        for source_exit, target_entrance in slot_data["pairings"]:
            entrances[source_exit].connected_region = entrances[target_entrance].parent_region

    def fill_slot_data(self):
        """Includes all information needed by the game into the slot data."""
        return {
            "level_swaps": self.levelSwaps,
            "pairings": self.pairings,
            "lum_gates": [
                self.options.first_gate_required.value,
                self.options.second_gate_required.value,
                self.options.third_gate_required.value,
                self.options.fourth_gate_required.value,
                self.options.walk_of_life_required.value,
                self.options.walk_of_power_required.value
            ],
            "death_link": self.options.death_link.value,
            "end_goal": self.options.end_goal.value,
            "room_randomisation": self.options.room_randomisation.value,
            "lumsanity": self.options.lumsanity.value,
            "side_temple_id": self.thatOneSideTempleExitId,
        }

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        """Includes decided level swaps in the spoiler file for debugging."""
        spoiler_handle.write(f"\nRayman 2 slot information:\n")
        spoiler_handle.write(f"Level Swaps: {self.levelSwaps}\n")
