from dataclasses import dataclass
from typing import List

from BaseClasses import LocationProgressType, ItemClassification
from .Layout import levels


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
    needsSilver: bool


base_id = 1651615
item_table: List[ItemDefinition] = []
location_table: List[LocationDefinition] = []
silverLumItemNames: List[str] = []
idMap: dict[int, str] = {}


# Claim a new id for an item and location
def claim_id():
    global base_id
    result = base_id
    base_id = result + 1
    return result


# Creates items and locations for every input
def create(subLevelName, internalName, name, classification: ItemClassification, progression: LocationProgressType,
           needsSilver: bool = False):
    # Add a requirement to obtain at least one silver lum from the options
    if "Silver Lum" in name:
        silverLumItemNames.append(name)

    id = claim_id()
    item_table.append(
        ItemDefinition(
            displayName=name,
            id=id,
            classification=classification,
        )
    )
    location_table.append(
        LocationDefinition(
            region=subLevelName,
            displayName=name,
            id=id,
            progressionType=progression,
            needsSilver=needsSilver,
        )
    )

    # Note down in the id map that this item exists
    # This is a temporary map for the mod to go from id -> game object name before ids get hardcoded.
    idMap[id] = internalName


# Go through all levels to create regions and items
for baseLevelName, levelInfo in levels.items():
    subLevelIndex = 0
    for subLevelName, subLevelInfo in levelInfo.sublevels.items():
        subLevelIndex += 1
        levelName = f"{levelInfo.displayName} {subLevelIndex}"

        # TODO Add access rules for masks to enter the Pirate Ship

        # Add access requirements to any levels that need silver lums
        needsSilver = subLevelInfo.needsSilver

        # Create an item for the silver lum
        if subLevelInfo.silverLum:
            create(subLevelName, f"{subLevelName}_SilverLum", f"{levelName} - Silver Lum",
                   ItemClassification.progression,
                   LocationProgressType.PRIORITY, needsSilver)

        # Create checks for all super lums
        index = 1
        for superLum in subLevelInfo.superLums:
            create(subLevelName, superLum, f"{levelName} - 5 Lum #{index}", ItemClassification.filler,
                   LocationProgressType.DEFAULT, needsSilver)
            index += 1

        # Create checks for all cages
        index = 1
        for cage, lumsInside in subLevelInfo.cages.items():
            create(subLevelName, cage, f"{levelName} - Cage #{index}", ItemClassification.useful,
                   LocationProgressType.PRIORITY, needsSilver)
            index += 1

        # Create checks for all special checks
        for (specialItem, displayName) in subLevelInfo.special.items():
            create(subLevelName, specialItem, f"{levelName} - {displayName}", ItemClassification.progression,
                   LocationProgressType.PRIORITY, needsSilver)

    # TODO Process the extra level
