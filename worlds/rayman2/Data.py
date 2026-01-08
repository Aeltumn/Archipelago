from dataclasses import dataclass
from typing import List

from BaseClasses import LocationProgressType, ItemClassification
from .Layout import levels, human_readable_names


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
def create(subLevelName, levelName, id, classification: ItemClassification, progression: LocationProgressType):
    hint = human_readable_names[id]
    displayName = f"{levelName} - {hint}"

    item_table.append(
        ItemDefinition(
            displayName=displayName,
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


# Go through all levels to create regions and items
for baseLevelName, levelInfo in levels.items():
    subLevelIndex = 0
    for subLevelName, subLevelInfo in levelInfo.sublevels.items():
        subLevelIndex += 1
        levelName = f"{levelInfo.displayName} #{subLevelIndex}"

        # TODO Add access rules for masks to enter the Pirate Ship
        # TODO Figure out and add lum doors

        # Create checks for all regular lums
        for lum in subLevelInfo.regularLums:
            create(subLevelName, levelName, lum, ItemClassification.filler, LocationProgressType.DEFAULT)

        # Create checks for all super lums
        for superLum in subLevelInfo.superLums:
            create(subLevelName, levelName, superLum, ItemClassification.filler, LocationProgressType.DEFAULT)

        # Create checks for all cages
        for cage in subLevelInfo.cages:
            create(subLevelName, levelName, cage, ItemClassification.useful, LocationProgressType.PRIORITY)

        # Create checks for all special checks
        for specialItem in subLevelInfo.special:
            create(subLevelName, levelName, specialItem, ItemClassification.progression, LocationProgressType.PRIORITY)

    # TODO Process the extra level
