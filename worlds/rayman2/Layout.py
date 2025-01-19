from dataclasses import dataclass, field
from typing import Dict, TypedDict, List


# This file contains the full game layout, defining all levels, which sub-levels they have,
# which ids everything uses, and all items contained within. This layout object is used by
# init.py to generate the items, locations, and regions.
@dataclass
class SubLevelInfo:
    regularLums: int = 0
    superLums: List[str] = field(default_factory=lambda: [])
    cages: Dict[str, int] = field(default_factory=lambda: {})
    silverLums: int = 0
    needsSilver: bool = False


@dataclass
class LevelInfo:
    displayName: str
    sublevels: Dict[str, SubLevelInfo]
    extra: str = None


extra_levels: Dict[str, LevelInfo] = {
    "Ly_10": LevelInfo(
        "The Walk of Life",
        {
            "Ly_10": SubLevelInfo(
                regularLums=50,
            )
        }
    ),
}

levels: Dict[str, LevelInfo] = {
    "Learn_10": LevelInfo(
        "The Woods of Light",
        {
            "Learn_10": SubLevelInfo(
                regularLums=5,
            )
        }
    ),
    "Learn_30": LevelInfo(
        "The Fairy Glade",
        {
            "Learn_30": SubLevelInfo(
                regularLums=3,
                cages={
                    "JCP_ARG_CageLums_I7": 1,
                    "JCP_ARG_CageLums_I2": 5
                },
            ),
            "Learn_31": SubLevelInfo(
                regularLums=1,
            ),
            "Bast_20": SubLevelInfo(
                regularLums=7,
                cages={
                    "OLP_Cage_Haut": 5,
                    "OLP_Cage_grotte": 5
                }
            ),
            "Bast_22": SubLevelInfo(
                regularLums=4,
                silverLums=1
            ),
            "Learn_60": SubLevelInfo(
                needsSilver=True,
                regularLums=14,
                cages={
                    "JCP_ARG_CageLums_I3": 3
                }
            )
        }
    ),
    "Ski_10": LevelInfo(
        "The Marshes of Awakening",
        {
            "Ski_10": SubLevelInfo(
                regularLums=10,
                cages={
                    "MIC_CageArbre_1": 5,
                    "MIC_CageArbre_3": 5,
                    "MIC_CageArbre_5": 5
                }
            ),
            "Ski_60": SubLevelInfo(
                regularLums=5,
                superLums=[
                    "STH_BigLumsJaune_Bombes",
                    "DOT_lums_08",
                    "DOT_lums_12",
                    "MIC_BigLums_Fin"
                ]
            )
        }
    ),
    "Chase_10": LevelInfo(
        "The Bayou",
        {
            "Chase_10": SubLevelInfo(
                needsSilver=True,
                regularLums=26,
                cages={
                    "FRG_ARG_CageLums_I1": 2,
                    "FRG_ARG_CageLums_I2": 2,
                    "FRG_ARG_CageLums_I4": 3,
                    "FRG_ARG_CageLums_I5": 2
                }
            ),
            "Chase_22": SubLevelInfo(
                needsSilver=True,
                regularLums=14,
                cages={
                    "FRG_CageLums_1": 1
                }
            )
        }
    )
}
