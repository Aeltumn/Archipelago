from dataclasses import dataclass, field
from typing import Dict, List


# This file contains the full game layout, defining all levels, which sub-levels they have,
# which ids everything uses, and all items contained within. This layout object is used by
# init.py to generate the items, locations, and regions.
@dataclass
class SubLevelInfo:
    regularLums: List[int] = field(default_factory=lambda: [])
    superLums: List[int] = field(default_factory=lambda: [])
    cages: List[int] = field(default_factory=lambda: [])
    special: List[int] = field(default_factory=lambda: [])
    lumGate: bool = False
    hasExitPortal: bool = False
    needsPurpleLum: bool = False


@dataclass
class LevelInfo:
    displayName: str
    sublevels: Dict[str, SubLevelInfo]
    extra: str = None

human_readable_names: Dict[int, str] = {
    # Woods of Light
    # learn_10
    840: "Cage above wooden grate",
    1399: "Lum from cage above wooden grate",
    1396: "Lum above Murfy stone",
    1398: "Lum on grass next to waterfall",
    1400: "Lum underneath waterfal",
    1397: "Lum between stone walls",
    841: "Cage with Teensies",

    # The Fairy Glade
    # Learn_30
    7: "Lum above mushroom",
    8: "Lum on tree branch",
    843: "Cage on tree branch",
    12: "Lum in cage on tree branch",
    842: "Underwater cage",
    1: "Super lum in underwater cage",
    6: "Lum under bridge",
    # learn_31
    11: "Lum on vines",
    # learn_31 (revisit)
    844: "Cage inside fort",
    9: "Lum in cage inside fort #1",
    10: "Lum in cage inside fort #2",
    # bast_20
    27: "Lum on lily pad #1",
    26: "Lum on lily pad #2",
    25: "Lum on lily pad #3",
    29: "Lum on rope ladder",
    28: "Lum at top of waterfall climb area",
    845: "Cage at top of waterfall climb area",
    13: "Super lum in cage at top of waterfall climb area",
    846: "Cage inside jail",
    18: "Super lum in cage inside jail",
    23: "Lum on ceiling ropes #1",
    24: "Lum on ceiling ropes #2",
    # bast_22
    31: "Lum on climbable rope #1",
    30: "Lum on climbable rope #2",
    1095: "Silver Lum from Ly",
    32: "Lum between metal pipes #1",
    33: "Lum between metal pipes #2",
    # learn_60
    34: "Floating lum #1",
    35: "Floating lum #2",
    36: "Lum on highest metal pipe",
    37: "Lum on second highest metal pipe",
    847: "Cage next to pirate",
    48: "Lum in cage next to pirate #1",
    49: "Lum in cage next to pirate #2",
    50: "Lum in cage next to pirate #2",
    38: "Lum in first wind vortex",
    42: "Lum in second wind vortex",
    45: "Lum in third wind vortex",
    44: "Lower lum in thin wind vortex",
    43: "Upper lum in thin wind vortex",
    39: "Lum in fourth wind vortex",
    46: "Lum in fifth wind vortex",
    47: "Lower lum in small wind vortex",
    41: "Upper lum in small wind vortex",
    40: "Lum in final wind vortex",
    848: "Cage with Teensie",

    # The Marshes of Awakening
    # Ski_10
    76: "Lum before Jano's cave",
    852: "Cage with Ssssam",
    66: "Super lum on Lever",
    80: "Lum near Zombie Chickens #1",
    78: "Lum near Zombie Chickens #2",
    77: "Lum near Zombie Chickens #3",
    79: "Lum near Zombie Chickens #4",
    849: "Cage around big tree #1",
    850: "Cage around big tree #2",
    851: "Cage around big tree #3",
    81: "Super lum in cage around big tree #1",
    86: "Super lum in cage around big tree #2",
    91: "Super lum in cage around big tree #3",
    # ski_60
    59: "Lum on wooden bridge #1",
    60: "Lum on wooden bridge #2",
    71: "Super lum behind group of bombs",
    61: "Super lum on wood pillar",
    56: "Lum floating abvove rock #1",
    58: "Lum floating abvove rock #2",
    57: "Lum floating abvove rock #3",
    51: "Super lum on fishing rod",
    96: "Super lum behind single bomb",
    853: "Cage with Teensie"
}

extra_levels: Dict[str, LevelInfo] = {
}

levels: Dict[str, LevelInfo] = {
    "learn_10": LevelInfo(
        "The Woods of Light",
        {
            "jail_20": SubLevelInfo(),
            "learn_10": SubLevelInfo(
                regularLums=[
                    1396,
                    1397,
                    1398,
                    1399,
                    1400
                ],
                cages=[
                    840,
                    841,
                ],
                hasExitPortal=True,
            )
        }
    ),
    "Learn_30": LevelInfo(
        "The Fairy Glade",
        {
            "Learn_30": SubLevelInfo(
                regularLums=[
                    6,
                    7,
                    8,
                    12,
                ],
                superLums=[
                    1,
                ],
                cages=[
                    842,
                    843,
                ],
            ),
            "learn_31": SubLevelInfo(
                regularLums=[
                    11,
                    9, # requires revisit
                    10 # requires revisit
                ],
                cages=[
                    844 # requires revisit
                ],
            ),
            "bast_20": SubLevelInfo(
                regularLums=[
                    27,
                    26,
                    25,
                    29,
                    28,
                    23,
                    24
                ],
                superLums=[
                    13,
                    18
                ],
                cages=[
                    845,
                    846
                ],
            ),
            "bast_22": SubLevelInfo(
                regularLums=[
                    31,
                    30,
                    32, # requires purple
                    33 # requires purple
                ],
                special=[
                    1095
                ],
                needsPurpleLum=True,
            ),
            "learn_60": SubLevelInfo(
                regularLums=[
                    34,
                    35,
                    36,
                    37,
                    48,
                    49,
                    50,
                    38,
                    42,
                    45,
                    44,
                    43,
                    39,
                    46,
                    47,
                    41,
                    40
                ],
                cages=[
                    847,
                    848
                ],
                hasExitPortal=True,
            ),
        }
    ),
    "Ski_10": LevelInfo(
        "The Marshes of Awakening",
        {
            "Ski_10": SubLevelInfo(
                regularLums=[
                    76,
                    77,
                    78,
                    79,
                    80
                ],
                superLums=[
                    66,
                    81,
                    86,
                    91
                ],
                cages=[
                    852,
                    849,
                    850,
                    851
                ],
            ),
            "ski_60": SubLevelInfo(
                regularLums=[
                    59,
                    60,
                    56,
                    58,
                    57
                ],
                superLums=[
                    71,
                    61,
                    51,
                    96
                ],
                cages=[
                    853
                ],
                hasExitPortal=True,
            ),
        }
    )
}
