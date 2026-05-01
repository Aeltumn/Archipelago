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

    def __init__(self, multiworld, player):
        super(Rayman2World, self).__init__(multiworld, player)
        self.levelChains = {}
        self.sideTempleFinishEvent = "Finish plum_20"
        self.cobdFinishEvent = "Finish vulca_20"

        # If not in lumsanity mode we have to determine the available lums
        # using accessible regions which means we have to check reachability
        # in entrance requirements on lum gate portals. So we disable this setting!
        # It'd be complicated to work around so we eat the performance cost for R2.
        self.explicit_indirect_conditions = False

    def applyAccessRequirement(self, accessible, tech: Tech):
        """Applies the relevant access requirement to an accessible object."""
        if tech != Tech.NONE:
            accessible.access_rule = lambda state: self.has_tech(state, tech)

    def create_level(self, sublevels: dict[str, SubLevelInfo], levelChain: list[str]) -> Tuple[Region | None, Region | None]:
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

            # Add this level to the chain for this level
            levelChain.append(subLevelName)

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
        event_location.show_in_spoiler = False
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

    def has_tech(self, state: CollectionState, tech: Tech) -> bool:
        """Returns whether the given state has the items to complete the given tech."""
        match tech:
            case Tech.PURPLE_SWING | Tech.BAYOU_DAMAGE_BOOST | Tech.PURPLE_SWING_OR_BACKWARDS_JUMP | Tech.PURPLE_SWING_OR_GLM:
                return state.has("Silver Lum", self.player)
            case Tech.ELIXIR_AND_PURPLE_SWING:
                return state.has("Silver Lum", self.player) and state.has("Elixir of Life", self.player)
            case Tech.HAS_REENTERED_FROM_THAT_ONE_SPECIFIC_EXIT:
                return state.has(self.sideTempleFinishEvent, self.player)
            case Tech.COMPLETED_COBD:
                return state.has(self.cobdFinishEvent, self.player)
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
            zones = []
            for levelInfo in allLevels:
                for subLevelName, subLevelInfo in levelInfo.sublevels.items():
                    # If this region is reachable count all lums in the region, also check
                    # if they have the necessary tech to get the ones behind a requirement
                    if state.can_reach_region(subLevelName, self.player):
                        zones.append(subLevelName)
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
            levelChain = []
            if levelInfo.chain is not None:
                self.levelChains[levelInfo.chain] = levelChain
            firstRegion, lastRegion = self.create_level(levelInfo.sublevels, levelChain)
            if firstRegion is None or lastRegion is None:
                continue

            # Finishing the last level of each standard world creates a hall of doors portal!
            self.create_mapmonde_portal_event(lastRegion, portal)

            # Create a portal for each level on the hall of doors
            mapmonde_exit = self.create_entrance_portal(menu, f"Portal #{portal + 1}", portal, levelInfo.lumGate, levelInfo.requireAllMasks)
            portal += 1

            # Connect the portal automatically to non-randomised levels (first/last)
            if levelInfo.chain is None:
                mapmonde_exit.connect(firstRegion)

        # Go through the extra levels and create them separately
        for extraLevelInfo in extra_levels:
            last_level: Region = None
            extra_rule: Callable[[CollectionState], bool] = None
            isRevisit = False
            match extraLevelInfo.displayName:
                case "The Fairly Glade #2 - Revisit":
                    last_level = self.get_region("cask_10")
                    isRevisit = True
                case "The Sanctuary of Stone and Fire - Side Temple":
                    last_level = self.get_region("plum_00")
                    isRevisit = True
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
            levelChain = []
            if extraLevelInfo.chain is not None:
                self.levelChains[extraLevelInfo.chain] = levelChain
            firstRegion, lastRegion = self.create_level(extraLevelInfo.sublevels, levelChain)
            if firstRegion is None:
                continue

            # Create an entrance in the source level
            self.create_entrance_portal(last_level, f"Portal to {firstRegion.name}", lum_gate=extraLevelInfo.lumGate, require_all_masks=extraLevelInfo.requireAllMasks, extra_rule=extra_rule)

            # Create an exit back to the source level from the side-level only for the revisits
            if isRevisit:
                self.connect_internal(lastRegion, last_level)

        # Go through all location and create them
        for data in location_table:
            # If not on lumsanity, don't shuffle in the lums!
            if data.itemName == "Lum" and not self.options.lumsanity.value:
                continue

            region = self.multiworld.get_region(data.region, self.player)
            location = Rayman2Location(self.player, data.displayName, data.id, region)

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

    def connect_levels(self):
        """Connects together regions based on the level chains set."""
        # Create a mapping of all sub levels and their info
        subLevelsById = {}
        allLevels: list[LevelInfo] = []
        allLevels += levels
        allLevels += extra_levels
        for levelInfo in allLevels:
            for subLevelName, subLevelInfo in levelInfo.sublevels.items():
                subLevelsById[subLevelName] = subLevelInfo

        # Print available checks per section
        # TODO Remove this!
        idx = 0
        tl = 0
        ci = 0
        for _, chainLevels in self.levelChains.items():
            ci += 1
            for subLevelId in chainLevels:
                info = subLevelsById[subLevelId]
                t = info.get_total_lumsane_lums()
                tl += t
                idx += 1
                print(f"Level #{idx} (Chain #{ci}) - {subLevelId} has {t} lumsane lums, total so far {tl}")

        # Go through all level chains and hook them up
        mapmonde = self.get_region("Menu")
        portal = 1
        for chainId, chainLevels in self.levelChains.items():
            # TODO Remove this!
            print(f"Level chain {chainId}: {chainLevels}")
            index = 0
            lastRegion: Region | None = None

            # If this is a revisit we have to connect up the room properly back to where
            # it originated from.
            isRevisit = chainId == "side_temple" or chainId == "fairy_glade_revisit"

            for subLevelName in chainLevels:
                index += 1

                # Find the data for this level
                subLevelInfo = subLevelsById[subLevelName]
                if subLevelInfo is None:
                    raise KeyError(f"Could not find sub level called {subLevelName}")

                # Find the region for this level
                region = self.get_region(subLevelName)

                # If this is the first region we connect it to the map portal
                if index == 1:
                    portal += 1
                    portalName = f"Portal #{portal}"
                    mapmonde_exit = next((x for x in mapmonde.get_exits() if x.name == portalName and x.connected_region is None), None)
                    if mapmonde_exit is not None:
                        mapmonde_exit.connect(region)

                # If this chain has a previous region it has an exit we have to connect to!
                if lastRegion is not None:
                    exits = list(lastRegion.get_exits())
                    for exit in exits:
                        if not exit.name.startswith("Portal to"):
                            exit.connect(region)
                            break
                lastRegion = region

                # If this region has a portal exit we link it up
                regionExits = list(region.get_exits())
                for regionExit in regionExits:
                    if regionExit.name.startswith("Portal to"):
                        target = None
                        match regionExit.name:
                            case "Portal to plum_20":
                                target = "side_temple"
                            case "Portal to Learn_32":
                                target = "fairy_glade_revisit"
                            case "Portal to vulca_10":
                                target = "cave_of_bad_dreams"
                            case "Portal to Ly_10":
                                target = "walk_of_life"
                            case "Portal to Ly_20":
                                target = "walk_of_power"
                            case _:
                                raise KeyError(f"Invalid exit name for side-level: {regionExit.name}")

                        # Connect this portal to the first level of the target chain
                        firstRegion = self.levelChains[target][0]
                        firstRegionObj = self.get_region(firstRegion)
                        regionExit.connect(firstRegionObj)

                # If this is the last of a revisit we need to hook it back up to where we came from
                if isRevisit and index == len(chainLevels):
                    exits = list(region.get_exits())
                    for exit in exits:
                        if not exit.name.startswith("Portal to"):
                            # Determine the base game level where this side-area normally ends!
                            target = None
                            match chainId:
                                case "side_temple":
                                    target = self.get_region("plum_00")
                                case "fairy_glade_revisit":
                                    target = self.get_region("cask_10")
                                case "cave_of_bad_dreams":
                                    target = self.get_region("Ski_10")
                                case "walk_of_life":
                                    target = self.get_region("chase_10")
                                case "walk_of_power":
                                    target = self.get_region("earth_10")
                                case _:
                                    raise KeyError(f"Invalid exit name for side-level chain: {chainId}")

                            exit.connect(target)
                            break

    def generate_early(self) -> None:
        """Ensures that key items are placed early so you cannot get stuck as many levels require it to complete."""
        self.multiworld.local_early_items[self.player]["Silver Lum"] = 1
        # self.multiworld.local_early_items[self.player]["Knowledge of the Cave of Bad Dreams"] = 1
        # self.multiworld.local_early_items[self.player]["Elixir of Life"] = 1

    def connect_entrances(self) -> None:
        """Connect entrances of any disconnected regions in room randomisation mode."""
        # If we're in UT we don't re-randomize!
        if getattr(self.multiworld, "generation_is_fake", False):
            return

        # If we're in room randomisation mode, generate the layout!
        if self.options.room_randomisation.value:
            # Run the custom generator
            generator = GeneratorState(self.random, self.options.lumsanity.value)
            generator.assemble_initial_levels(self.options)
            generator.generate()

            # Connect up the map based on the generator's work, ignoring the base level chains
            self.levelChains = generator.level_chains
            self.sideTempleFinishEvent = generator.collected.sideTempleFinishEvent
            self.cobdFinishEvent = generator.collected.cobdFinishEvent

        self.connect_levels()

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
        """Hook method used by Universal Tracker to load data from slot data back into Python so the game layout is consistent."""
        self.levelChains = slot_data["level_chains"]
        self.sideTempleFinishEvent = slot_data["side_temple_finish_event"]
        self.cobdFinishEvent = slot_data["cobd_finish_event"]
        self.connect_levels()

    def get_filler_item_name(self) -> str:
        """If necessary as a fallback, any filler items should be lums."""
        return "Lum"

    def fill_slot_data(self):
        """Includes all information needed by the game into the slot data."""
        return {
            "level_chains": self.levelChains,
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
            "side_temple_finish_event": self.sideTempleFinishEvent,
            "cobd_finish_event": self.cobdFinishEvent,
        }

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        """Includes decided level swaps in the spoiler file for debugging."""
        if not self.options.room_randomisation:
            return

        spoiler_handle.write(f"\nRayman 2 slot information:\n")
        for id, chain in self.levelChains.items():
            spoiler_handle.write(f"Level Chain {id}: {chain}\n")
