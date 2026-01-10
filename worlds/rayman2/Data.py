from dataclasses import dataclass
from typing import List

from BaseClasses import LocationProgressType, ItemClassification
from .Layout import Checks, levels, extra_levels, human_readable_names


@dataclass
class ItemDefinition:
    displayName: str
    id: int
    classification: ItemClassification


@dataclass
class LocationDefinition:
    region: str
    displayName: str
    id: int
    progressionType: LocationProgressType


base_id = 1651615
item_table: List[ItemDefinition] = []
location_table: List[LocationDefinition] = []

# Creates items and locations for every input
def create(subLevelName, levelName, id, itemName, classification: ItemClassification, progression: LocationProgressType):
    hint = human_readable_names[id]
    displayName = f"{levelName} - {hint}"

    item_table.append(
        ItemDefinition(
            displayName=itemName,
            id=base_id + id,
            classification=classification,
        )
    )
    location_table.append(
        LocationDefinition(
            region=subLevelName,
            displayName=displayName,
            id=base_id + id,
            progressionType=progression,
        )
    )

def createForChecks(subLevelName, levelName, checks: Checks):
    # Create checks for all regular lums
    for lum in checks.regularLums:
        create(subLevelName, levelName, lum, "Lum", ItemClassification.filler, LocationProgressType.DEFAULT)

    # Create checks for all super lums
    for superLum in checks.superLums:
        create(subLevelName, levelName, superLum, "Super Lum", ItemClassification.filler, LocationProgressType.DEFAULT)

    # Create checks for all cages
    for cage in checks.cages:
        create(subLevelName, levelName, cage, "Cage", ItemClassification.useful, LocationProgressType.PRIORITY)

    # Create checks for all special checks
    for specialItem, name in checks.special.items():
        create(subLevelName, levelName, specialItem, name, ItemClassification.progression, LocationProgressType.PRIORITY)

# Go through all levels to create regions and items
for baseLevelName, levelInfo in levels.items():
    subLevelIndex = 0
    for subLevelName, subLevelInfo in levelInfo.sublevels.items():
        subLevelIndex += 1
        levelName = f"{levelInfo.displayName} #{subLevelIndex}"

        # Create items out of any defined checks
        createForChecks(subLevelName, levelName, subLevelInfo.checks)
        for _, checks in subLevelInfo.behindRequirements.items():
            createForChecks(subLevelName, levelName, checks)

# Also go through all extra levels!
for baseLevelName, levelInfo in extra_levels.items():
    subLevelIndex = 0
    for subLevelName, subLevelInfo in levelInfo.sublevels.items():
        subLevelIndex += 1
        levelName = f"{levelInfo.displayName} #{subLevelIndex}"

        # Create items out of any defined checks
        createForChecks(subLevelName, levelName, subLevelInfo.checks)
        for _, checks in subLevelInfo.behindRequirements.items():
            createForChecks(subLevelName, levelName, checks)
