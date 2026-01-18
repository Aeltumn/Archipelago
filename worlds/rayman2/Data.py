from dataclasses import dataclass
from typing import List

from BaseClasses import LocationProgressType, ItemClassification
from .Layout import Checks, LevelInfo, Tech, levels, extra_levels, human_readable_names


@dataclass
class ItemDefinition:
    displayName: str
    id: int
    classification: ItemClassification


@dataclass
class LocationDefinition:
    region: str
    itemName: str
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
            itemName=itemName,
            displayName=displayName,
            id=base_id + id,
            progressionType=progression,
            tech=tech,
        )
    )

def createForChecks(subLevelName, levelName, checks: Checks, tech: Tech):
    # Create checks for all regular lums
    for lum in checks.regularLums:
        create(subLevelName, levelName, lum, "Lum", ItemClassification.progression_deprioritized, LocationProgressType.DEFAULT, tech)

    # Create checks for all super lums
    for superLum in checks.superLums:
        create(subLevelName, levelName, superLum, "Super Lum", ItemClassification.progression_deprioritized, LocationProgressType.DEFAULT, tech)

    # Create checks for all cages
    for cage in checks.cages:
        create(subLevelName, levelName, cage, "Cage", ItemClassification.filler, LocationProgressType.DEFAULT, tech)

    # Create checks for all special checks
    for specialItem, name in checks.special.items():
        create(subLevelName, levelName, specialItem, name, ItemClassification.progression | ItemClassification.useful, LocationProgressType.PRIORITY, tech)

# Go through all levels to create regions and items
allLevels: list[LevelInfo] = []
allLevels += levels
allLevels += extra_levels

for levelInfo in allLevels:
    subLevelIndex = 0
    hasMultipleRooms = len(levelInfo.sublevels) > 1

    for subLevelName, subLevelInfo in levelInfo.sublevels.items():
        # If there's multiple levels add the sub level number to the name!
        subLevelIndex += 1
        if hasMultipleRooms:
            levelName = f"{levelInfo.displayName} #{subLevelIndex}"
        else:
            levelName = levelInfo.displayName

        # Create items out of any defined checks
        createForChecks(subLevelName, levelName, subLevelInfo.checks, Tech.NONE)
        for tech, checks in subLevelInfo.behindRequirements.items():
            createForChecks(subLevelName, levelName, checks, tech)
