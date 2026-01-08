from dataclasses import dataclass, field
from typing import Dict, List


# This file contains the full game layout, defining all levels, which sub-levels they have,
# which ids everything uses, and all items contained within. This layout object is used by
# init.py to generate the items, locations, and regions.
@dataclass
class SubLevelInfo:
    hasExitPortal: bool = False
    regularLums: List[int] = field(default_factory=lambda: [])
    superLums: List[int] = field(default_factory=lambda: [])
    cages: List[int] = field(default_factory=lambda: [])
    lumGate: bool = False
    special: List[int] = field(default_factory=lambda: [])


@dataclass
class LevelInfo:
    displayName: str
    sublevels: Dict[str, SubLevelInfo]
    extra: str = None

human_readable_names: Dict[int, str] = {
    # learn_10
    840: "Cage above wooden grate",
    1399: "Lum from cage above wooden grate",
    1396: "Lum above Murfy stone",
    1398: "Lum on grass next to waterfall",
    1400: "Lum underneath waterfal",
    1397: "Lum between stone walls",
    841: "Cage with Teensies",
    # Learn_30
    7: "Lum above mushroom",
    8: "Lum on tree branch",
    843: "Cage on tree branch",
    12: "Lum in cage on tree branch",
    842: "Underwater cage",
    1: "Super Lum in underwater cage",
    6: "Lum under bridge",
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
        }
    ),
}
