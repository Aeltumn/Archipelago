from dataclasses import dataclass
from typing import List

from Options import Range, DeathLink, Choice, OptionGroup, T, Toggle
from worlds.AutoWorld import PerGameCommonOptions


class EndGoal(Choice):
    """The end goal required to beat the game.

    Crow's Nest: Defeat Razorbeard in the Crow's Nest.
    Treasure%: Take Jano's offer in the Cave of Bad Dreams.
    100%: Requires collecting all 1000 lums, 80 cages, and 4 masks, then defeating Razorbeard.
    """
    display_name = "End Goal"
    option_crows_nest = 1
    option_treasure = 2
    option_100 = 3
    default = 1

    @classmethod
    def get_option_name(cls, value) -> str:
        if value == 1:
            return "Crow's Nest"
        elif value == 2:
            return "Treasure%"
        else:
            return "100%"

class RoomRandomisation(Toggle):
    """[EXPERIMENTAL] - Whether to enable room randomisation. Currently implemented using generic entrance randomisation which often results in invalid configurations."""
    display_name = "Room Randomisation"
    default = False

class Lumsanity(Toggle):
    """Whether all individual yellow lums should be their own checks. If disabled, only super yellow lums are checks instead of all yellow lums."""
    display_name = "Shuffle All Yellow Lums"
    default = True

class FirstGateRequirement(Range):
    """The amount of lums required to enter the Sanctuary of Water and Ice."""
    display_name = "First Lum Gate Requirement"
    range_start = 0
    range_end = 1000
    default = 100


class SecondGateRequirement(Range):
    """The amount of lums required to enter the Sanctuary of Stone & Fire."""
    display_name = "Second Lum Gate Requirement"
    range_start = 0
    range_end = 1000
    default = 300


class ThirdGateRequirement(Range):
    """The amount of lums required to enter Beneath the Sanctuary of Rock & Lava."""
    display_name = "Third Lum Gate Requirement"
    range_start = 0
    range_end = 1000
    default = 450


class FourthGateRequirement(Range):
    """The amount of lums required to enter the Iron Mountains."""
    display_name = "Fourth Lum Gate Requirement"
    range_start = 0
    range_end = 1000
    default = 550


class WalkOfLifeRequirement(Range):
    """The amount of lums required to enter the Walk of Life."""
    display_name = "Walk of Life Lum Requirement"
    range_start = 0
    range_end = 1000
    default = 60


class WalkOfPowerRequirement(Range):
    """The amount of lums required to enter the Walk of Power."""
    display_name = "Walk of Power Lum Requirement"
    range_start = 0
    range_end = 1000
    default = 475


@dataclass
class Rayman2Options(PerGameCommonOptions):
    end_goal: EndGoal
    death_link: DeathLink

    room_randomisation: RoomRandomisation
    lumsanity: Lumsanity

    first_gate_required: FirstGateRequirement
    second_gate_required: SecondGateRequirement
    third_gate_required: ThirdGateRequirement
    fourth_gate_required: FourthGateRequirement
    walk_of_life_required: WalkOfLifeRequirement
    walk_of_power_required: WalkOfPowerRequirement


def create_option_groups() -> List[OptionGroup]:
    return [
        OptionGroup(name="Lum Requirement Options",
                    options=[WalkOfLifeRequirement, FirstGateRequirement, SecondGateRequirement, WalkOfPowerRequirement, ThirdGateRequirement, FourthGateRequirement])
    ]
