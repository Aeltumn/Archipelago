import copy
from enum import IntEnum
from typing import List, Dict

from BaseClasses import Entrance
from .Layout import SubLevelInfo, Tech, Checks, levels, extra_levels
from .Options import Rayman2Options

# The total amount of super lum checks that exist and can be placed.
TOTAL_SUPER_LUMS = 58

# The total amount of regular lum checks that exist and can be placed.
TOTAL_REGULAR_LUMS = 710

class GeneratorCollection:
    """A state of items collected from a generation."""
    events: List[str] = []
    zones: List[str] = []
    lumSaneLums: int = 0
    # Woods of Light is always first and provides at least 7 checks which is enough for any tech items!
    checks: int = 7

    def get_maximum_obtainable_lums(self, lumsanity: int) -> int:
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
        if not lumsanity:
            lums += self.lumSaneLums

        # In lum sanity we also check where we can place the regular
        # lum checks.
        if lumsanity and checksForLums > 0:
            regularLums = checksForLums
            if regularLums > TOTAL_REGULAR_LUMS:
                regularLums = TOTAL_REGULAR_LUMS
            lums += regularLums

        return lums

    def add_items(self, checks: Checks, lumsanity: int):
        """Adds the items from the given [checks] to this collection."""
        checks += checks.get_total_checks(lumsanity)
        if not lumsanity:
            self.lumSaneLums += len(checks.regularLums)

    def could_have_tech(self, tech: Tech) -> bool:
        """Returns whether this state could have acquired [tech] in some way."""
        match tech:
            case Tech.HAS_REENTERED_FROM_THAT_ONE_SPECIFIC_EXIT:
                return "Finish Side Temple" in self.events
            case Tech.NONE:
                return True
            case _:
                raise KeyError(f"Invalid tech type {tech}")

class RoomType(IntEnum):
    """The types of rooms we can place."""
    STANDARD = 0
    ENTRANCE = 1
    EXIT = 2
    BOTH = 3
    INTERNAL = 4

class GeneratorLevel:
    """Stores information on a single level in the Rayman 2 generator."""
    lumsRequired: int = 0
    zoneRequired: str | None = None
    length: Dict[RoomType, int] = {}

    def is_extendable(self) -> bool:
        """Returns whether this level supports adding additional segments in the middle."""
        return self.length.get(RoomType.ENTRANCE, 0) > 0

class GeneratorState:
    """Stores the overall state of the Rayman 2 generator."""
    lumsanity: int
    levels: List[GeneratorLevel] = []
    remaining: Dict[RoomType, List[SubLevelInfo]] = {}
    collected: GeneratorCollection = GeneratorCollection()
    pairings: Dict[str, str] = {}

    def assemble_initial_levels(self, options: Rayman2Options):
        """Assembles the initial level layout for the game."""
        lastLumRequirement = 0
        for levelInfo in levels:
            # The Woods of Light and Crow's Nest are not randomised so the randomiser always starts
            # with enough lums and you can end the game properly at the end.
            if levelInfo.displayName == "The Woods of Light" or levelInfo.displayName == "The Crow's Nest":
                continue

            # Create a new level which defaults to having one starting and one ending level
            newLevel = GeneratorLevel()
            self.levels.append(newLevel)
            newLevel.length[RoomType.ENTRANCE] = 1
            newLevel.length[RoomType.EXIT] = 1

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
            for segment in levelInfo.sublevels:
                # Determine the type of this level
                type = 0
                if index == 0:
                    type += 1
                if index == total - 2:
                    type += 2
                roomType = RoomType(type)

                # Add the level segments to the list of remaining segments
                sublist = self.remaining.get(roomType, [])
                sublist += segment
                self.remaining[roomType] = sublist

        for levelInfo in extra_levels:
            # Create a new level which defaults to having one starting and one ending level
            newLevel = GeneratorLevel()
            self.levels.append(newLevel)
            match levelInfo.displayName:
                case "The Cave of Bad Dreams":
                    # The Cave of Bad Dreams has multiple segments!
                    newLevel.length[RoomType.ENTRANCE] = 1
                    newLevel.length[RoomType.EXIT] = 1
                case "The Walk of Life" | "The Walk of Power":
                    # The walks should be randomised with each other as they start
                    # a custom script and return you to the hall of doors normally.
                    newLevel.length[RoomType.BOTH] = 1
                case _:
                    # The two revisits should get randomised together as well.
                    newLevel.length[RoomType.INTERNAL] = 1

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

    def generate(self, entrances: Dict[str, Entrance]):
        """Generates the level layout state."""
        print("Now we got here, what do we do next")
        raise ValueError("Not yet implemented, use non-room randomisation on this build!")

    def get_maximum_obtainable(self, level_id: str, level: SubLevelInfo) -> GeneratorCollection:
        """Returns the maximum collection that can be obtained by adding [level]."""
        goal = copy.deepcopy(self.collected)

        # Add the checks for all items that are accessible in some way
        goal.add_items(level.checks, self.lumsanity)
        for tech, checks in level.behindRequirements:
            if goal.could_have_tech(tech):
                goal.add_items(checks, self.lumsanity)

        # If we could have the tech to finish this level, we assume we can!
        if goal.could_have_tech(level.exitRequirement):
            goal.events += f"Finish {level_id}"
        goal.zones += level_id

        return goal