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
        self.placedTransitions = {}
        self.generating = False

    def is_exit_reachable(self, exit: str, state: CollectionState) -> bool:
        """Returns whether the given connection is accessible."""
        if exit in self.placedTransitions:
            # The transition we are looking for got turned into this one, so
            # we need to check if you can reach the end of the level it turned into!
            target = self.placedTransitions[exit]
            first = target.split(" -> ", 1)[0]
            return state.can_reach_location(f"Finish {first}", self.player)
        return False

    def applyAccessRequirement(self, accessible, tech: Tech):
        """Applies the relevant access requirement to an accessible object."""
        match tech:
            case Tech.PURPLE_SWING | Tech.BAYOU_DAMAGE_BOOST | Tech.PURPLE_SWING_OR_BACKWARDS_JUMP | Tech.PURPLE_SWING_OR_GLM:
                accessible.access_rule = lambda state: self.generating or state.has("Silver Lum", self.player)
            case Tech.ELIXIR_AND_PURPLE_SWING:
                accessible.access_rule = lambda state: self.generating or (state.has("Silver Lum", self.player) and state.has("Elixir of Life", self.player))
            case Tech.HAS_REENTERED_FROM_THAT_ONE_SPECIFIC_EXIT:
                accessible.acccess_rule = lambda state: self.generating or self.is_exit_reachable("plum_10 -> plum_00", state)
            case Tech.NONE:
                return
            case _:
                raise KeyError(f"Invalid tech type {tech}")
            
    def create_level(
            self, 
            levelInfo: LevelInfo, 
            lastLevel: Region, 
            entryType: Connection = Connection.ENTRY_PORTAL,
            extraRule: Callable[[CollectionState], bool] = None,
    ) -> Region:
        """Creates a new level from a level info that can be entered from source."""
        if len(levelInfo.sublevels) == 0:
            return lastLevel

        first = True
        lastRegion: Region = lastLevel
        for subLevelName, subLevelInfo in levelInfo.sublevels.items():
            # Create this level and connect it
            region = Region(subLevelName, self.player, self.multiworld)
            self.multiworld.regions.append(region)

            # Connect this to either the previous region or the menu, only include the level info's
            # rules on the initial entrance into this level!
            if first:
                self.connect_level_entrance(lastRegion, region, levelInfo, entryType, extraRule)
            else:
                self.connect_internal(lastRegion, region)
            first = False

            # Connect every level to the menu so Archipelago doesn't get confused about that we're
            # always allowed to exit the levels at any time!
            region.connect(self.get_region("Menu")).randomization_group = Connection.NOT_RANDOM

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
            type: Connection = Connection.ENTRY_PORTAL,
            extraRule: Callable[[CollectionState], bool] = None,
        ):
        """Connects the menu to this region."""
        connection = f"{lastLevel.name} -> {region.name}"
        exit = lastLevel.create_exit(connection)

        # If this is the final level it cannot be randomised!
        if region.name == "Rhop_10" or not self.options.room_randomisation.value:
            exit.connect(region)
        else:
            # Mark the exit as being in the right randomization groups
            exit.randomization_group = type

            # Create an entrance randomization target for this region!
            entrance = region.create_er_target(connection)
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

            exit.access_rule = lambda state: self.generating or ((state.prog_items[self.player]["1000th Lum"] + 
                                              state.prog_items[self.player]["Lum"] + 
                                              (5 * state.prog_items[self.player]["Super Lum"])
                                            ) >= lumRequirement)
        elif levelInfo.requireAllMasks:
            # If this is a mask requiring level we add that as a requirement!
            exit.access_rule = lambda state: self.generating or (state.has("Water Mask", self.player) and \
                                        state.has("Earth Mask", self.player) and \
                                        state.has("Fire Mask", self.player) and \
                                        state.has("Air Mask", self.player))
            
        # Add the extra rule for this entrance
        if extraRule is not None:
            base = exit.access_rule
            exit.access_rule = lambda state: extraRule(state) and base(state)

    def connect_internal(
            self,
            lastRegion: Region,
            region: Region
        ):
        """Connects the given region to the previous one."""
        connection = f"{lastRegion.name} -> {region.name}"
        exit = lastRegion.create_exit(connection)
        exit.randomization_group = Connection.INTERNAL

        # Create an entrance only if room randomisation is enabled
        if self.options.room_randomisation.value:
            entrance = region.create_er_target(connection)
            entrance.randomization_group = Connection.INTERNAL
        else:
            exit.connect(region)

        # Whether this exit can be reached depends on finishing the previous region!
        if lastRegion.name != "Menu":
            exit.access_rule = lambda state: state.can_reach_location(f"Finish {lastRegion.name}",  self.player)

    def create_regions(self) -> None:
        # Start by creating the menu
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        # Go through all levels to create regions and items
        lastLevel = menu
        for levelInfo in levels:
            if lastLevel.name == "Menu":
                lastLevel = self.create_level(levelInfo, lastLevel)
            else:
                # If this is not the menu we require that you can finish the last level to unlock the next portal!
                boundLastLevel = lastLevel
                lastLevel = self.create_level(levelInfo, lastLevel, Connection.ENTRY_PORTAL, lambda state: state.can_reach_location(f"Finish {boundLastLevel.name}", self.player))
         
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

            self.create_level(extraLevelInfo, lastLevel, entryType, extraRule)

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

    # Run room randomization when we need to connect everything up
    def connect_entrances(self) -> None:
        # If we're in UT we don't re-randomize!
        is_ut = getattr(self.multiworld, "generation_is_fake", False)
        if is_ut:
            return

        def handlePlacement(_: entrance_rando.ERPlacementState, placed_exits: list[Entrance], placed_targets: list[Entrance]) -> bool:
            refresh = False
            for i in range(len(placed_exits)):
                original = placed_exits[i]
                placed = placed_targets[i]

                # Ignore exits we already know about!
                if original.name in self.placedTransitions:
                    continue
                
                # Store this connection now
                self.placedTransitions[original.name] = placed.name
                print(f"Locked in mapping from {original} to {placed}")

                # If the stone and fire side temple has become available we need to update
                # the access rule of the lums.
                if original.name == "plum_10 -> plum_00":
                    refresh = True
            return refresh

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
        
        # Go through the decided entrances and determine for each base game
        # sub level what level should we actually send them to.
        for exit, entrance in placement.pairings:
            # Entrance is the level to actually be played, where we want
            # to send the player, exit is where they would normally go.
            print(f"Pairing of {exit} to {entrance}")
            self.levelSwaps[exit] = entrance

    # Create basic items
    def create_item(self, item: str,
                    classification: ItemClassification = ItemClassification.progression) -> Rayman2Item:
        return Rayman2Item(item, classification, self.item_name_to_id[item], self.player)

    # Fill the item pool based on the item table
    def create_items(self):
        itempool = []
        for item in item_table:
            # If not on lumsanity, don't shuffle in the lums!
            if item.displayName == "Lum" and not self.options.lumsanity.value:
                continue
            itempool.append(self.create_item(item.displayName, item.classification))
        self.multiworld.itempool += itempool

    # Load level connections back from the slot
    def interpret_slot_data(self, slot_data: dict[str, Any]) -> None:
        entrances = {
            entrance.name: entrance
            for region in self.get_regions()
            for entrance in region.entrances
        }
        for source_exit, target_entrance in slot_data["pairings"]:
            entrances[source_exit].connected_region = entrances[target_entrance].parent_region

    # Include information the game needs in the slot data
    def fill_slot_data(self):
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
        }

    # Write slot data to the spoiler file for extra info
    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\nRayman 2 slot information:\n")
        spoiler_handle.write(f"Level Swaps: {self.levelSwaps}\n")
