import dataclasses
import random
from dataclasses import dataclass
from enum import IntEnum
from typing import Tuple

from .Layout import SubLevelInfo, Checks, levels, extra_levels
from .Options import Rayman2Options

# The total amount of super lum checks that exist and can be placed.
TOTAL_SUPER_LUMS = 58

# The total amount of regular lum checks that exist and can be placed.
TOTAL_REGULAR_LUMS = 710

# The total amount of cages.
TOTAL_CAGES = 80

@dataclass
class GeneratorCollection:
    """A state of items collected from a generation."""
    events: list[str] = dataclasses.field(default_factory=list)
    zones: list[str] = dataclasses.field(default_factory=list)
    lumSaneLums: int = 0
    # Woods of Light is always first and provides at least 7 checks which is enough for any tech items!
    checks: int = 7
    waitingChecks: list[Checks] = dataclasses.field(default_factory=list)
    sideTempleFinishEvent: str | None = None

    def get_maximum_obtainable_lums(self, lumsanity: int) -> int:
        """Returns the maximum amount of lums that can be obtained with how many checks are accessible"""
        lums = 0

        # We assume the first three checks are taken by any progression items.
        checksForLums = self.checks - 10

        # Take away up to 80 checks which are used for the cages
        if checksForLums > 0:
            # 1/8th of early lums are assumed to be taken up by cages
            cageChecks = checksForLums / 8
            if cageChecks > TOTAL_CAGES:
                cageChecks = TOTAL_CAGES
            checksForLums -= cageChecks

        if not lumsanity:
            # Outside lumsanity you can obtain lums on your own!
            lums += self.lumSaneLums

            # Outside lumsanity we use all checks for super lums!
            if checksForLums > 0:
                superLums = checksForLums
                if superLums > TOTAL_SUPER_LUMS:
                    superLums = TOTAL_SUPER_LUMS
                lums += superLums * 5
                checksForLums -= superLums
        else:
            # A tenth of lums are assumed to be super lums
            earlySuperLums = 0
            if checksForLums > 0:
                superLums = checksForLums / 10
                if superLums > TOTAL_SUPER_LUMS:
                    superLums = TOTAL_SUPER_LUMS
                lums += superLums * 5
                earlySuperLums += superLums
                checksForLums -= superLums

            # In lumsanity we first use checks for lums, then super lums!
            if checksForLums > 0:
                regularLums = checksForLums
                if regularLums > TOTAL_REGULAR_LUMS:
                    regularLums = TOTAL_REGULAR_LUMS
                lums += regularLums
                checksForLums -= regularLums

            if checksForLums > 0:
                superLums = checksForLums
                total = TOTAL_SUPER_LUMS - earlySuperLums
                if superLums > total:
                    superLums = total
                lums += superLums * 5
                checksForLums -= superLums

        return lums

    def add_items(self, checks: Checks, lumsanity: int, requires_exit: bool = False):
        """Adds the items from the given [checks] to this collection."""
        if requires_exit and not self.has_side_temple():
            self.waitingChecks.append(checks)
            return

        self.checks += len(checks.superLums)
        self.checks += len(checks.cages)

        regularLums = len(checks.regularLums)
        if not lumsanity:
            self.lumSaneLums += regularLums
        else:
            self.checks += regularLums

    def add_event(self, event: str, lumsanity: int):
        """Adds an event to this state."""
        self.events.append(event)

        # Once the side temple is finished, award the waiting checks!
        if self.sideTempleFinishEvent is not None and event == self.sideTempleFinishEvent:
            for check in self.waitingChecks:
                self.add_items(check, lumsanity)

    def has_side_temple(self) -> bool:
        """Returns whether the side temple can be reached."""
        return self.sideTempleFinishEvent is not None and self.sideTempleFinishEvent in self.events

    def include_level(self, subLevelId: str, level: SubLevelInfo, isSideTemple: bool, lumsanity: int):
        """Adds the results of completing [level] to this collection set."""
        # Add the checks for all items that are accessible in some way
        self.add_items(level.checks, lumsanity)
        for tech, checks in level.behindRequirements.items():
            self.add_items(checks, lumsanity, tech.requires_that_one_exit)

        # If this is the side temple then this allows you to reach those specific checks!
        if isSideTemple:
            self.sideTempleFinishEvent = f"Finish {subLevelId}"

        # If we could have the tech to finish this level, we assume we can!
        self.add_event(f"Finish {subLevelId}", lumsanity)

        # Mark down that this zone is now accessible!
        self.zones.append(subLevelId)

class RoomType(IntEnum):
    """The types of rooms we can place."""
    STANDARD = 0
    ENTRANCE = 1
    EXIT = 2
    BOTH = 3

@dataclass
class GeneratorLevel:
    """Stores information on a single level in the Rayman 2 generator."""
    name: str
    lumsRequired: int = 0
    zoneRequired: str | None = None
    baseGame: dict[RoomType, list[Tuple[str, SubLevelInfo]]] = dataclasses.field(default_factory=dict)
    generated: dict[RoomType, list[Tuple[str, SubLevelInfo]]] = dataclasses.field(default_factory=dict)
    isSideTemple: bool = False
    isRevisit: bool = False

    def get_output(self) -> list[str]:
        """Returns the order of this level in the generation."""
        order = []
        for entry in self.generated.get(RoomType.ENTRANCE, []):
            order.append(entry[0])
        for entry in self.generated.get(RoomType.STANDARD, []):
            order.append(entry[0])
        for entry in self.generated.get(RoomType.EXIT, []):
            order.append(entry[0])
        for entry in self.generated.get(RoomType.BOTH, []):
            order.append(entry[0])
        return order

    def is_extendable(self) -> bool:
        """Returns whether this level supports adding additional segments in the middle."""
        return len(self.baseGame.get(RoomType.ENTRANCE, [])) > 0


@dataclass
class GeneratorState:
    """Stores the overall state of the Rayman 2 generator."""
    random: random.Random
    lumsanity: int
    fixed_level_lengths: int
    levels: dict[str, GeneratorLevel] = dataclasses.field(default_factory=dict)
    remaining: dict[RoomType, list[Tuple[str, SubLevelInfo]]] = dataclasses.field(default_factory=dict)
    early_collected: GeneratorCollection = dataclasses.field(default_factory=GeneratorCollection)
    collected: GeneratorCollection = dataclasses.field(default_factory=GeneratorCollection)
    level_chains: dict[str, list[str]] = dataclasses.field(default_factory=dict)

    def assemble_initial_levels(self, options: Rayman2Options):
        """Assembles the initial level layout for the game."""
        lastLumRequirement = 0
        regularLumRequirements = {}
        for levelInfo in levels:
            # Ignore levels without a chain (Crow's Nest)
            if levelInfo.chain is None:
                continue

            # Create a new level which defaults to having one starting and one ending level
            newLevel = GeneratorLevel(levelInfo.chain, 0, None, {})
            self.levels[levelInfo.chain] = newLevel

            # Mark whether this is a lum gate
            if levelInfo.lumGate is not None:
                match levelInfo.lumGate:
                    case 0:
                        lastLumRequirement = options.first_gate_required.value
                    case 1:
                        lastLumRequirement = options.second_gate_required.value
                    case 2:
                        lastLumRequirement = options.third_gate_required.value
                    case 3:
                        lastLumRequirement = options.fourth_gate_required.value
            newLevel.lumsRequired = lastLumRequirement

            # Add all the level segments in the original list to the remaining areas
            index = 0
            total = len(levelInfo.sublevels)
            for subLevelId, segment in levelInfo.sublevels.items():
                # Determine the type of this level
                typeId = 0
                if index == 0:
                    typeId += 1
                if index == total - 1:
                    typeId += 2
                roomType = RoomType(typeId)
                index += 1

                # Add the level segment to the level itself
                sublist1 = newLevel.baseGame.get(roomType, [])
                sublist1.append([subLevelId, segment])
                newLevel.baseGame[roomType] = sublist1

                # Add the level segments to the list of remaining segments
                sublist = self.remaining.get(roomType, [])
                sublist.append([subLevelId, segment])
                self.remaining[roomType] = sublist

                # Store the lums required to get to a base level
                regularLumRequirements[subLevelId] = lastLumRequirement

        for levelInfo in extra_levels:
            # Create a new level which defaults to having one starting and one ending level
            newLevel = GeneratorLevel(levelInfo.chain, 0, None, {})
            self.levels[levelInfo.chain] = newLevel

            # Link up which other level you must have accessed to gain access to these levels
            match levelInfo.displayName:
                case "The Fairly Glade #2 - Revisit":
                    newLevel.zoneRequired = "cask_10"
                case "The Sanctuary of Stone and Fire - Side Temple":
                    newLevel.zoneRequired = "plum_00"
                case "The Cave of Bad Dreams":
                    # You also need the knowledge but there's accessible lums in Ski_10 that can give you that,
                    # so we don't need to account for that when generating the layout, only when setting up the
                    # regions.
                    newLevel.zoneRequired = "Ski_10"
                case "The Walk of Life":
                    newLevel.zoneRequired = "chase_10"
                case "The Walk of Power":
                    newLevel.zoneRequired = "earth_10"
                case _:
                    raise KeyError(f"Unknown extra level {levelInfo.displayName}")

            # Mark whether this is a lum gate
            if levelInfo.lumGate is not None:
                match levelInfo.lumGate:
                    case 4:
                        newLevel.lumsRequired = options.walk_of_life_required.value
                    case 5:
                        newLevel.lumsRequired = options.walk_of_power_required.value
            else:
                newLevel.lumsRequired = regularLumRequirements[newLevel.zoneRequired]

            # Add all the level segments in the original list to the remaining areas
            index = 0
            total = len(levelInfo.sublevels)
            for subLevelId, segment in levelInfo.sublevels.items():
                # Determine the type of this level
                typeId = 0
                if index == 0:
                    typeId += 1
                if index == total - 1:
                    typeId += 2

                # The revisits are special and considered standard rooms!
                if subLevelId == "Learn_32" or subLevelId == "plum_20":
                    typeId = 0
                    newLevel.isRevisit = True

                # If this is the side temple, not that down!
                if subLevelId == "plum_20":
                    newLevel.isSideTemple = True

                roomType = RoomType(typeId)
                index += 1

                # Add the level segment to the level itself
                sublist1 = newLevel.baseGame.get(roomType, [])
                sublist1.append([subLevelId, segment])
                newLevel.baseGame[roomType] = sublist1

                # Add the level segments to the list of remaining segments
                sublist = self.remaining.get(roomType, [])
                sublist.append([subLevelId, segment])
                self.remaining[roomType] = sublist

    def redetermine_collected(self):
        """Redetermines which items can be collected in currently generated levels."""
        completedFully = False
        while not completedFully:
            # We set completed fully to true every turn
            # and if we make it all the way through without
            # any new discoveries we can stop.
            completedFully = True
            maxLums = self.collected.get_maximum_obtainable_lums(self.lumsanity)

            for level in self.levels.values():
                # Ignore levels we cannot yet access!
                if level.zoneRequired is not None and level.zoneRequired not in self.collected.zones:
                    continue

                if level.lumsRequired > maxLums:
                    continue

                for _, rooms in level.generated.items():
                    for xLevelId, xLevelInfo in rooms:
                        # Ignore zones we already collected!
                        if xLevelId in self.collected.zones:
                            continue

                        self.collected.include_level(xLevelId, xLevelInfo, level.isSideTemple, self.lumsanity)
                        completedFully = False

    def add_to_level(self, level: GeneratorLevel, room_type: RoomType, choice: Tuple[str, SubLevelInfo], early: bool = False):
        """Adds the given [choice] to [level] under [room_type]."""
        # Remove this option for future level swaps
        options = self.remaining.get(room_type, [])
        options.remove(choice)

        # Add the checks within this level to the current state & early state
        subLevelId, levelInfo = choice
        if early:
            collected = self.early_collected
        else:
            collected = self.collected

        collected.include_level(subLevelId, levelInfo, level.isSideTemple, self.lumsanity)

        # Add it to the level's generated list
        sublist = level.generated.get(room_type, [])
        sublist.append([subLevelId, levelInfo])
        level.generated[room_type] = sublist

        # Determine which levels this open up and claim the early collected list
        if not early:
            self.redetermine_collected()

    def select_for_level(self, level: GeneratorLevel, room_type: RoomType, options: list[Tuple[str, SubLevelInfo]], average_checks, early: bool = False):
        """Adds a room of the given [room_type] to [level]."""
        if len(options) == 0:
            raise ValueError(f"Not enough type {room_type} rooms to extend level, how did we pick this?")

        # If we can help it, avoid picking levels with less checks than needed!
        filteredOptions = []
        byPotential = []
        for levelId, levelInfo in options:
            # Count how many checks we can get here!
            lums = 0
            check = 0
            check += len(levelInfo.checks.superLums)
            check += len(levelInfo.checks.cages)
            lums += len(levelInfo.checks.regularLums)
            for _, checks in levelInfo.behindRequirements.items():
                check += len(checks.superLums)
                check += len(checks.cages)
                lums += len(checks.regularLums)

            # Vaguely judge potential as regular lums + 2.5x checks plus a free buffer
            # as we don't want to aggressively deny levels just favor higher ones!
            potential = 2.5 + lums + check * 2.5
            if potential > average_checks:
                filteredOptions.append([levelId, levelInfo])

            # Store all levels by potential
            byPotential.append([[levelId, levelInfo], potential])

        if len(filteredOptions) > 0:
            choice = self.random.choice(filteredOptions)
        else:
            # If all levels have too few lums, pick randomly from the top 3 with most lums!
            top_three = sorted(byPotential, key=lambda x: x[1], reverse=True)[:3]
            data = self.random.choice(top_three)
            choice = data[0]

        self.add_to_level(level, room_type, choice, early)

    def select_any_remaining_for_level(self, level: GeneratorLevel, room_type: RoomType, average_checks):
        """Adds a room from the remaining rooms of type [room_type] to [level]."""
        self.select_for_level(level, room_type, self.remaining.get(room_type, []), average_checks)

    def attempt_zone_required_generation(self) -> bool:
        """Attempts to place any restrictive room."""
        # Determine all levels we can place something in currently
        selectableLevels = list(filter(lambda it: it.zoneRequired is None or it.zoneRequired in self.early_collected.zones, self.levels.values()))

        # Determine all zones that need to be placed to unblock remaining levels!
        allRequiredZones = []
        for level in self.levels.values():
            if level.zoneRequired is not None and level.zoneRequired not in self.early_collected.zones:
                allRequiredZones.append(level.zoneRequired)

        # Determine all actions we can currently take which are all equally valid
        all_valid_placements_by_room = {}
        for level in selectableLevels:
            for roomType in level.baseGame.keys():
                # Determine if there's rooms missing that need filling!
                baseGameRooms = len(level.baseGame.get(roomType, []))
                generatedRooms = len(level.generated.get(roomType, []))
                if (not self.fixed_level_lengths and roomType == RoomType.STANDARD) or baseGameRooms > generatedRooms:
                    sublist = all_valid_placements_by_room.get(roomType, [])
                    all_valid_placements_by_room[roomType] = sublist
                    sublist.append(level)

        # For each room type determine which rooms we can still place
        for roomType, remainingRooms in self.remaining.items():
            # Get all levels we can place this room in
            all_valid_placements = all_valid_placements_by_room.get(roomType, [])
            if len(all_valid_placements) == 0:
                continue
            level = self.random.choice(all_valid_placements)

            # Determine all rooms that we are waiting to place
            selectableRooms = []
            for roomId, roomInfo in remainingRooms:
                if roomId in allRequiredZones:
                    selectableRooms.append([roomId, roomInfo])

            # If we can place a room, place it!
            if len(selectableRooms) > 0:
                self.select_for_level(level, roomType, selectableRooms, 0, True)
                return False

        return True

    def attempt_lum_gated_generation(self) -> bool:
        """Attempts to place one more room."""
        # Start by determining which levels are accessible currently given the lums we have
        maxLums = self.collected.get_maximum_obtainable_lums(self.lumsanity)
        selectableLevels = list(filter(lambda it: it.lumsRequired <= maxLums and it.zoneRequired is None or it.zoneRequired in self.collected.zones, self.levels.values()))
        nonSelectableLevels = list(filter(lambda it: it.lumsRequired > maxLums or (it.zoneRequired is not None and it.zoneRequired not in self.collected.zones), self.levels.values()))

        # Determine all actions we can currently take which are all equally valid
        all_valid_options = []

        # We can place any of the available rooms in a required remaining position (entrances, exits, both)
        for level in selectableLevels:
            for roomType in level.baseGame.keys():
                # Standard rooms are added by the extension code below!
                if not self.fixed_level_lengths and roomType == RoomType.STANDARD:
                    continue

                # Determine if there's rooms missing that need filling!
                baseGameRooms = len(level.baseGame.get(roomType, []))
                generatedRooms = len(level.generated.get(roomType, []))
                if baseGameRooms > generatedRooms:
                    all_valid_options.append([level, roomType])

        # If we have any standard rooms left to place we decide their locations, unless
        # we are using fixed level lengths where we just match the base game.
        if self.fixed_level_lengths:
            remainingExtenders = []
        else:
            remainingExtenders = self.remaining.get(RoomType.STANDARD, [])

        # Determine which revisits we have not selected as we have to cover them all at least once!
        remainingUnselectedRevisits = list(filter(lambda it: it.isRevisit and len(it.generated.get(RoomType.STANDARD, [])) <= 0, selectableLevels))

        if len(remainingUnselectedRevisits) > 0:
            # If there's revisits with zero levels inside we need to fill those first!
            for level in remainingUnselectedRevisits:
                # Add a random standard room to this level
                all_valid_options.append([level, RoomType.STANDARD])
        elif len(remainingExtenders) > 0 and len(all_valid_options) == 0:
            # We only add additional levels when we either don't need to worry about the future
            # or if we otherwise have nothing else we can select!
            for level in selectableLevels:
                # Ignore non-extendable levels!
                if not level.is_extendable():
                    continue

                # Add a random standard room to this level
                all_valid_options.append([level, RoomType.STANDARD])

        # If we're out of options we're done!
        nextLumGate = 0
        for level in nonSelectableLevels:
            if level.lumsRequired > 0 and level.lumsRequired > nextLumGate:
                nextLumGate = level.lumsRequired
        if len(all_valid_options) == 0:
            if len(nonSelectableLevels) > 0:
                raise KeyError(f"Lum gate {nextLumGate} is too high and makes it too hard to complete the generation!")
            return True

        # Pick a random choice from the list and run it!
        remaining_options = len(all_valid_options)
        average_checks = (nextLumGate - maxLums) / remaining_options
        level, roomType = self.random.choice(all_valid_options)
        self.select_any_remaining_for_level(level, roomType, average_checks)
        return False

    def generate(self):
        """Generates the level layout state."""
        # We place twice, first we start by placing all restricted levels
        # in places where they will definitely be accessible followed by placing
        # all remaining levels wherever they fit to have enough lums.
        while True:
            if self.attempt_zone_required_generation():
                break

        # Determine the collected state based on what is already generated
        self.redetermine_collected()

        # Perform regular generation which only accounts for lums
        while True:
            if self.attempt_lum_gated_generation():
                break

        # Require that we placed every level!
        for _, options in self.remaining.items():
            assert len(options) == 0

        # Determine the output level chains for everything
        all_levels = []
        all_levels += levels
        all_levels += extra_levels
        for level in all_levels:
            # Ignore levels without chain!
            if level.chain is None:
                continue

            # Ignore levels that didn't make it in, somehow?
            generatedLevel = self.levels.get(level.chain, None)
            if generatedLevel is None:
                continue

            # Determine the final created chain
            output = generatedLevel.get_output()
            self.level_chains[level.chain] = output