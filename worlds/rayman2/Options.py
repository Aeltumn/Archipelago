from dataclasses import dataclass
from typing import List

from Options import Range, DeathLink, Choice, OptionGroup, Toggle
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
    """Whether to enable room randomization which will randomize the order of all levels."""
    display_name = "Room Randomisation"
    default = True


class Lumsanity(Toggle):
    """Whether all individual yellow lums should be their own checks instead of only super lums. This will add 710 extra progression checks!"""
    display_name = "Lumsanity"
    default = False


class InstantPortalAccess(Toggle):
    """Whether all portals should be accessible as soon as you obtain enough lums. Will speed up the game considerably."""
    display_name = "Instant Portal Access"
    default = False


class FixedLevelLengths(Toggle):
    """Whether to use fixed level lengths with room randomisation, which ensures every level has as many rooms as it does in the base game. This is more likely to cause generation failures with high lum gates as early levels in the base game don't have many rooms."""
    display_name = "Fixed Level Lengths"
    default = False


class FirstGateRequirement(Range):
    """The amount of lums required to enter the Sanctuary of Water and Ice."""
    display_name = "First Lum Gate Requirement"
    range_start = 0
    range_end = 200
    default = 100


class SecondGateRequirement(Range):
    """The amount of lums required to enter the Sanctuary of Stone & Fire."""
    display_name = "Second Lum Gate Requirement"
    range_start = 0
    range_end = 450
    default = 300


class ThirdGateRequirement(Range):
    """The amount of lums required to enter Beneath the Sanctuary of Rock & Lava."""
    display_name = "Third Lum Gate Requirement"
    range_start = 0
    range_end = 600
    default = 450


class FourthGateRequirement(Range):
    """The amount of lums required to enter the Iron Mountains."""
    display_name = "Fourth Lum Gate Requirement"
    range_start = 0
    range_end = 800
    default = 550


class WalkOfLifeRequirement(Range):
    """The amount of lums required to enter the Walk of Life."""
    display_name = "Walk of Life Lum Requirement"
    range_start = 0
    range_end = 750
    default = 60


class WalkOfPowerRequirement(Range):
    """The amount of lums required to enter the Walk of Power."""
    display_name = "Walk of Power Lum Requirement"
    range_start = 0
    range_end = 750
    default = 475


@dataclass
class Rayman2Options(PerGameCommonOptions):
    end_goal: EndGoal
    death_link: DeathLink

    room_randomisation: RoomRandomisation
    lumsanity: Lumsanity

    instant_portal_access: InstantPortalAccess
    fixed_level_lengths: FixedLevelLengths

    first_gate_required: FirstGateRequirement
    second_gate_required: SecondGateRequirement
    third_gate_required: ThirdGateRequirement
    fourth_gate_required: FourthGateRequirement
    walk_of_life_required: WalkOfLifeRequirement
    walk_of_power_required: WalkOfPowerRequirement


def create_option_groups() -> List[OptionGroup]:
    return [
        OptionGroup(name="Lum Requirement Options",
                    options=[WalkOfLifeRequirement, FirstGateRequirement, SecondGateRequirement, WalkOfPowerRequirement,
                             ThirdGateRequirement, FourthGateRequirement])
    ]
