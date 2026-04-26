from typing import Any, Callable, TextIO, Tuple

from BaseClasses import CollectionState, Tutorial, ItemClassification, Item, Region, Location, Entrance
from worlds.AutoWorld import WebWorld, World
from .Data import item_table, location_table
from .Generator import GeneratorState
from .Layout import SubLevelInfo, Tech, LevelInfo, levels, extra_levels
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
        self.levelSwaps = {}
        self.pairings = {}

    def applyAccessRequirement(self, accessible, tech: Tech):
        """Applies the relevant access requirement to an accessible object."""
        if tech != Tech.NONE:
            accessible.access_rule = lambda state: self.has_tech(state, tech)

    def create_level(self, sublevels: dict[str, SubLevelInfo]) -> Tuple[Region | None, Region | None]:
        """Creates a new level from a level info that can be entered from source."""
        if len(sublevels) == 0:
            return [None, None]

        firstRegion: Region | None = None
        lastRegion: Region | None = None
        for subLevelName, subLevelInfo in sublevels.items():
            # Create this level and connect it
            region = Region(subLevelName, self.player, self.multiworld)
            self.multiworld.regions.append(region)

            if lastRegion is not None:
                # If this is not the first level of this world create a connection between
                self.connect_internal(lastRegion, region)

            # Create an event for finishing this sub-region
            self.create_level_finish_event(region, subLevelInfo)

            # If we're not in room randomisation mode we create an event for finishing the side temple
            # immediately as we place the rooms!
            if not self.options.room_randomisation and region.name == "plum_10":
                event = self.create_event(region, "Finish Side Temple")
                self.applyAccessRequirement(event, subLevelInfo.exitRequirement)

            # Store the first and last regions
            if firstRegion is None:
                firstRegion = region
            lastRegion = region
        return [firstRegion, lastRegion]
    
    def create_mapmonde_portal_event(self, region: Region, portals: int) -> Location:
        """Creates an event for generating a portal in the Hall of Doors."""
        event = self.create_event(region, f"Create Portal #{portals + 1}", "Create Portal")
        event.access_rule = lambda state: state.has(f"Finish {region.name}", self.player)
        return event

    def create_level_finish_event(self, region: Region, levelInfo: SubLevelInfo) -> Location:
        """Creates an event for finishing this level."""
        event = self.create_event(region, f"Finish {region.name}")
        if levelInfo is not None:
            self.applyAccessRequirement(event, levelInfo.exitRequirement)
        return event
    
    def create_event(self, region: Region, location_name: str, item_name: str = None) -> Location:
        """Creates a new generic event in the given region that requires finishing the given level."""
        if item_name is None:
            item_name = location_name
        event_location = Location(self.player, location_name, None, region)
        event_location.show_in_spoiler = True
        event_item = Item(item_name, ItemClassification.progression, None, self.player)
        event_location.place_locked_item(event_item)
        region.locations.append(event_location)
        return event_location
    
    def create_entrance_portal(self, source: Region, name: str, portals: int = 0, lum_gate: int | None = None, require_all_masks: bool = False, extra_rule: Callable[[CollectionState], bool] = None) -> Entrance:
        """Creates a new portal on the source which requires unlocking portals and possibly lum gates or masks but can be accessed itself without any requirements."""
        portal = source.create_exit(name)

        # Require the minimum amount of portals to be made previously so this one is reachable
        if portals > 0:
            portal.access_rule = lambda state: state.prog_items[self.player]["Create Portal"] >= portals

        # Determine the lum requirement to reach this portal
        if lum_gate is not None:
            # Determine the lum requirement based on when the last lum gate was
            lumRequirement = 0
            match lum_gate:
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

            base = portal.access_rule
            portal.access_rule = lambda state, base=base: self.get_lums(state) >= lumRequirement and base(state)
        
        if require_all_masks:
            # If this is a mask requiring level we add that as a requirement!
            base = portal.access_rule
            portal.access_rule = lambda state, base=base: (state.has("Water Mask", self.player) and \
                                        state.has("Earth Mask", self.player) and \
                                        state.has("Fire Mask", self.player) and \
                                        state.has("Air Mask", self.player)) and \
                                        base(state)
            
        # Add the extra rule for this portal if one is given.
        if extra_rule is not None:
            base = portal.access_rule
            portal.access_rule = lambda state, base=base, extra_rule=extra_rule: extra_rule(state) and base(state)

        return portal

    def connect_internal(self, lastRegion: Region, region: Region):
        """Connects the given region to the previous one."""
        # Create an exit on the region that can be used when you finish that region
        connection = f"{lastRegion.name} -> {region.name}"
        exit = lastRegion.create_exit(connection)
        exit.access_rule = lambda state: state.has(f"Finish {lastRegion.name}", self.player)

        # If not in room randomisation, connect this directly to the last zone
        if not self.options.room_randomisation.value:
            exit.connect(region)

    def has_tech(self, state: CollectionState, tech: Tech) -> bool:
        """Returns whether the given state has the items to complete the given tech."""
        match tech:
            case Tech.PURPLE_SWING | Tech.BAYOU_DAMAGE_BOOST | Tech.PURPLE_SWING_OR_BACKWARDS_JUMP | Tech.PURPLE_SWING_OR_GLM:
                return state.has("Silver Lum", self.player)
            case Tech.ELIXIR_AND_PURPLE_SWING:
                return state.has("Silver Lum", self.player) and state.has("Elixir of Life", self.player)
            case Tech.HAS_REENTERED_FROM_THAT_ONE_SPECIFIC_EXIT:
                return state.has("Finish Side Temple", self.player)
            case Tech.NONE:
                return True
            case _:
                raise KeyError(f"Invalid tech type {tech}")

    def get_lums(self, state: CollectionState) -> int:
        """Returns the amount of lums currently within state. Accounts for accessible lums in non-lumsanity."""
        if self.options.lumsanity.value:
            return state.prog_items[self.player]["Lum"] + (5 * state.prog_items[self.player]["Super Lum"])
        else:
            # Start with all super lums you have
            lumCount = (5 * state.prog_items[self.player]["Super Lum"])

            # Crawl through all available levels
            allLevels: list[LevelInfo] = []
            allLevels += levels
            allLevels += extra_levels
            for levelInfo in allLevels:
                for subLevelName, subLevelInfo in levelInfo.sublevels.items():
                    # If this region is reachable count all lums in the region, also check
                    # if they have the necessary tech to get the ones behind a requirement
                    if state.can_reach_region(subLevelName, self.player):
                        lumCount += len(subLevelInfo.checks.regularLums)

                        for tech, checks in subLevelInfo.behindRequirements.items():
                            if self.has_tech(state, tech):
                                lumCount += len(checks.regularLums)
            return lumCount

    def create_regions(self) -> None:
        """Creates all regions available in the game."""
        # Start by creating the menu
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        # Go through all levels to create regions and items
        portal = 0
        for levelInfo in levels:
            firstRegion, lastRegion = self.create_level(levelInfo.sublevels)
            if firstRegion is None or lastRegion is None:
                continue

            # Finishing the last level of each standard world creates a hall of doors portal!
            self.create_mapmonde_portal_event(lastRegion, portal)

            # Create a portal for each level on the hall of doors
            mapmonde_exit = self.create_entrance_portal(menu, f"Portal #{portal + 1}", portal, levelInfo.lumGate, levelInfo.requireAllMasks)
            portal += 1

            # Connect the portal to the level if not randomising or for the first/last levels
            if not self.options.room_randomisation.value or levelInfo.displayName == "The Woods of Light" or levelInfo.displayName == "The Crow's Nest":
                mapmonde_exit.connect(firstRegion)
         
        # Go through the extra levels and create them separately
        for extraLevelInfo in extra_levels:
            last_level: Region = None
            extra_rule: Callable[[CollectionState], bool] = None
            match extraLevelInfo.displayName:
                case "The Fairly Glade #2 - Revisit":
                    last_level = self.get_region("cask_10")
                case "The Sanctuary of Stone and Fire - Side Temple":
                    last_level = self.get_region("plum_00")
                case "The Cave of Bad Dreams":
                    last_level = self.get_region("Ski_10")
                    extra_rule = lambda state: state.has("Knowledge of the Cave of Bad Dreams", self.player)
                case "The Walk of Life":
                    last_level = self.get_region("chase_10")
                case "The Walk of Power":
                    last_level = self.get_region("earth_10")
                case _:
                    raise KeyError(f"Unknown extra level {extraLevelInfo.displayName}")

            # Create this level itself
            firstRegion, _ = self.create_level(extraLevelInfo.sublevels)
            if firstRegion is None:
                continue

            # Create an entrance in the source level
            level_exit = self.create_entrance_portal(last_level, f"Portal to {firstRegion.name}", lum_gate=extraLevelInfo.lumGate, require_all_masks=extraLevelInfo.requireAllMasks, extra_rule=extra_rule)

            # If room randomisation is off, connect the portal to this side-level!
            if not self.options.room_randomisation.value:
                level_exit.connect(firstRegion)

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
                self.multiworld.completion_condition[self.player] = lambda state: (
                        state.has("Finish Rhop_10", self.player) and
                        self.get_lums(state) >= 1000 and
                        state.prog_items[self.player]["Cage"] >= 80
                )

    def connect_entrances(self) -> None:
        """Connect entrances of any disconnected regions in room randomisation mode."""
        # If we're in UT we don't re-randomize!
        if getattr(self.multiworld, "generation_is_fake", False):
            return

        # If we're not in room randomisation mode, don't do anything!
        if not self.options.room_randomisation.value:
            return

        # Determine all entrances to randomise
        entrances = {
            entrance.name: entrance
            for region in self.get_regions()
            for entrance in region.entrances
        }

        # Run the custom generator
        generator = GeneratorState()
        generator.lumsanity = self.options.lumsanity.value
        generator.assemble_initial_levels(self.options)
        generator.generate(entrances)

        # Hook up all the regions based on the generator
        for source_exit, target_entrance in generator.pairings:
            entrances[source_exit].connected_region = entrances[target_entrance].parent_region
        self.pairings = generator.pairings

        # Parse the pairings into the format the game needs
        for exit, entrance in self.pairings:
            if exit.startswith("Portal #"):
                # This is a connection from a mapmonde portal.
                match exit:
                    case "Portal #1":
                        first = "learn_10"
                    case "Portal #2":
                        first = "learn_30"
                    case "Portal #3":
                        first = "ski_10"
                    case "Portal #4":
                        first = "chase_10"
                    case "Portal #5":
                        first = "water_10"
                    case "Portal #6":
                        first = "rodeo_10"
                    case "Portal #7":
                        first = "glob_10"
                    case "Portal #8":
                        first = "whale_00"
                    case "Portal #9":
                        first = "plum_00"
                    case "Portal #10":
                        first = "bast_10"
                    case "Portal #11":
                        first = "nave_10"
                    case "Portal #12":
                        first = "seat_10"
                    case "Portal #13":
                        first = "earth_10"
                    case "Portal #14":
                        first = "helic_10"
                    case "Portal #15":
                        first = "morb_00"
                    case "Portal #16":
                        first = "learn_40"
                    case "Portal #17":
                        first = "boat01"
                    case _:
                        raise KeyError(f"Invalid name {exit}")
            elif exit.startswith("Portal to "):
                # If it's a portal into a sub-region we map that region.
                first = exit[10:]
            else:
                # Otherwise take the source level of the transition.
                first = exit.split(" -> ", 1)[1]

            if entrance.startswith("Portal into "):
                second = entrance[12:]
            else:
                second = entrance.split(" -> ", 1)[1]

            # Learn 32 is our name for the EEC loading zone, not yet recognised by the mod so we
            # just make it learn 31 for now.
            if first == "Learn_32":
                first = "learn_31"
            if second == "Learn_32":
                second = "learn_31"

            self.levelSwaps[first] = second

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
        }

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        """Includes decided level swaps in the spoiler file for debugging."""
        spoiler_handle.write(f"\nRayman 2 slot information:\n")
        spoiler_handle.write(f"Level Swaps: {self.levelSwaps}\n")
