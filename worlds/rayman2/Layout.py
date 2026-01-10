from dataclasses import dataclass, field
from typing import Dict, List
from enum import Enum

# This file contains the full game layout, defining all levels, which sub-levels they have,
# which ids everything uses, and all items contained within. This layout object is used by
# init.py to generate the items, locations, and regions.
class Tech(Enum):
    """The types of tech required to accomplish something."""
    PURPLE_SWING = 1
    EARLY_ECHOING_CAVES_OR_REVISIT = 2
    BAYOU_DAMAGE_BOOST = 3

@dataclass
class Checks:
    regularLums: List[int] = field(default_factory=lambda: [])
    superLums: List[int] = field(default_factory=lambda: [])
    cages: List[int] = field(default_factory=lambda: [])
    special: Dict[int, str] = field(default_factory=lambda: {})

@dataclass
class SubLevelInfo:
    checks: Checks = Checks()
    exitRequirements: List[Tech] = field(default_factory=lambda: [])
    behindRequirements: Dict[Tech, Checks] = field(default_factory=lambda: {}),
    lumGate: bool = False
    hasExitPortal: bool = False


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
    853: "Cage with Teensie",

    # The Bayou
    # chase_10
    854: "Cage on mossy tree branch",
    122: "Lum in cage on mossy tree branch #1",
    123: "Lum in cage on mossy tree branch #2",
    101: "Lum inside hollow tree #1",
    102: "Lum inside hollow tree #2",
    103: "Lum inside hollow tree #3",
    120: "Lum floating at big switch jump #1",
    121: "Lum floating at big switch jump #2",
    128: "Lum on unstable bridge #1",
    129: "Lum on unstable bridge #2",
    130: "Lum on unstable bridge #3",
    131: "Lum on unstable bridge #4",
    856: "Cage above sleeping pirate",
    104: "Lum on river #1",
    105: "Lum on river #2",
    106: "Lum on river #3",
    107: "Lum on river #4",
    108: "Lum on river #5",
    855: "Cage under mossy tree branch",
    118: "Lum in cage under mossy tree branch #1",
    119: "Lum in cage under mossy tree branch #2",
    109: "Lum in air over checkpoint bridge #1",
    110: "Lum in air over checkpoint bridge #2",
    111: "Lum in air over checkpoint bridge #3",
    135: "Lum in air over checkpoint bridge #4",
    124: "Lums arcing around corner #1",
    125: "Lums arcing around corner #2",
    126: "Lums arcing around corner #3",
    127: "Lums arcing around corner #4",
    857: "Cage in hollow tree",
    132: "Lum in cage in hollow tree #1",
    133: "Lum in cage in hollow tree #2",
    134: "Lum in cage in hollow tree #3",
    114: "Lum on bridges blown up by bombs #1",
    115: "Lum on bridges blown up by bombs #2",
    116: "Lum on bridges blown up by bombs #3",
    117: "Lum on bridges blown up by bombs #4",
    858: "Cage under wooden platform",
    112: "Lum in cage under wooden platform #1",
    113: "Lum in cage under wooden platform #2",
    # chase_22
    137: "Lum above piranha",
    144: "Lum on ground behind piranha #1",
    145: "Lum on ground behind piranha #2",
    146: "Lum on rolling barrel platform #1",
    147: "Lum on rolling barrel platform #2",
    148: "Lum on rolling barrel platform #3",
    149: "Lum next to switch",
    150: "Lum floating in front of spooky tree",
    859: "Cage next to falling barrels",
    136: "Lum in cage next to falling barrels",
    138: "Lum above trampoline #1",
    139: "Lum above trampoline #2",
    140: "Lum above trampoline #3",
    141: "Lum above trampoline #4",
    142: "Lum above trampoline #5",
    143: "Lum above trampoline #6",
    860: "Cage with Teensie",
}

extra_levels: Dict[str, LevelInfo] = {
}

levels: Dict[str, LevelInfo] = {
    "learn_10": LevelInfo(
        "The Woods of Light",
        {
            "jail_20": SubLevelInfo(),
            "learn_10": SubLevelInfo(
                checks=Checks(
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
                    ]
                ),
                hasExitPortal=True,
            )
        }
    ),
    "Learn_30": LevelInfo(
        "The Fairy Glade",
        {
            "Learn_30": SubLevelInfo(
                checks=Checks(
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
                    ]
                )
            ),
            "learn_31": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        11
                    ]
                ),
                behindRequirements={
                    Tech.EARLY_ECHOING_CAVES_OR_REVISIT: Checks(
                        regularLums=[
                            9,
                            10
                        ],
                        cages=[
                            844
                        ]
                    )
                }
            ),
            "bast_20": SubLevelInfo(
                checks=Checks(
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
                    ]
                ),
            ),
            "bast_22": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        31,
                        30                        
                    ],
                    special={
                        1095: "Silver Lum"
                    },
                ),
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        regularLums=[
                            32,
                            33
                        ]
                    )
                },
                exitRequirements=[
                    Tech.PURPLE_SWING
                ]
            ),
            "learn_60": SubLevelInfo(
                checks=Checks(
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
                    ]
                ),
                hasExitPortal=True,
            ),
        }
    ),
    "Ski_10": LevelInfo(
        "The Marshes of Awakening",
        {
            "Ski_10": SubLevelInfo(
                checks=Checks(
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
                    ]
                )
            ),
            "ski_60": SubLevelInfo(
                checks=Checks(
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
                    ]
                ),
                hasExitPortal=True,
            ),
        }
    ),
    "chase_10": LevelInfo(
        "The Bayou",
        {
            "chase_10": SubLevelInfo(
                checks=Checks(
                    cages=[
                        854,
                        856,
                    ],
                    regularLums=[
                        122,
                        123,
                        101,
                        102,
                        103,
                        120,
                        121,
                        128,
                        129,
                        130,
                        131,
                    ]
                ),
                behindRequirements={
                    Tech.BAYOU_DAMAGE_BOOST: Checks(
                        cages=[
                            855,
                            858
                        ],
                        regularLums=[
                            104,
                            105,
                            106,
                            107,
                            108,
                            118,
                            119,
                            109,
                            110,
                            111,
                            135,
                            124,
                            125,
                            126,
                            127,
                            114,
                            115,
                            116,
                            117,
                            112,
                            113
                        ]
                    ),
                    Tech.PURPLE_SWING: Checks(
                        cages=[
                            857
                        ],
                        regularLums=[
                            132,
                            133,
                            134
                        ]
                    )
                },
                exitRequirements=[
                    Tech.BAYOU_DAMAGE_BOOST
                ]
            ),
            "chase_22": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        137,
                        144,
                        145,
                        146,
                        147,
                        148,
                        149
                    ]
                ),
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        regularLums=[
                            150,
                            136,
                            138,
                            139,
                            140,
                            141,
                            142,
                            143
                        ],
                        cages=[
                            859,
                            860
                        ]
                    )
                },
                exitRequirements=[
                    Tech.PURPLE_SWING,
                ],
                hasExitPortal=True
            )
        }
    )
}
