from dataclasses import dataclass
from typing import List

from BaseClasses import LocationProgressType, ItemClassification
from .Layout import Checks, Tech, levels, extra_levels, human_readable_names


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
    tech: Tech


base_id = 1651615
item_table: List[ItemDefinition] = []
location_table: List[LocationDefinition] = []

# Creates items and locations for every input
def create(subLevelName, levelName, id, itemName, classification: ItemClassification, progression: LocationProgressType, tech: Tech):
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
            tech=tech,
        )
    )

def createForChecks(subLevelName, levelName, checks: Checks, tech: Tech):
    # Create checks for all regular lums
    for lum in checks.regularLums:
        create(subLevelName, levelName, lum, "Lum", ItemClassification.filler, LocationProgressType.DEFAULT, tech)

    # Create checks for all super lums
    for superLum in checks.superLums:
        create(subLevelName, levelName, superLum, "Super Lum", ItemClassification.filler, LocationProgressType.DEFAULT, tech)

    # Create checks for all cages
    for cage in checks.cages:
        create(subLevelName, levelName, cage, "Cage", ItemClassification.useful, LocationProgressType.PRIORITY, tech)

    # Create checks for all special checks
    for specialItem, name in checks.special.items():
        create(subLevelName, levelName, specialItem, name, ItemClassification.progression, LocationProgressType.PRIORITY, tech)

# Go through all levels to create regions and items
for levelInfo in levels:
    subLevelIndex = 0
    for subLevelName, subLevelInfo in levelInfo.sublevels.items():
        subLevelIndex += 1
        levelName = f"{levelInfo.displayName} #{subLevelIndex}"

        # Create items out of any defined checks            )
        createForChecks(subLevelName, levelName, subLevelInfo.checks, Tech.NONE)
        for tech, checks in subLevelInfo.behindRequirements.items():
            createForChecks(subLevelName, levelName, checks, tech)

# Also go through all extra levels!
for subLevelName, subLevelInfo in extra_levels.items():
    levelName = f"{levelInfo.displayName} #{subLevelIndex}"

    # Create items out of any defined checks
    createForChecks(subLevelName, levelName, subLevelInfo.checks, Tech.NONE)
    for tech, checks in subLevelInfo.behindRequirements.items():
        createForChecks(subLevelName, levelName, checks, tech)
