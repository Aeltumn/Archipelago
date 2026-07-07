from dataclasses import dataclass
from typing import Dict, List

from BaseClasses import ItemClassification
from .Layout import Checks, LevelInfo, Tech, levels, extra_levels, human_readable_names


@dataclass
class ItemDefinition:
    displayName: str
    classification: ItemClassification
    regularClassification: ItemClassification



@dataclass
class LocationDefinition:
    region: str
    itemName: str
    displayName: str
    id: int
    tech: Tech


base_id = 1651615
rayman_item_name_to_id: Dict[str, int] = {
    "Lum": 1651615,
    "Super Lum": 1651616,
    "Cage": 1651617,
    "Water Mask": 1651618,
    "Earth Mask": 1651619,
    "Fire Mask": 1651620,
    "Air Mask": 1651621,
    "Silver Lum": 1651622,
    "Elixir of Life": 1651623,
    "Knowledge of the Cave of Bad Dreams": 1651624,
    "Lum Bundle": 1651625,
    "Leftover Lum Bundle": 1651626,
}
item_table: List[ItemDefinition] = []
location_table: List[LocationDefinition] = []

# Create location names for everything including all possible lum bundles
def create_rayman_location_names():
    names = {loc.displayName: loc.id for loc in location_table}
    bundle_base_id = 1653615
    names["Leftover Lum Bundle"] = bundle_base_id
    for i in range(0, 355):
        bundle_base_id += 1
        name = f"Lum Bundle #{i + 1}"
        names[name] = bundle_base_id
    return names

# Creates items and locations for every input
def create(subLevelName, levelName, id, itemName, classification: ItemClassification, regularClassification: ItemClassification, tech: Tech):
    hint = human_readable_names[id]
    displayName = f"{levelName} - {hint}"

    item_table.append(
        ItemDefinition(
            displayName=itemName,
            classification=classification,
            regularClassification=regularClassification,
        )
    )
    location_table.append(
        LocationDefinition(
            region=subLevelName,
            itemName=itemName,
            displayName=displayName,
            id=base_id + id,
            tech=tech,
        )
    )

def createForChecks(subLevelName, levelName, checks: Checks, tech: Tech):
    # Create checks for all regular lums
    for lum in checks.regularLums:
        create(subLevelName, levelName, lum, "Lum", ItemClassification.progression_deprioritized_skip_balancing, ItemClassification.progression_deprioritized_skip_balancing, tech)

    # Create checks for all super lums
    for superLum in checks.superLums:
        create(subLevelName, levelName, superLum, "Super Lum", ItemClassification.progression_deprioritized_skip_balancing, ItemClassification.progression_deprioritized_skip_balancing, tech)

    # Create checks for all cages
    for cage in checks.cages:
        create(subLevelName, levelName, cage, "Cage", ItemClassification.progression_deprioritized_skip_balancing, ItemClassification.filler, tech)

    # Create checks for all special checks
    for specialItem, name in checks.special.items():
        create(subLevelName, levelName, specialItem, name, ItemClassification.progression | ItemClassification.useful, ItemClassification.progression | ItemClassification.useful, tech)

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
