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
    NOT_RANDOM = 2

class Tech(IntEnum):
    """The types of tech required to accomplish something."""
    NONE = 0
    PURPLE_SWING = 1
    BAYOU_DAMAGE_BOOST = 2
    PURPLE_SWING_OR_BACKWARDS_JUMP = 3
    ELIXIR_AND_PURPLE_SWING = 4
    PURPLE_SWING_OR_GLM = 5
    HAS_REENTERED_FROM_THAT_ONE_SPECIFIC_EXIT = 6

@dataclass
class Checks:
    regularLums: List[int] = field(default_factory=list)
    superLums: List[int] = field(default_factory=list)
    cages: List[int] = field(default_factory=list)
    special: Dict[int, str] = field(default_factory=dict)

    def total(self, lumsanity: bool) -> int:
        """Returns the total amount of checks in this segment."""
        count = 0
        if lumsanity:
            count += len(self.regularLums)
        count += len(self.superLums)
        count += len(self.cages)
        count += len(self.special)
        return count

@dataclass
class SubLevelInfo:
    checks: Checks = field(default_factory=lambda: Checks())
    exitRequirement: Tech = Tech.NONE
    behindRequirements: Dict[Tech, Checks] = field(default_factory=dict)

@dataclass
class LevelInfo:
    displayName: str
    sublevels: Dict[str, SubLevelInfo]
    lumGate: int | None = None
    requireAllMasks: bool = False

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
    50: "Lum in cage next to pirate #3",
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
    
    # The Walk of Life
    # Ly_10
    1201: "Lum in time race #1",
    1202: "Lum in time race #2",
    1203: "Lum in time race #3",
    1236: "Lum in time race #4",
    1206: "Lum in time race #5",
    1205: "Lum in time race #6",
    1208: "Lum in time race #7",
    1210: "Lum in time race #8",
    1212: "Lum in time race #9",
    1209: "Lum in time race #10",
    1214: "Lum in time race #11",
    1211: "Lum in time race #12",
    1215: "Lum in time race #13",
    1217: "Lum in time race #14",
    1216: "Lum in time race #15",
    1218: "Lum in time race #16",
    1219: "Lum in time race #17",
    1220: "Lum in time race #18",
    1221: "Lum in time race #19",
    1222: "Lum in time race #20",
    1223: "Lum in time race #21",
    1224: "Lum in time race #22",
    1225: "Lum in time race #23",
    1226: "Lum in time race #24",
    1227: "Lum in time race #25",
    1229: "Lum in time race #26",
    1230: "Lum in time race #27",
    1231: "Lum in time race #28",
    1233: "Lum in time race #29",
    1244: "Lum in time race #30",
    1246: "Lum in time race #31",
    1242: "Lum in time race #32",
    1232: "Lum in time race #33",
    1243: "Lum in time race #34",
    1238: "Lum in time race #35",
    1239: "Lum in time race #36",
    1240: "Lum in time race #37",
    1245: "Lum in time race #38",
    1247: "Lum in time race #39",
    1237: "Lum in time race #40",
    1234: "Lum in time race #41",
    1228: "Lum in time race #42",
    1207: "Lum in time race #43",
    1235: "Lum in time race #44",
    1241: "Lum in time race #45",
    1249: "Lum in time race #46",
    1213: "Lum in time race #47",
    1250: "Lum in time race #48",
    1248: "Lum in time race #49",
    1204: "Lum in time race #50",
    
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
    1101: "Knowledge of the Cave of Bad Dreams",
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
    1123: "Elixir of Life",
    
    # The Canopy
    # glob_30
    266: "Lum on spiderweb #1",
    251: "Lum on spiderweb #2",
    262: "Lum on spiderweb #3",
    252: "Lum on spiderweb #4",
    253: "Lum on spiderweb #5",
    254: "Lum on spiderweb #6",
    263: "Lum on spiderweb #7",
    258: "Lum on spiderweb #8",
    264: "Lum on spiderweb #9",
    259: "Lum on spiderweb #10",
    255: "Lum on spiderweb #11",
    265: "Lum on spiderweb #12",
    256: "Lum on spiderweb #13",
    261: "Lum on spiderweb #14",
    260: "Lum on spiderweb #15",
    257: "Lum on spiderweb #16",
    871: "Cage beneath red lum",
    267: "Lum in cage beneath red lum #1",
    268: "Lum in cage beneath red lum #2",
    872: "Cage over gap",
    269: "Lum in cage over gap #1",
    270: "Lum in cage over gap #2",
    # glob_10
    283: "Lum on bridge",
    276: "Lum next to laser barrier",
    275: "Lum on mushroom",
    271: "Lum in midair near bridge",
    274: "Lum near pirate",
    281: "Lum midair after laser barrier",
    285: "Lum next to tall mushroom",
    280: "Lum next to platform sprout #1",
    284: "Lum next to platform sprout #2",
    282: "Lum on edge near gap",
    277: "Lum above platform sprout",
    273: "Lum over gap #1",
    272: "Lum over gap #2",
    279: "Lum near pillar",
    278: "Lum near fire",
    1143: "Silver Lum from Globox",
    # glob_20
    286: "Lum collected in cutscene",
    291: "Lum beneath firing ship",
    290: "Lum after laser barrier",
    287: "Lum around bush #1",
    288: "Lum around bush #2",
    289: "Lum around bush #3",
    874: "Cage hanging from mushroom",
    297: "Lum in cage hanging from mushroom #1",
    298: "Lum in cage hanging from mushroom #2",
    292: "Super lum above security door",
    873: "Cage with teensies",
    299: "Lum in cage with teensies #1",
    300: "Lum in cage with teensies #2",
    
    # Whale Bay
    # whale_00
    339: "Lum underwater in chest",
    341: "Lum underneath rope #1",
    327: "Lum underneath rope #2",
    320: "Lum underneath rope #3",
    323: "Lum underneath rope #4",
    321: "Lum above rolling barrels #1",
    326: "Lum above rolling barrels #2",
    338: "Lum above rolling barrels #3",
    340: "Lum above rolling barrels #4",
    322: "Lum above rolling barrels #5",
    875: "Cage with purple lum",
    315: "Super lum in cage with purple lum",  
    # whale_05
    325: "Lum on shell ride #1",
    324: "Lum on shell ride #2",
    876: "Cage after shell ride",
    333: "Super lum in cage after shell ride #1",
    328: "Super lum in cage after shell ride #2",
    # whale_10
    303: "Lum exiting underwater #1",
    302: "Lum exiting underwater #2",
    877: "Cage atop ship",
    310: "Super lum in cage atop ship",
    348: "Lum on waterfall slide #1",
    307: "Lum on waterfall slide #2",
    306: "Lum on waterfall slide #3",
    345: "Lum on waterfall slide #4",
    308: "Lum on waterfall slide #5",
    309: "Lum on waterfall slide #6",
    350: "Lum on waterfall slide #7",
    344: "Lum on waterfall slide #8",
    346: "Lum on waterfall slide #9",
    349: "Lum on waterfall slide #10",
    347: "Lum on top of sand #1",
    342: "Lum on top of sand #2",
    343: "Lum in front of exit portal",
    304: "Lum near gorilla pirate #1",
    301: "Lum near gorilla pirate #2",
    305: "Lum near gorilla pirate #3",
    878: "Cage with teensies",
    
    # The Sanctuary of Stone and Fire
    # plum_00
    353: "Lum on pillar in lava",
    356: "Lum in air next to gold fist",
    354: "Lum in cave next to lava river",
    885: "Cage in cave behind gorilla pirate",
    364: "Super lum in cage behind gorilla pirate",
    357: "Lum on lava river",
    883: "Cave below trampoline",
    359: "Super lum in cave below trampoline",
    352: "Lum on spider webs",
    358: "Lum outside above side temple #1",
    351: "Lum outside above side temple #2",
    884: "Cage next to pirate above lava river",
    369: "Super lum in cage next to pirate above lava river",
    355: "Lum on pillar next to crumbling floor",

    # plum_20
    879: "Cage on stone pillar",
    391: "Lum in cage on stone pillar",
    880: "Cage in middle of lava river",
    392: "Lum in cage in middle of lava river #1",
    393: "Lum in cage in middle of lava river #2",
    881: "Cage on lava stairs",
    394: "Lum in cage on lava stairs #1",
    395: "Lum in cage on lava stairs #2",
    396: "Lum in cage on lava stairs #3",
    882: "Cage above golden fist",
    397: "Lum in cage above golden fist #1",
    398: "Lum in cage above golden fist #2",
    399: "Lum in cage above golden fist #3",
    400: "Lum in cage above golden fist #4",

    # plum_10
    386: "Lum on stone wall during lava river",
    380: "Super lum after red lum chain in lava river",
    390: "Lum high above floor next to plum plant",
    388: "Lum on lava river",
    886: "Cage on ceiling high above lava river",
    375: "Super lum in cage on ceiling high above lava river",
    374: "Lum on slide",
    387: "Lum on stone block next to Umber",
    385: "Lum on Umber's head",
    389: "Lum hidden in sanctuary room",
    1113: "Earth Mask of Polokus",
    
    # The Echoing Caves
    # bast_10
    406: "Super lum behind tree",
    401: "Super lum above platform",
    416: "Super lum on ledge #1",
    411: "Super lum on ledge #2",

    # cask_10
    887: "Cage behind breakable door",
    421: "Lum above acid #1",
    422: "Lum above acid #2",
    423: "Lum above acid #3",
    888: "Cage on wooden tower",
    430: "Lum in cage on wooden tower #1",
    431: "Lum in cage on wooden tower #2",
    432: "Lum in cage on wooden tower #3",
    428: "Lum on wooden tower #1",
    429: "Lum on wooden tower #2",
    424: "Lum above acid #4",
    425: "Lum above acid #5",
    426: "Lum above acid #6",
    427: "Lum above acid #7",
    433: "Lum above acid #8",
    434: "Lum above acid #9",
    435: "Lum above acid #10",

    # cask_30
    889: "Cage on ceiling",
    436: "Lum above acid #1",
    437: "Lum above acid #2",
    438: "Lum above acid #3",
    448: "Lum on trampoline",
    890: "Cage that triggers a cutscene",
    449: "Lum above gap in bridge",
    446: "Lum above acid #4",
    447: "Lum above acid #5",
    439: "Lum above acid #6",
    440: "Lum above acid #7",
    441: "Lum above acid #8",
    442: "Lum above acid #9",
    443: "Lum above acid #10",
    444: "Lum above acid #11",
    445: "Lum above acid #12",
    450: "Lum between two wooden structures",
    891: "Cage with Teensie",

    # The Precipice
    # nave_10
    451: "Lum on bridge #1", 
    452: "Lum on bridge #2",
    892: "Cage above green lum",
    454: "Lum in cage above green lum #1",
    455: "Lum in cage above green lum #2",
    460: "Lum on bridge #3",
    893: "Cage above corner platform",
    456: "Lum in cage above corner platform #1",
    457: "Lum in cage above corner platform #2",
    453: "Lum on bridge #4",
    894: "Cage in wooden skull",
    458: "Lum in cage in wooden skull #1",
    459: "Lum in cage in wooden skull #2",

    # nave_15
    465: "Lum around tower #1",
    466: "Lum around tower #2",
    468: "Lum around tower #3",
    896: "Cage hanging on tower",
    470: "Lum in cage hanging on tower #1",
    471: "Lum in cage hanging on tower #2",
    472: "Lum in cage hanging on tower #3",
    469: "Lum around tower #4",
    462: "Lum around tower #5",
    895: "Cage next to switch",
    473: "Lum in cage next to switch #1",
    474: "Lum in cage next to switch #2",
    463: "Lum on crane #1",
    467: "Lum on crane #2",
    475: "Lum on crane #3",
    461: "Lum on crane #4",
    464: "Lum on crane #5",

    # nave_20
    489: "Lum in ravine #1",
    476: "Lum in ravine #2",
    480: "Lum in ravine #3",
    483: "Lum in ravine #4",
    485: "Lum in ravine #5",
    481: "Lum in ravine #6",
    484: "Lum in ravine #7",
    478: "Lum in ravine #8",
    490: "Lum in ravine #9",
    477: "Lum in ravine #10",
    479: "Lum in ravine #11",
    482: "Lum in ravine #12",
    487: "Lum in ravine #13",
    486: "Lum in ravine #14",
    488: "Lum in ravine #15",
    491: "Super lum in pirate fort #1",
    496: "Super lum in pirate fort #2",
    897: "Cage with Teensie",

    # The Top of the World
    # Seat_10
    540: "Lum on chair track #1",
    521: "Lum on chair track #2",
    541: "Lum on chair track #3",
    542: "Lum on chair track #4",
    543: "Lum on chair track #5",
    518: "Lum on chair track #6",
    519: "Lum on chair track #7",
    520: "Lum on chair track #8",
    531: "Lum on chair track #9",
    539: "Lum on chair track #10",
    532: "Lum on chair track #11",
    524: "Lum on chair track #12",
    525: "Lum on chair track #13",
    533: "Lum on chair track #14",
    522: "Lum on chair track #15",
    523: "Lum on chair track #16",
    527: "Lum on chair track #17",
    528: "Lum on chair track #18",
    529: "Lum on chair track #19",
    530: "Lum on chair track #20",
    526: "Lum on chair track #21",
    537: "Lum on chair track #22",
    536: "Lum on chair track #23",
    535: "Lum on chair track #24",
    538: "Lum on chair track #25",
    544: "Lum on chair track #26",
    545: "Lum on chair track #27",
    546: "Lum on chair track #28",
    547: "Lum on chair track #29",
    548: "Lum on chair track #30",
    534: "Lum on chair track #31",
    549: "Lum on chair track #32",
    550: "Lum on chair track #33",

    # seat_11
    501: "Lum next to barrel pirate",
    502: "Lum above pit",
    505: "Lum in Teensie jail",
    504: "Lum on spider web",
    503: "Lum on tall crate",
    899: "Cage next to barrel pirate",
    511: "Lum in cage next to barrel pirate #1",
    512: "Lum in cage next to barrel pirate #2",
    513: "Lum in cage next to barrel pirate #3",
    506: "Lum in hallway",
    507: "Lower lum in dead end",
    508: "Upper lum in dead end",
    517: "Lum behind crate",
    509: "Lum on top of big crate",
    510: "Lum on top of crate next to cage",
    898: "Cage behind crates",
    514: "Lum in cage behind crates #1",
    515: "Lum in cage behind crates #2",
    516: "Lum in cage behind crates #3",
    
    # The Sanctuary of Rock and Lava
    # earth_10
    900: "Cage with purple lum",
    555: "Lum in eyeball room #1",
    551: "Lum in eyeball room #2",
    552: "Lum in eyeball room #3",
    553: "Lum in eyeball room #4",
    554: "Lum in eyeball room #5",
    901: "Cage hanging from bridge",
    556: "Super lum in cage hanging from bridge",   
    # earth_20
    561: "Lum on climable metal grate #1",
    562: "Lum on climable metal grate #2",
    563: "Lum on climable metal grate #3",
    902: "Cage behind stained glass",
    575: "Lum in cage behind stained glass #1",
    576: "Lum in cage behind stained glass #2",
    577: "Lum in cage behind stained glass #3",
    564: "Lum around water lily #1",
    565: "Lum around water lily #2",
    566: "Lum around water lily #3",
    567: "Lum during water lily ride #1",
    568: "Lum during water lily ride #2",
    569: "Lum during water lily ride #3",
    570: "Lum during water lily ride #4",
    571: "Lum midair after water lily #1",
    572: "Lum midair after water lily #2",
    574: "Lum on green platform",
    903: "Cage hanging from green platform",
    579: "Lum in cage hanging from green platform #1",
    578: "Lum in cage hanging from green platform #2",
    580: "Lum in cage hanging from green platform #3",
    573: "Lum before button",
    # earth_30
    581: "Lum on green platform",
    582: "Lum on rotating monolith",
    583: "Lum on platform beneath climbable metal grate",
    584: "Lum on climable metal grate #1",
    585: "Lum on climable metal grate #2",
    586: "Lum on platform atop climable metal grate",
    904: "Cage hanging from platform",
    593: "Lum in cage hanging from platform #1",
    594: "Lum in cage hanging from platform #2",
    595: "Lum in cage hanging from platform #3",
    587: "Lum before button",
    588: "Lum amongst baby caterpillars #1",
    589: "Lum amongst baby caterpillars #2",
    591: "Lum on lower climable metal grate #1",
    592: "Lum on lower climable metal grate #2",
    590: "Lum before pushing walls",
    905: "Cage before pushing walls",
    596: "Lum in cage before pushing walls #1",
    597: "Lum in cage before pushing walls #2",
    598: "Lum in cage before pushing walls #3",
    599: "Lum behind right pillar",
    600: "Lum behind left pillar",
    906: "Cage with teensies",
    
    # The Walk of Power
    # Ly_20
    1272: "Lum in time race #1",
    1251: "Lum in time race #2",
    1271: "Lum in time race #3",
    1273: "Lum in time race #4",
    1274: "Lum in time race #5",
    1275: "Lum in time race #6",
    1252: "Lum in time race #7",
    1253: "Lum in time race #8",
    1278: "Lum in time race #9",
    1277: "Lum in time race #10",
    1254: "Lum in time race #11",
    1279: "Lum in time race #12",
    1255: "Lum in time race #13",
    1280: "Lum in time race #14",
    1281: "Lum in time race #15",
    1282: "Lum in time race #16",
    1256: "Lum in time race #17",
    1257: "Lum in time race #18",
    1284: "Lum in time race #19",
    1258: "Lum in time race #20",
    1285: "Lum in time race #21",
    1276: "Lum in time race #22",
    1259: "Lum in time race #23",
    1286: "Lum in time race #24",
    1269: "Lum in time race #25",
    1289: "Lum in time race #26",
    1288: "Lum in time race #27",
    1260: "Lum in time race #28",
    1261: "Lum in time race #29",
    1287: "Lum in time race #30",
    1262: "Lum in time race #31",
    1263: "Lum in time race #32",
    1290: "Lum in time race #33",
    1291: "Lum in time race #34",
    1295: "Lum in time race #35",
    1267: "Lum in time race #36",
    1292: "Lum in time race #37",
    1270: "Lum in time race #38",
    1293: "Lum in time race #39",
    1265: "Lum in time race #40",
    1266: "Lum in time race #41",
    1294: "Lum in time race #42",
    1296: "Lum in time race #43",
    1299: "Lum in time race #44",
    1298: "Lum in time race #45",
    1268: "Lum in time race #46",
    1300: "Lum in time race #47",
    1283: "Lum in time race #48",
    1297: "Lum in time race #49",
    1264: "Lum in time race #50", 

    # Beneath the Sanctuary of Rock and Lava
    #helic_10
    907: "Cage behind breakable wall",
    610: "Lum in cage behind breakable wall #1",
    611: "Lum in cage behind breakable wall #2",
    612: "Lum in cage behind breakable wall #3",
    643: "Lum in first ascent",
    644: "Lum in flight track #1",
    645: "Lum in flight track #2",
    606: "Lum in flight track #3",
    601: "Lum atop pillar #1",
    602: "Lum atop pillar #2",
    908: "Cage hanging from bridge",
    607: "Lum in cage hanging from bridge #1",
    608: "Lum in cage hanging from bridge #2",
    609: "Lum in cage hanging from bridge #3",
    603: "Lum on bridge #1",
    604: "Lum on bridge #2",
    605: "Lum midair before exit",
    646: "Super lum behind slanted wall",
    #helic_20
    623: "Lum in flight track #1",
    624: "Lum in flight track #2",
    641: "Lum in flight track #3",
    625: "Lum in flight track #4",
    627: "Lum in flight track #5",
    629: "Lum in flight track #6",
    626: "Lum in flight track #7",
    642: "Lum in flight track #8",
    628: "Lum in flight track #9",
    910: "Cage leftmost in stop",
    618: "Super lum in cage leftmost in stop",
    909: "Cage rightmost in stop",
    613: "Super lum in cage rightmost in stop",
    630: "Lum in flight track #10",
    631: "Super lum in flight track #1",
    636: "Super lum in flight track #3",
    #helic_30
    1114: "Fire Mask of Polokus",
    
    # Tomb of the Ancients
    # morb_00
    911: "Cage in room at start",
    697: "Lum in cage in room at start #1",
    698: "Lum in cage in room at start #2",
    699: "Lum in cage in room at start #3",
    700: "Lum in cage in room at start #4",
    694: "Lum surrounding grave #1",
    695: "Lum surrounding grave #2",
    696: "Lum surrounding grave #3",
    691: "Lum surrounding grave #4",
    692: "Lum surrounding grave #5",
    693: "Lum surrounding grave #6",
    1014: "1000th Lum",
    # morb_10
    656: "Lum on flying barrel ride #1",
    655: "Lum on flying barrel ride #2",
    654: "Lum on flying barrel ride #3",
    914: "Cage with purple lum",
    912: "Cage hanging from bridge",
    686: "Super lum in cage hanging from bridge #1",
    681: "Super lum in cage hanging from bridge #2",
    657: "Lum below spider web",
    913: "Cage amongst zombie chickens",
    671: "Super lum in cage amongst zombie chickens #1",
    676: "Super lum in cage amongst zombie chickens #2",
    652: "Lum on barrel sludge ride #1",
    653: "Lum on barrel sludge ride #2",
    651: "Lum on barrel sludge ride #3",
    658: "Lum on barrel sludge ride #4",
    660: "Lum on barrel sludge ride #5",
    659: "Lum on barrel sludge ride #6",
    915: "Cage behind bandage door",
    666: "Super lum in cage behind bandage door #1",
    661: "Super lum in cage behind bandage door #2",    
    # morb_20
    916: "Cage with teensies",
    
    # The Iron Mountains
    # learn_40
    711: "Lum midair with purple lums #1",
    708: "Lum midair with purple lums #2",
    707: "Lum midair with purple lums #3",
    709: "Lum midair with purple lums #4",
    712: "Lum midair after purple lums #1",
    713: "Lum midair after purple lums #2",
    717: "Lum on spinning laser disc #1",
    716: "Lum on spinning laser disc #2",
    715: "Lum on spinning laser disc #3",
    714: "Lum on spinning laser disc #4",
    719: "Lum on spinning laser disc #5",
    718: "Lum on spinning laser disc #6",
    710: "Lum atop wooden tower",
    917: "Cage hanging from wooden tower",
    701: "Lum in cage hanging from wooden tower #1",
    702: "Lum in cage hanging from wooden tower #2",
    703: "Lum in cage hanging from wooden tower #3",
    918: "Cage in windy river",
    706: "Lum in cage in windy river #1",
    705: "Lum in cage in windy river #2",
    704: "Lum in cage in windy river #3",    
    # ile_10
    919: "Cage across bridge",
    721: "Super lum in cage across bridge",
    736: "Super lum atop structure #1",
    731: "Super lum atop structure #2",
    730: "Lum atop structure",
    726: "Lum underneath menhirs #1",
    728: "Lum underneath menhirs #2",
    727: "Lum underneath menhirs #3",
    729: "Lum underneath menhirs #4",
    # mine_10
    720: "Lum atop box",
    746: "Super lum behind entrance",
    741: "Super Lum on top of pipe",
    1115: "Air Mask of Polokus",
    
    # The Prison Ship
    # boat01
    1370: "Lum on slide #1",
    1359: "Lum on slide #2",
    1369: "Lum on slide #3",
    1373: "Lum on slide #4",
    1371: "Lum on slide #5",
    1377: "Lum on slide #6",
    1372: "Lum on slide #7",
    1379: "Lum on slide #8",
    1374: "Lum on slide #9",
    1375: "Lum on slide #10",
    1368: "Lum on slide #11",
    1376: "Lum on slide #12",
    1360: "Lum on slide #13",
    1361: "Lum on slide #14",
    1367: "Lum on slide #15",
    1362: "Lum on slide #16",
    1366: "Lum on slide #17",
    1364: "Lum on slide #18",
    1365: "Lum on slide #19",
    1378: "Lum on slide #20",
    1363: "Lum on slide #21",
    # boat02
    1334: "Lum on slide #1",
    1333: "Lum on slide #2",
    1352: "Lum on slide #3",
    1351: "Lum on slide #4",
    1353: "Lum on slide #5",
    1348: "Lum on slide #6",
    1324: "Lum on slide #7",
    1317: "Lum on slide #8",
    1319: "Lum on slide #9",
    1318: "Lum on slide #10",
    1321: "Lum on slide #11",
    1322: "Lum on slide #12",
    1331: "Lum on slide #13",
    1316: "Lum on slide #14",
    1332: "Lum on slide #15",
    1320: "Lum on slide #16",
    1323: "Lum on slide #17",
    1329: "Lum on slide #18",
    1330: "Lum on slide #19",
    1336: "Lum on slide #20",
    1343: "Lum on slide #21",
    1341: "Lum on slide #22",
    1328: "Lum on slide #23",
    1337: "Lum on slide #24",
    1338: "Lum on slide #25",
    1339: "Lum on slide #26",
    1342: "Lum on slide #27",
    1344: "Lum on slide #28",
    1327: "Lum on slide #29",
    1340: "Lum on slide #30",
    1326: "Lum on slide #31",
    1325: "Lum on slide #32",
    1335: "Lum on slide #33",
    1345: "Lum on slide #34",
    1347: "Lum surrounding exit #1",
    1346: "Lum surrounding exit #2",
    1349: "Lum surrounding exit #3",
    1350: "Lum surrounding exit #4",
    1354: "Super lum near exit",
    # astro_00
    1387: "Lum on metal path",
    1388: "Lum on sloped metal",
    1389: "Super lum underneath metal path",
    1385: "Lum midair on right #1",
    1383: "Lum midair on right #2",
    1382: "Lum near lava #1",
    1381: "Lum near lava #2",
    1380: "Lum near lava #3",
    1384: "Lum midair on left",
    1386: "Lum on exit switch #1",
    1394: "Lum on exit switch #2",
    # astro_10
    1301: "Lum on flight path #1",
    1302: "Lum on flight path #2",
    1303: "Lum on flight path #3",
    1304: "Lum on flight path #4",
    1305: "Lum on flight path #5",
    1306: "Lum on flight path #6",
    1307: "Lum on flight path #7",
    1308: "Lum on flight path #8",
    1309: "Lum on flight path #9",
    1310: "Lum on flight path #10",
    1311: "Super lum on flight path",
}

extra_levels: list[LevelInfo] = [
    LevelInfo(
        "The Fairly Glade #2 - Revisit",
        {
            # The game does not distinguish this area but we do! We give it the custom ID of Learn_32.
            "Learn_32": SubLevelInfo(
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
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
        }
    ),
    LevelInfo(
        "The Walk of Life",
        {
            "Ly_10": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        1201,
                        1202,
                        1203,
                        1236,
                        1206,
                        1205,
                        1208,
                        1210,
                        1212,
                        1209,
                        1214,
                        1211,
                        1215,
                        1217,
                        1216,
                        1218,
                        1219,
                        1220,
                        1221,
                        1222,
                        1223,
                        1224,
                        1225,
                        1226,
                        1227,
                        1229,
                        1230,
                        1231,
                        1233,
                        1244,
                        1246,
                        1242,
                        1232,
                        1243,
                        1238,
                        1239,
                        1240,
                        1245,
                        1247,
                        1237,
                        1234,
                        1228,
                        1207,
                        1235,
                        1241,
                        1249,
                        1213,
                        1250,
                        1248,
                        1204
                    ]
                ),
            )
        },
        lumGate=4,
    ),
    LevelInfo(
        "The Cave of Bad Dreams",
        {
            "vulca_10": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        751
                    ]                    
                ),
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        regularLums=[
                            752,
                            753,
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
                        791
                    ]
                ),
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        superLums=[ 
                            796
                        ],
                        special={
                            1123: "Elixir of Life",
                        }
                    ),
                },
                exitRequirement=Tech.PURPLE_SWING
            )
        }
    ),
    LevelInfo(
        "The Sanctuary of Stone and Fire - Side Temple",
        {
            "plum_20": SubLevelInfo(
                checks=Checks(
                    cages=[
                        879,
                        880,
                        881,
                        882
                    ],
                    regularLums=[
                        391,
                        392,
                        393,
                        394,
                        395,
                        396,
                        397,
                        398,
                        399,
                        400
                    ]
                ),
                exitRequirement=Tech.PURPLE_SWING,
            ),
        }
    ),
    LevelInfo(
        "The Walk of Power",
        {
            "Ly_20": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        1272,
                        1251,
                        1271,
                        1273,
                        1274,
                        1275,
                        1252,
                        1253,
                        1278,
                        1277,
                        1254,
                        1279,
                        1255,
                        1280,
                        1281,
                        1282,
                        1256,
                        1257,
                        1284,
                        1258,
                        1285,
                        1276,
                        1259,
                        1286,
                        1269,
                        1289,
                        1288,
                        1260,
                        1261,
                        1287,
                        1262,
                        1263,
                        1290,
                        1291,
                        1295,
                        1267,
                        1292,
                        1270,
                        1293,
                        1265,
                        1266,
                        1294,
                        1296,
                        1299,
                        1298,
                        1268,
                        1300,
                        1283,
                        1297,
                        1264
                    ]
                ),
            )
        },
        lumGate=5,
    ),
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
                )
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
                        182,
                        183,
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
                        special={
                            1112: "Water Mask",
                        }
                    )
                },
                exitRequirement=Tech.PURPLE_SWING_OR_BACKWARDS_JUMP
            )
        },
        lumGate=0,
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
                        866
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
                        218
                    ],
                    special={
                        1101: "Knowledge of the Cave of Bad Dreams"
                    }
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
        "The Canopy",
        {
            "glob_30": SubLevelInfo(
                checks=Checks(
                    cages=[
                        871,
                        872
                    ],
                    regularLums=[
                        266,
                        251,
                        262,
                        252,
                        253,
                        254,
                        263,
                        258,
                        264,
                        259,
                        255,
                        265,
                        256,
                        261,
                        260,
                        257,
                        267,
                        268,
                        269,
                        270
                    ]                    
                )
            ),
            "glob_10": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        283,
                        276,
                        275,
                        271,
                        274,
                        281,
                        285,
                        280,
                        284,
                        282,
                        277,
                        273,
                        272,
                        279,
                        278
                    ],
                    special={
                        1143: "Silver Lum",
                    },
                )
            ),
            "glob_20": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        286,
                        291,
                        290,
                        287,
                        288,
                        289,
                        299,
                        300
                    ],
                    cages=[
                        874,
                        873
                    ],
                ),
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        regularLums=[
                            297,
                            298
                        ],
                        superLums=[
                            292
                        ]
                    )
                }
            )
        },
    ),
    LevelInfo(
        "Whale Bay",
        {
            "whale_00": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        339,
                        341,
                        327,
                        320,
                        323,
                        321,
                        326,
                        338,
                        340,
                        322
                    ],
                    cages=[
                        875
                    ],
                    superLums=[
                        315
                    ]
                ),
                exitRequirement=Tech.PURPLE_SWING
            ),
            "whale_05": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        325,
                        324
                    ],
                    cages=[
                        876
                    ],
                    superLums=[
                        333,
                        328
                    ]
                )
            ),
            "whale_10": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        303,
                        302,
                        348,
                        307,
                        306,
                        345,
                        308,
                        309,
                        350,
                        344,
                        346,
                        349,
                        347,
                        342,
                        343,
                        304,
                        301,
                        305
                    ],
                    cages=[
                        877,
                        878
                    ],
                    superLums=[
                        310
                    ]
                )
            )
        },
    ),
    LevelInfo(
        "The Sanctuary of Stone and Fire",
        {
            "plum_00": SubLevelInfo(
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        regularLums=[
                            353,
                            356,
                            354,
                            357,
                            352,
                            355
                        ],
                        superLums=[
                            364,
                            359,
                            369
                        ],
                        cages=[
                            885,
                            883,
                            884
                        ]
                    ),
                    Tech.HAS_REENTERED_FROM_THAT_ONE_SPECIFIC_EXIT: Checks(
                        regularLums=[
                            358,
                            351,
                        ]
                    )
                },
                exitRequirement=Tech.PURPLE_SWING_OR_GLM
            ),
            "plum_10": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        386,
                        390,
                        388,
                        374,
                        387,
                        385,
                        389
                    ],
                    superLums=[
                        380,
                        375
                    ],
                    cages=[
                        886
                    ],
                    special={
                        1113: "Earth Mask"
                    }
                )
            ),
        },
        lumGate=1,
    ),
    LevelInfo(
        "The Echoing Caves",
        {
            "bast_10": SubLevelInfo(
                checks=Checks(
                    superLums=[
                        406,
                        401,
                        416,
                        411
                    ]
                )
            ),
            "cask_10": SubLevelInfo(
                checks=Checks(
                    cages=[
                        887,
                        888
                    ],
                    regularLums=[
                        421,
                        422,
                        423,
                        430,
                        431,
                        432,
                        428,
                        429,
                        424,
                        425,
                        426,
                        427,
                        433,
                        434,
                        435
                    ]
                )
            ),
            "cask_30": SubLevelInfo(
                checks=Checks(
                    cages=[
                        889,
                        890,
                        891
                    ],
                    regularLums=[
                        436,
                        437,
                        438,
                        448,
                        449,
                        446,
                        447,
                        439,
                        440,
                        441,
                        442,
                        443,
                        444,
                        445,
                        450,
                    ]
                )
            )
        },
    ),
    LevelInfo(
        "The Precipice",
        {
            "nave_10": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        451
                    ]
                ),
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        regularLums=[
                            452,
                            454,
                            455,
                            460,
                            456,
                            457,
                            453,
                            458,
                            459,
                        ],
                        cages=[
                            892,
                            893,
                            894,
                        ]
                    )
                },
                exitRequirement=Tech.PURPLE_SWING,
            ),
            "nave_15": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        465,
                        466,
                        468,
                        470,
                        471,
                        472,
                        469,
                        462,
                        473,
                        474,
                        463,
                        467,
                        475,
                        461,
                        464,
                    ],
                    cages=[
                        896,
                        895,
                    ]
                )
            ),
            "nave_20": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        489,
                        476,
                        480,
                        483,
                        485,
                        481,
                        484,
                        478,
                        490,
                        477,
                        479,
                        482,
                        487,
                        486,
                        488,
                    ],
                    cages=[
                        897,
                    ],
                    superLums=[
                        491,
                        496,
                    ]
                )
            )
        },
    ),
    LevelInfo(
        "The Top of the World",
        {
            "Seat_10": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        540,
                        521,
                        541,
                        542,
                        543,
                        518,
                        519,
                        520,
                        531,
                        539,
                        532,
                        524,
                        525,
                        533,
                        522,
                        523,
                        527,
                        528,
                        529,
                        530,
                        526,
                        537,
                        536,
                        535,
                        538,
                        544,
                        545,
                        546,
                        547,
                        548,
                        534,
                        549,
                        550
                    ]
                )
            ),
            "seat_11": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        501,
                        502,
                        505,
                        504,
                        503,
                        511,
                        512,
                        513,
                        506,
                        507,
                        508,
                        517,
                        509,
                        510,
                        514,
                        515,
                        516,
                    ],
                    cages=[
                        899,
                        898,
                    ]
                )
            )
        },
    ),
    LevelInfo(
        "The Sanctuary of Rock and Lava",
        {
            "earth_10": SubLevelInfo(
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        regularLums=[
                            555,
                            551,
                            552,
                            553,
                            554
                        ],
                        cages=[
                            900,
                            901
                        ],
                        superLums=[
                            556
                        ]
                    )
                },
                exitRequirement=Tech.PURPLE_SWING
            ),
            "earth_20": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        561,
                        562,
                        563,
                        575,
                        576,
                        577,
                        564,
                        565,
                        566,
                        567,
                        568,
                        569,
                        570,
                        571,
                        572,
                        574,
                        579,
                        578,
                        580,
                        573
                    ],
                    cages=[
                        902,
                        903
                    ]
                )
            ),
            "earth_30": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        581,
                        582,
                        583,
                        584,
                        585,
                        586,
                        593,
                        594,
                        595,
                        587,
                        588,
                        589,
                        591,
                        592,
                        590,
                        596,
                        597,
                        598,
                        599,
                        600
                    ],
                    cages=[
                        904,
                        905,
                        906
                    ]
                )
            )
        },
    ),
    LevelInfo(
        "Beneath the Sanctuary of Rock and Lava",
        {
            "helic_10": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        610,
                        611,
                        612,
                        643,
                        644,
                        645,
                        606,
                        601,
                        602,
                        607,
                        608,
                        609,
                        603,
                        604,
                        605
                    ],
                    cages=[
                        907,
                        908
                    ],
                    superLums=[
                        646
                    ]
                )
            ),
            "helic_20": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        623,
                        624,
                        641,
                        625,
                        627,
                        629,
                        626,
                        642,
                        628,
                        630
                    ],
                    cages=[
                        910,
                        909
                    ],
                    superLums=[
                        618,
                        613,
                        631,
                        636
                    ]
                )
            ),
            "helic_30": SubLevelInfo(
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        special={
                            1114: "Fire Mask"
                        }
                    )
                },
                exitRequirement=Tech.PURPLE_SWING
            )
        },
        lumGate=2,
    ),
    LevelInfo(
        "Tomb of the Ancients",
        {
            "morb_00": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        697,
                        698,
                        699,
                        700,
                        694,
                        695,
                        696,
                        691,
                        692,
                        693,
                        1014
                    ],
                    cages=[
                        911
                    ]
                )
            ),
            "morb_10": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        656,
                        655,
                        654,
                        657,
                        652,
                        653,
                        651,
                        658,
                        660,
                        659
                    ],
                    cages=[
                        914,
                        912,
                        915
                    ],
                    superLums=[
                        686,
                        681,
                        661,
                        666
                    ]
                ),
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        regularLums=[],
                        cages=[
                            913
                        ],
                        superLums=[
                            671,
                            676
                        ]
                    )
                },
                exitRequirement=Tech.PURPLE_SWING
            ),
            "morb_20": SubLevelInfo(
                checks=Checks(
                    cages=[
                        916
                    ]
                )
            )
        },
    ),
    LevelInfo(
        "The Iron Mountains",
        {
            "learn_40": SubLevelInfo(
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        regularLums=[
                            711,
                            708,
                            707,
                            709,
                            712,
                            713,
                            717,
                            716,
                            715,
                            714,
                            719,
                            718,
                            710,
                            701,
                            702,
                            703,
                            706,
                            705,
                            704
                        ],
                        cages=[
                            917,
                            918
                        ]
                    )
                },
                exitRequirement=Tech.PURPLE_SWING
            ),
            "ile_10": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        730,
                        726,
                        728,
                        727,
                        729
                    ],
                    cages=[
                        919
                    ],
                    superLums=[
                        721,
                        736,
                        731
                    ]
                )
            ),
            "mine_10": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        720
                    ],
                    superLums=[
                        746
                    ]
                ),
                behindRequirements={
                    Tech.PURPLE_SWING: Checks(
                        superLums=[
                            741
                        ],
                        special={
                            1115: "Air Mask"
                        }
                    )
                },
                exitRequirement=Tech.PURPLE_SWING
            )
        },
        lumGate=3,
    ),
    LevelInfo(
        "The Prison Ship",
        {
            "boat01": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        1370,
                        1359,
                        1369,
                        1373,
                        1371,
                        1377,
                        1372,
                        1379,
                        1374,
                        1375,
                        1368,
                        1376,
                        1360,
                        1361,
                        1367,
                        1362,
                        1366,
                        1364,
                        1365,
                        1378,
                        1363
                    ]
                )
            ),
            "boat02": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        1334,
                        1333,
                        1352,
                        1351,
                        1353,
                        1348,
                        1324,
                        1317,
                        1319,
                        1321,
                        1322,
                        1331,
                        1316,
                        1332,
                        1320,
                        1323,
                        1329,
                        1330,
                        1336,
                        1343,
                        1341,
                        1328,
                        1337,
                        1338,
                        1339,
                        1342,
                        1344,
                        1327,
                        1340,
                        1326,
                        1325,
                        1335,
                        1345,
                        1347,
                        1346,
                        1349,
                        1350
                    ],
                    superLums=[
                        1354
                    ]
                )
            ),
            "astro_00": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        1387,
                        1388,
                        1385,
                        1383,
                        1382,
                        1381,
                        1380,
                        1384,
                        1386,
                        1394
                    ],
                    superLums=[
                        1389
                    ]
                )
            ),
            "astro_10": SubLevelInfo(
                checks=Checks(
                    regularLums=[
                        1301,
                        1302,
                        1303,
                        1304,
                        1305,
                        1306,
                        1307,
                        1308,
                        1309,
                        1310
                    ],
                    superLums=[
                        1311
                    ]
                )
            )
        },
    ),
    LevelInfo(
        "The Crow's Nest",
        {
            "Rhop_10": SubLevelInfo()
        },
        requireAllMasks=True
    ),
]
