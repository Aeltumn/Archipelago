# This file contains the full game layout, defining all levels, which sub-levels they have,
# which ids everything uses, and all items contained within. This layout object is used by
# init.py to generate the items, locations, and regions.
levels = {
    "Learn_10": {
        "displayName": "The Woods of Light",
        "sublevels": {
            "Learn_10": {
                "regularLums": 5
            }
        }
    },
    "Learn_30": {
        "displayName": "The Fairy Glade",
        "sublevels": {
            "Learn_30": {
                "regularLums": 3,
                "cages": {
                    "JCP_ARG_CageLums_I7": 1,
                    "JCP_ARG_CageLums_I2": 5
                }
            },
            "Learn_31": {
                "regularLums": 1
            },
            "Bast_20": {
                "regularLums": 7,
                "cages": {
                    "OLP_Cage_Haut": 5,
                    "OLP_Cage_grotte": 5
                }
            },
            "Bast_22": {
                "regularLums": 4,
                "silverLums": 1
            },
            "Learn_60": {
                "needsSilver": True,
                "regularLums": 14,
                "cages": {
                    "JCP_ARG_CageLums_I3": 3
                }
            }
        }
    },
    "Ski_10": {
        "displayName": "The Marshes of Awakening",
        "sublevels": {
            "Ski_10": {
                "regularLums": 10,
                "cages": {
                    "MIC_CageArbre_1": 5,
                    "MIC_CageArbre_3": 5,
                    "MIC_CageArbre_5": 5
                }
            },
            "Ski_60": {
                "regularLums": 5,
                "superLums": [
                    "STH_BigLumsJaune_Bombes",
                    "DOT_lums_08",
                    "DOT_lums_12",
                    "MIC_BigLums_Fin"
                ]
            }
        }
    },
    "Chase_10": {
        "displayName": "The Bayou",
        "extra": ["Ly_10"],
        "sublevels": {
            "Chase_10": {
                "regularLums": 26,
                "needsSilver": True,
                "cages": {
                    "FRG_ARG_CageLums_I1": 2,
                    "FRG_ARG_CageLums_I2": 2,
                    "FRG_ARG_CageLums_I4": 3,
                    "FRG_ARG_CageLums_I5": 2
                }
            },
            "Chase_22": {
                "regularLums": 14,
                "needsSilver": True,
                "cages": {
                    "FRG_CageLums_1": 1
                }
            }
        }
    },
    "Ly_10": {
        "displayName": "The Walk of Life",
        "sublevels": {
            "Ly_10": {
                "regularLums": 50
            }
        }
    }
}