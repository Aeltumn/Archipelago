from dataclasses import dataclass
from typing import List

from Options import Range, DeathLink, DefaultOnToggle, Choice, OptionGroup, T
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

    def get_option_name(cls, value: T) -> str:
        if value == "option_crows_nest":
            return "Crow's Nest"
        elif value == "option_treasure":
            return "Treasure%"
        else:
            return "100%"


class ShuffleRooms(DefaultOnToggle):
    """Whether rooms should be shuffled as well, if disabled only levels are shuffled."""
    display_name = "Shuffle Rooms"


class FirstMaskRequirement(Range):
    """The percentage of available lums required for the first mask level."""
    display_name = "First Mask Lum Requirement Percentage"
    range_start = 0
    range_end = 100
    default = 33  # Base game requires 100 out of 300


class SecondMaskRequirement(Range):
    """The percentage of available lums required for the second mask level."""
    display_name = "Second Mask Lum Requirement Percentage"
    range_start = 0
    range_end = 100
    default = 50  # Base game requires 300 out of 550


class ThirdMaskRequirement(Range):
    """The percentage of available lums required for the third mask level."""
    display_name = "Third Mask Lum Requirement Percentage"
    range_start = 0
    range_end = 100
    default = 60  # Base game requires 475 out of 800


class FourthMaskRequirement(Range):
    """The percentage of available lums required for the fourth mask level."""
    display_name = "Fourth Mask Lum Requirement Percentage"
    range_start = 0
    range_end = 100
    default = 60  # Base game requires 550 out of 900


class WalkOfLifeRequirement(Range):
    """The percentage of available lums required to unlock the extra level in The Bayou."""
    display_name = "Walk of Life Lum Requirement Percentage"
    range_start = 0
    range_end = 100
    default = 20  # Base game requires 60 out of 300


class WalkOfPowerRequirement(Range):
    """The percentage of available lums required to unlock the extra level in The Sanctuary of Rock and Lava."""
    display_name = "Walk of Power Lum Requirement Percentage"
    range_start = 0
    range_end = 100
    default = 55  # Base game requires 450 out of 800


@dataclass
class Rayman2Options(PerGameCommonOptions):
    first_mask_required: FirstMaskRequirement
    second_mask_required: SecondMaskRequirement
    third_mask_required: ThirdMaskRequirement
    fourth_mask_required: FourthMaskRequirement
    walk_of_life_required: WalkOfLifeRequirement
    walk_of_power_required: WalkOfPowerRequirement

    end_goal: EndGoal
    shuffle_rooms: ShuffleRooms
    death_link: DeathLink


def create_option_groups() -> List[OptionGroup]:
    return [
        OptionGroup(name="Lum Requirement Options",
                    options=[FirstMaskRequirement, WalkOfLifeRequirement, SecondMaskRequirement, WalkOfPowerRequirement, ThirdMaskRequirement, FourthMaskRequirement])
    ]
