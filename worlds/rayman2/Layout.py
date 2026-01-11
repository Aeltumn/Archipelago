from dataclasses import dataclass, field
from typing import Dict, List
from enum import IntEnum

# This file contains the full game layout, defining all levels, which sub-levels they have,
# which ids everything uses, and all items contained within. This layout object is used by
# init.py to generate the items, locations, and regions.
class Connection(IntEnum):
    """The types of connections between rooms."""
    ENTRY_PORTAL = 0
    INTERNAL = 1
    EXIT_PORTAL = 2

class Tech(IntEnum):
    """The types of tech required to accomplish something."""
    NONE = 0
    PURPLE_SWING = 1
    EARLY_ECHOING_CAVES_OR_REVISIT = 2
    BAYOU_DAMAGE_BOOST = 3
    PURPLE_SWING_OR_BACKWARDS_JUMP = 4
    ELIXIR_AND_PURPLE_SWING = 5

@dataclass
class Checks:
    regularLums: List[int] = field(default_factory=list)
    superLums: List[int] = field(default_factory=list)
    cages: List[int] = field(default_factory=list)
    special: Dict[int, str] = field(default_factory=dict)

@dataclass
class SubLevelInfo:
    checks: Checks = field(default_factory=lambda: Checks())
    exitRequirement: Tech = Tech.NONE
    behindRequirements: Dict[Tech, Checks] = field(default_factory=dict)

@dataclass
class LevelInfo:
    displayName: str
    sublevels: Dict[str, SubLevelInfo]

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
    
    # The Sanctuary of Water and Ice
    # water_10
    862: "Cage on pier",
    156: "Lum in cage on pier #1",
    157: "Lum in cage on pier #2",
    158: "Lum in cage on pier #3",
    166: "Lum on slope #1",
    167: "Lum on slope #2",
    168: "Lum on slope #3",
    169: "Lum on slope #4",
    170: "Lum on slope #5",
    171: "Lum before cave pool",
    172: "Super lum in pool tunnel",
    178: "Lum in pool tunnel #1",
    177: "Lum in pool tunnel #2",
    861: "Cage in cave",
    151: "Lum in cage in cave #1",
    152: "Lum in cage in cave #2",
    153: "Lum in cage in cave #3",
    154: "Lum on ladder #1",
    155: "Lum on ladder #2",
    159: "Lum on ladder #3",
    160: "Lum on ladder #4",
    161: "Super lum near barrel",
    180: "Lum between balconies",
    182: "Lum on balcony #1",
    183: "Lum on balcony #2",
    181: "Lum on balcony #3",
    184: "Lum on balcony #4",
    186: "Lum on balcony #5",
    187: "Lum on balcony #6",
    185: "Lum on balcony #7",
    188: "Lum on balcony #8",
    189: "Lum on balcony #9",
    179: "Lum on balcony #10",
    190: "Lum on balcony #11",
    # water_20
    197: "Lum on first jump of slide",
    199: "Lum on right side of slide",
    193: "Lum in centre of slide #1",
    194: "Lum in centre of slide #2",
    195: "Lum in centre of slide #3",
    198: "Lum on midway jump of slide",
    196: "Lum on final jump of slide #1",
    191: "Lum on final jump of slide #2",
    192: "Lum on final jump of slide #3",
    200: "Lum above waterfall",
    1112: "Water Mask of Polokus",
    
    # The Menhir Hills
    # rodeo_10
    864: "Cage in hole",
    206: "Super lum in cage in hole",
    865: "Cage behind bandage",
    201: "Super lum in cage behind bandage",
    863: "Cage behind pirate door",
    211: "Super lum in cage behind pirate door",    
    # rodeo_40
    226: "Lum behind tree",
    227: "Lum on platform after purple lum",
    868: "Cage across platform after purple lum",
    219: "Lum in cage across platform after purple lum #1",
    220: "Lum in cage across platform after purple lum #2",
    221: "Lum in cage across platform after purple lum #3",
    224: "Lum on start of shell ride #1",
    223: "Lum on start of shell ride #2",
    225: "Lum on start of shell ride #3",
    231: "Lum on boardwark during shell ride",
    228: "Lum on midway point of shell ride #1",
    222: "Lum on midway point of shell ride #2",
    233: "Lum on midway point of shell ride #3",
    232: "Lum on midway point of shell ride #4",
    230: "Lum on final turn of shell ride #1",
    235: "Lum on final turn of shell ride #2",
    234: "Lum on final turn of shell ride #3",
    229: "Lum after bandage",
    866: "Cage after flying barrel",
    216: "Lum in cage after flying barrel #1",
    217: "Lum in cage after flying barrel #2",
    218: "Lum in cage after flying barrel #3",  
    867: "Cage after purple lums",
    236: "Lum in cage after purple lums #1",
    237: "Lum in cage after purple lums #2",
    238: "Lum in cage after purple lums #3",    
    # rodeo_60
    870: "Cage after purple lum swing",
    241: "Lum in cage after purple lum swing #1",
    242: "Lum in cage after purple lum swing #2",
    246: "Lum on vine behind shell #1",
    245: "Lum on vine behind shell #2",
    869: "Cage near vine behind shell",
    239: "Lum in cage near vine behind shell #1",
    240: "Lum in cage near vine behind shell #2",
    243: "Lum on start of shell ride #1",
    244: "Lum on start of shell ride #2",
    248: "Lum on start of shell ride #3",
    247: "Lum on start of shell ride #4",
    249: "Lum on boardwalk during shell ride #1",
    250: "Lum on boardwalk during shell ride #2",    
    # The Cave of Bad Dreams
    # vulca_10
    751: "Lum on skeleton at start",
    752: "Lum on bone wall at start",
    753: "Lum after first skeleton arm",
    754: "Lum on bone wall after purple swing",
    755: "Lum on bridge",
    756: "Lum between skeleton arms",
    757: "Lum before climbing wall",
    758: "Lum between climbing wall",
    759: "Lum near mini-janos #1",
    760: "Lum near mini-janos #2",
    761: "Lum near mini-janos #3",
    762: "Super lum after sphere trapdoor",
    769: "Lum on blue sphere path #1",
    768: "Lum on blue sphere path #2",
    767: "Lum on blue sphere path #3",
    770: "Lum on orange sphere path #1",
    771: "Lum on orange sphere path #2",
    772: "Lum on orange sphere path #3",
    773: "Lum on orange sphere path #4",
    774: "Lum on orange sphere path #5",
    775: "Lum on orange sphere path #6",
    776: "Super lum after sphere gate",
    # vulca_20
    781: "Super lum on slide #1",
    786: "Super lum on slide #2",
    791: "Super lum on slide #3",
    796: "Super lum on platform",
    1120: "Elixir of Life",
    # The above could be 1123, both happened at the same time, need to check
}

extra_levels: list[LevelInfo] = [
]

levels: list[LevelInfo] = [
    LevelInfo(
        "The Woods of Light",
        {
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
            )
        }
    ),
    LevelInfo(
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
                    ),
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
                        1095: "Silver Lum",
                    },
                ),
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        regularLums=[
                            32,
                            33
                        ]
                    ),
                },
                exitRequirement=Tech.PURPLE_SWING
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
            ),
        }
    ),
    LevelInfo(
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
            ),
        }
    ),
    LevelInfo(
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
                    ),
                },
                exitRequirement=Tech.BAYOU_DAMAGE_BOOST
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
                    ),
                },
                exitRequirement=Tech.PURPLE_SWING,
            )
        }
    ),
    LevelInfo(
        "The Sanctuary of Water and Ice",
        {
            "water_10": SubLevelInfo(
                checks=Checks(
                    cages=[
                        862,
                        861
                    ],
                    regularLums=[
                        156,
                        157,
                        158,
                        166,
                        167,
                        168,
                        169,
                        170,
                        171,
                        178,
                        177,
                        151,
                        152,
                        153,
                        154,
                        155,
                        159,
                        160,
                        180,
                        181,
                        184,
                        186,
                        187,
                        185,
                        188,
                        189,
                        179,
                        190
                    ],
                    superLums=[
                        172,
                        161
                    ]
                )  
            ),
            "water_20": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        197,
                        199,
                        193,
                        194,
                        195,
                        198,
                        196,
                        191,
                        192,                   
                    ]
                ),
                behindRequirements={
                    Tech.PURPLE_SWING_OR_BACKWARDS_JUMP: Checks(
                        regularLums=[
                            200
                        ],
                        special=[
                            1112: "Water Mask",
                        ]
                    ),
                },
                exitRequirement=Tech.PURPLE_SWING_OR_BACKWARDS_JUMP
            )
        },
    ),
    LevelInfo(
        "The Menhir Hills",
        {
            "rodeo_10": SubLevelInfo(
                checks=Checks(
                    cages=[
                        864,
                        865,
                        863
                    ],
                    superLums=[
                        206,
                        201,
                        211
                    ]
                )  
            ),
            "rodeo_40": SubLevelInfo(
                checks=Checks(
                    cages=[
                        866,
                        867
                    ],
                    regularLums=[
                        226,
                        224,
                        223,
                        225,
                        231,
                        228,
                        222,
                        233,
                        232,
                        230,
                        235,
                        234,
                        229,
                        216,
                        217,
                        218,
                        236,
                        237,
                        238
                    ]
                ),
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        regularLums=[
                            227,
                            219,
                            220,
                            221                            
                        ],
                        cages=[
                            868
                        ]
                    ),
                    Tech.ELIXIR_AND_PURPLE_SWING: Checks(
                        regularLums=[
                            236,
                            237,
                            238
                        ],
                        cages=[
                            867
                        ]
                    ),
                },
                exitRequirement=Tech.ELIXIR_AND_PURPLE_SWING               
            ),
            "rodeo_60": SubLevelInfo(
                checks=Checks(
                    cages=[
                        869
                    ],
                    regularLums=[
                        246,
                        245,
                        239,
                        240,
                        243,
                        244,
                        248,
                        247,
                        249,
                        250
                    ]
                ),
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        regularLums=[
                            241,
                            242
                        ],
                        cages=[
                            870
                        ]
                    ),
                },
            )
        },
    ),
    LevelInfo(
        "The Cave of Bad Dreams",
        {
            "vulca_10": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        751,
                        752,
                        753
                    ]                    
                ),
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        regularLums=[
                            754,
                            755,
                            756,
                            757,
                            758,
                            759,
                            760,
                            761,
                            769,
                            768,
                            767,
                            770,
                            771,
                            772,
                            773,
                            774,
                            775                            
                        ],
                        superLums=[
                            762,
                            776
                        ]
                    ),
                },
                exitRequirement=Tech.PURPLE_SWING
            ),
            "vulca_20": SubLevelInfo(
                checks=Checks(
                    superLums=[
                        781,
                        786,
                        791,
                        796
                    ],
                    special=[
                        1113: "Elixir of Life",
                    ]
                ),
            )
        }
    ),
    # Added so EEC doesn't crash
    LevelInfo(
        "The Echoing Caves",
        {
            "Cask_10": SubLevelInfo()
        }
    )
]
