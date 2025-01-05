from typing import List
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Range, DeathLink

class FirstLumDoorMin(Range):
    """The lowest possible required yellow lums to pass the first lum requirement. This will be the amount you are required to obtain in the first 4 levels."""
    display_name = "Lowest First Lum Requirement"
    range_start = 0
    range_end = 300
    default = 50

class FirstLumDoorMax(Range):
    """The highest possible required yellow lums to pass the first lum requirement. This will be the amount you are required to obtain in the first 4 levels."""
    display_name = "Highest First Lum Requirement"
    range_start = 0
    range_end = 300
    default = 200

class SecondLumDoorMin(Range):
    """The lowest possible required yellow lums to pass the second lum requirement. This will be the amount you are required to obtain in the first 8 levels."""
    display_name = "Lowest Second Lum Requirement"
    range_start = 0
    range_end = 550
    default = 200


class SecondLumDoorMax(Range):
    """The highest possible required yellow lums to pass the second lum requirement. This will be the amount you are required to obtain in the first 8 levels."""
    display_name = "Highest Second Lum Requirement"
    range_start = 0
    range_end = 550
    default = 400

class ThirdLumDoorMin(Range):
    """The lowest possible required yellow lums to pass the third lum requirement. This will be the amount you are required to obtain in the first 13 levels."""
    display_name = "Lowest Third Lum Requirement"
    range_start = 0
    range_end = 800
    default = 375

class ThirdLumDoorMax(Range):
    """The highest possible required yellow lums to pass the third lum requirement. This will be the amount you are required to obtain in the first 13 levels."""
    display_name = "Highest Third Lum Requirement"
    range_start = 0
    range_end = 800
    default = 475

class FourthLumDoorMin(Range):
    """The lowest possible required yellow lums to pass the fourth lum requirement. This will be the amount you are required to obtain in the first 15 levels."""
    display_name = "Lowest Fourth Lum Requirement"
    range_start = 0
    range_end = 900
    default = 450

class FourthLumDoorMax(Range):
    """The highest possible required yellow lums to pass the fourth lum requirement. This will be the amount you are required to obtain in the first 15 levels."""
    display_name = "Highest Fourth Lum Requirement"
    range_start = 0
    range_end = 900
    default = 650

@dataclass
class Rayman2Options(PerGameCommonOptions):
    first_lum_min:          FirstLumDoorMin
    first_lum_max:          FirstLumDoorMax
    second_lum_min:         SecondLumDoorMin
    second_lum_max:         SecondLumDoorMax
    third_lum_min:          ThirdLumDoorMin
    third_lum_max:          ThirdLumDoorMax
    fourth_lum_min:         FourthLumDoorMin
    fourth_lum_max:         FourthLumDoorMax

    death_link:             DeathLink

def create_option_groups() -> List[OptionGroup]:
    return [
        OptionGroup(name="Lum Requirement Options", options=[FirstLumDoorMin, FirstLumDoorMax, SecondLumDoorMin, SecondLumDoorMax, ThirdLumDoorMin, ThirdLumDoorMax, FourthLumDoorMin, FourthLumDoorMax])
    ]

def adjust_options(world: "Rayman2World"):
    if world.options.FirstLumDoorMax < world.options.FirstLumDoorMin:
        world.options.FirstLumDoorMax.value, world.options.FirstLumDoorMin.value = \
         world.options.FirstLumDoorMin.value, world.options.FirstLumDoorMax.value

    if world.options.SecondLumDoorMax < world.options.SecondLumDoorMin:
        world.options.SecondLumDoorMax.value, world.options.SecondLumDoorMin.value = \
         world.options.SecondLumDoorMin.value, world.options.SecondLumDoorMax.value
    
    if world.options.ThirdLumDoorMax < world.options.ThirdLumDoorMin:
        world.options.ThirdLumDoorMax.value, world.options.ThirdLumDoorMin.value = \
         world.options.ThirdLumDoorMin.value, world.options.ThirdLumDoorMax.value

    if world.options.FourthLumDoorMax < world.options.FourthLumDoorMin:
        world.options.FourthLumDoorMax.value, world.options.FourthLumDoorMin.value = \
         world.options.FourthLumDoorMin.value, world.options.FourthLumDoorMax.value