import copy
import dataclasses
import random
from dataclasses import dataclass
from enum import IntEnum
from typing import Iterable, Tuple

from BaseClasses import Region
from .Layout import SubLevelInfo, Tech, Checks, levels, extra_levels
from .Options import Rayman2Options

# The total amount of super lum checks that exist and can be placed.
TOTAL_SUPER_LUMS = 58

# The total amount of regular lum checks that exist and can be placed.
TOTAL_REGULAR_LUMS = 710

class GeneratorCollection:
    """A state of items collected from a generation."""
    lumsanity: int
    events: list[str] = []
    zones: list[str] = []
    lumSaneLums: int = 0
    # Woods of Light is always first and provides at least 7 checks which is enough for any tech items!
    checks: int = 7
    waitingEvents: dict[Tech, list[str]] = {}
    waitingChecks: dict[Tech, list[Checks]] = {}

    def get_maximum_obtainable_lums(self) -> int:
        """Returns the maximum amount of lums that can be obtained with how many checks are accessible"""
        lums = 0

        # We assume the first three checks are taken by a Silver Lum, Elixir of Life and Knowledge of the Cave of Bad Dreams,
        # we only want worst-case here so we can make sure the layout is not impossible, we assume there's plenty of checks
        # anyway as we mostly do things random, we just deny impossible layouts.
        checksForLums = self.checks - 3

        if checksForLums > 0:
            superLums = checksForLums
            if superLums > TOTAL_SUPER_LUMS:
                superLums = TOTAL_SUPER_LUMS
            lums += superLums * 5
            checksForLums -= superLums

        # Outside of lumsanity you can obtain lums on your own!
        if not self.lumsanity:
            lums += self.lumSaneLums

        # In lum sanity we also check where we can place the regular
        # lum checks.
        if self.lumsanity and checksForLums > 0:
            regularLums = checksForLums
            if regularLums > TOTAL_REGULAR_LUMS:
                regularLums = TOTAL_REGULAR_LUMS
            lums += regularLums

        return lums

    def add_items(self, checks: Checks, tech: Tech = Tech.NONE):
        """Adds the items from the given [checks] to this collection."""
        if not self.could_have_tech(tech):
            # If this tech is out of reach, then queue up the checks!
            sublist = self.waitingChecks.get(tech, [])
            sublist.append(checks)
            self.waitingChecks[tech] = sublist
            return

        self.checks += checks.get_total_checks(self.lumsanity)
        if not self.lumsanity:
            self.lumSaneLums += len(checks.regularLums)

    def add_event(self, event: str, tech: Tech = Tech.NONE):
        """Adds an event to this state."""
        if not self.could_have_tech(tech):
            # If this tech is out of reach, then queue up the event!
            sublist = self.waitingEvents.get(tech, [])
            sublist.append(event)
            self.waitingEvents[tech] = sublist
            return

        self.events.append(event)
        if event == "Finish Side Temple":
            self.award_tech(Tech.HAS_REENTERED_FROM_THAT_ONE_SPECIFIC_EXIT)

    def award_tech(self, tech: Tech):
        """Handles [tech] becoming available."""
        checks = self.waitingChecks.get(tech, [])
        for check in checks:
            self.add_items(check)
        self.waitingChecks[tech] = []

        events = self.waitingEvents.get(tech, [])
        for event in events:
            self.add_event(event)
        self.waitingEvents[tech] = []

    def could_have_tech(self, tech: Tech) -> bool:
        """Returns whether this state could have acquired [tech] in some way."""
        match tech:
            case Tech.HAS_REENTERED_FROM_THAT_ONE_SPECIFIC_EXIT:
                return "Finish Side Temple" in self.events
            case _:
                return True

    def include_level(self, subLevelId: str, level: SubLevelInfo, isSideTemple: bool):
        """Adds the results of completing [level] to this collection set."""
        # Add the checks for all items that are accessible in some way
        self.add_items(level.checks)
        for tech, checks in level.behindRequirements.items():
            self.add_items(checks, tech)

        # If we could have the tech to finish this level, we assume we can!
        self.add_event(f"Finish {subLevelId}", level.exitRequirement)

        # If this is the side temple then this allows you to reach those specific checks!
        if isSideTemple:
            self.add_event("Finish Side Temple", level.exitRequirement)

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


class GeneratorState:
    """Stores the overall state of the Rayman 2 generator."""
    lumsanity: int
    levels: dict[str, GeneratorLevel] = {}
    remaining: dict[RoomType, list[Tuple[str, SubLevelInfo]]] = {}
    collected: GeneratorCollection = GeneratorCollection()
    levelChains: dict[str, list[str]] = {}
    sideTemple: str | None = None

    def assemble_initial_levels(self, options: Rayman2Options):
        """Assembles the initial level layout for the game."""
        # Ensure lumsanity state is synced!
        self.collected.lumsanity = self.lumsanity

        lastLumRequirement = 0
        for levelInfo in levels:
            # The Woods of Light and Crow's Nest are not randomised so the randomiser always starts
            # with enough lums and you can end the game properly at the end.
            if levelInfo.displayName == "The Woods of Light" or levelInfo.displayName == "The Crow's Nest":
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

                roomType = RoomType(typeId)
                index += 1

                # If this is the side temple, not that down!
                if subLevelId == "plum_20":
                    newLevel.isSideTemple = True

                # Add the level segment to the level itself
                sublist1 = newLevel.baseGame.get(roomType, [])
                sublist1.append([subLevelId, segment])
                newLevel.baseGame[roomType] = sublist1

                # Add the level segments to the list of remaining segments
                sublist = self.remaining.get(roomType, [])
                sublist.append([subLevelId, segment])
                self.remaining[roomType] = sublist

    def add_to_level(self, level: GeneratorLevel, roomType: RoomType, choice: Tuple[str, SubLevelInfo]):
        # Remove this option for future level swaps
        options = self.remaining.get(roomType, [])
        options.remove(choice)

        # Add the checks within this level to the current state
        subLevelId, levelInfo = choice
        self.collected.include_level(subLevelId, levelInfo, level.isSideTemple)

        # Add it to the level's generated list
        sublist = level.generated.get(roomType, [])
        sublist.append([subLevelId, levelInfo])
        level.generated[roomType] = sublist

    def select_for_level(self, level: GeneratorLevel, roomType: RoomType):
        """Adds a room of the given [type] to [level]."""
        options = self.remaining.get(roomType, [])
        if len(options) == 0:
            raise ValueError(f"Not enough type {roomType} rooms to extend level, how did we pick this?")
        choice = random.choice(options)
        self.add_to_level(level, roomType, choice)

    def attempt_generation_step(self) -> bool:
        """Attempts to place one more room."""
        # Start by determining which levels are accessible currently given the lums we have
        maxLums = self.collected.get_maximum_obtainable_lums()
        selectableLevels = list(filter(lambda it: it.lumsRequired <= maxLums and (it.zoneRequired is None or it.zoneRequired in self.collected.zones), self.levels.values()))

        # Determine which levels of which types are currently being blocked
        blockedLevels = list(filter(lambda it: it.lumsRequired <= maxLums and it.zoneRequired is not None and it.zoneRequired not in self.collected.zones, self.levels.values()))
        blockedTypes = {}
        for blockedLevel in blockedLevels:
            roomType = None
            for rt, options in self.remaining.items():
                for levelId, _ in options:
                    if levelId == blockedLevel.zoneRequired:
                        roomType = rt
            blockedTypes[roomType] = blockedTypes.get(roomType, 0) + 1

        # Determine all actions we can currently take which are all equally valid
        all_valid_options = []

        # We can place any of the available rooms in a required remaining position (entrances, exits, both)
        for level in selectableLevels:
            for roomType in level.baseGame.keys():
                # Standard rooms are added by the extension code below!
                if roomType == RoomType.STANDARD:
                    continue

                # Determine if there's rooms missing that need filling!
                baseGameRooms = len(level.baseGame.get(roomType, []))
                generatedRooms = len(level.generated.get(roomType, []))
                if baseGameRooms > generatedRooms:
                    all_valid_options.append([level, roomType])

        # If we have any standard rooms left to place we decide their locations
        remainingExtenders = self.remaining.get(RoomType.STANDARD, [])
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
        if len(all_valid_options) == 0:
            return True

        # If we have any blocked levels that are not yet accessible because we are missing some zone, we force
        # that zone to be placed somewhere so it gets unblocked! Since we keep all options open and don't place
        # in order this shouldn't result in the side-level access zones from being weirdly early or anything.
        if len(blockedLevels) > 0:
            # Check how many options we have left for each room type, if there's less than 3 remaining
            # we start forcing the selections!
            byRoomType = {}
            for option in all_valid_options:
                byRoomType[option[1]] = byRoomType.get(option[1], 0) + 1
            lowest = 999
            lowestType = RoomType.STANDARD
            for roomType, count in byRoomType.items():
                # Ignore room types that do not block anything!
                if blockedTypes.get(roomType) is not None and count < lowest:
                    lowest = count
                    lowestType = roomType

            if lowest < 3:
                allLowestLevels = list(filter(lambda it: it[1] == lowestType, all_valid_options))
                requiredZones = list(map(lambda it: it.zoneRequired, blockedLevels))
                validOptions = list(filter(lambda it: it[0] in requiredZones, self.remaining.get(lowestType, [])))
                if len(validOptions) == 0:
                    raise ValueError(f"Not enough type {validOptions} rooms that open something up, why are we here?")
                choice = random.choice(validOptions)
                level, _ = random.choice(allLowestLevels)
                self.add_to_level(level, lowestType, choice)
                return False

        # Pick a random choice from the list and run it!
        level, roomType = random.choice(all_valid_options)
        self.select_for_level(level, roomType)
        return False

    def generate(self):
        """Generates the level layout state."""
        # Continuously perform generation steps until we run out of options!
        while True:
            if self.attempt_generation_step():
                break

        # Require that we placed every level!
        for _, options in self.remaining.items():
            assert len(options) == 0

        # Determine the output level chains for everything
        all_levels = []
        all_levels += levels
        all_levels += extra_levels
        for level in all_levels:
            generatedLevel = self.levels.get(level.chain, None)
            if generatedLevel is not None:
                self.levelChains[level.chain] = generatedLevel.get_output()