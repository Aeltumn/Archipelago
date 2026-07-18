from dataclasses import dataclass
from typing import Dict, List

from BaseClasses import ItemClassification
from .Layout import Checks, LevelInfo, Tech, levels, extra_levels, rayman_location_hints


@dataclass
class ItemDefinition:
    displayName: str
    progressionClassification: ItemClassification
    endGoals: List[int]
    fragmented: bool



@dataclass
class LocationDefinition:
    region: str
    itemName: str
    displayName: str
    id: int
    tech: Tech
    fragmented: bool
    chainCompletion: str | None = None


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
    "Hover": 1651627,
    "Ledge Grab": 1651628,
    "Swim": 1651629,
    "Lava Hover": 1651630,
    "Fairy Glade Revisit Swing": 1651631,
    "Cave of Bad Dreams 1 Swings": 1651632,
    "Cave of Bad Dreams 2 Swings": 1651633,
    "Stone and Fire Side Temple Swing": 1651634,
    "Fairy Glade 4 Swing": 1651635,
    "Fairy Glade 5 Swing": 1651636,
    "Bayou 1 Swings": 1651637,
    "Bayou 2 Swing": 1651638,
    "Water and Ice 2 Swings": 1651639,
    "Menhir Hills 2 Swings": 1651640,
    "Menhir Hills 3 Swing": 1651641,
    "Canopy 3 Swing": 1651642,
    "Whale Bay 1 Swing": 1651642,
    "Stone and Fire 1 Swings": 1651643,
    "Stone and Fire 2 Swings": 1651644,
    "Precipice 1 Swings": 1651646,
    "Rock and Lava 1 Swing": 1651647,
    "Beneath Rock and Lava 3 Swing": 1651648,
    "Tomb of the Ancients 2 Swings": 1651649,
    "Iron Mountains 1 Swings": 1651650,
    "Iron Mountains 3 Swings": 1651651,
    "Powered Shots": 1651652,
}
fragmented_names = [
    "Fairy Glade Revisit Swing",
    "Cave of Bad Dreams 1 Swings",
    "Cave of Bad Dreams 2 Swings",
    "Stone and Fire Side Temple Swing",
    "Fairy Glade 4 Swing",
    "Fairy Glade 5 Swing",
    "Bayou 1 Swings",
    "Bayou 2 Swing",
    "Water and Ice 2 Swings",
    "Menhir Hills 2 Swings",
    "Menhir Hills 3 Swing",
    "Canopy 3 Swing",
    "Whale Bay 1 Swing",
    "Stone and Fire 1 Swings",
    "Stone and Fire 2 Swings",
    "Precipice 1 Swings",
    "Rock and Lava 1 Swing",
    "Beneath Rock and Lava 3 Swing",
    "Tomb of the Ancients 2 Swings",
    "Iron Mountains 1 Swings",
    "Iron Mountains 3 Swings",
    "Powered Shots",
]
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
def create(subLevelName, levelName, id, itemName, progressionClassification: ItemClassification, endGoals: List[int], tech: Tech, fragmented: bool, chainCompletion: str | None = None):
    hint = rayman_location_hints[id]
    displayName = f"{levelName} - {hint}"

    item_table.append(
        ItemDefinition(
            displayName=itemName,
            progressionClassification=progressionClassification,
            endGoals=endGoals,
            fragmented=fragmented,
        )
    )
    location_table.append(
        LocationDefinition(
            region=subLevelName,
            itemName=itemName,
            displayName=displayName,
            id=base_id + id,
            tech=tech,
            fragmented=fragmented,
            chainCompletion=chainCompletion,
        )
    )

def createForChecks(subLevelName, levelName, checks: Checks, tech: Tech):
    # Create checks for all regular lums
    for lum in checks.regularLums:
        create(subLevelName, levelName, lum, "Lum", ItemClassification.progression_deprioritized_skip_balancing, [1, 2, 3, 4, 5], tech, False)

    # Create checks for all super lums
    for superLum in checks.superLums:
        create(subLevelName, levelName, superLum, "Super Lum", ItemClassification.progression_deprioritized_skip_balancing, [1, 2, 3, 4, 5], tech, False)

    # Create checks for all cages
    for cage in checks.cages:
        create(subLevelName, levelName, cage, "Cage", ItemClassification.progression_deprioritized_skip_balancing, [3, 5], tech, False)

    # Create checks for all special checks
    for specialItem, name in checks.special.items():
        if "Mask" in name:
            endGoals = [1, 3, 5]
        else:
            endGoals = [1, 2, 3, 4, 5]

        if name == "Fragmented Silver Lum":
            name = fragmented_names.pop(0)
            fragmented = True
        else:
            fragmented = False

        create(subLevelName, levelName, specialItem, name, ItemClassification.progression | ItemClassification.useful, endGoals, tech, fragmented)

        # Silver Lums are also created as the same item but with the fragmented silver lums!
        if name == "Silver Lum":
            name = fragmented_names.pop(0)
        item_table.append(
            ItemDefinition(
                displayName=name,
                progressionClassification=ItemClassification.progression | ItemClassification.useful,
                endGoals=endGoals,
                fragmented=True,
            )
        )

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
        createForChecks(subLevelName, levelName, subLevelInfo.checks, Tech())
        for tech, checks in subLevelInfo.behindRequirements.items():
            createForChecks(subLevelName, levelName, checks, tech)

    # Create the item for finishing this chain
    if levelInfo.chain is not None and levelInfo.portalId is not None:
        if levelInfo.chain == "bayou":
            # The Bayou portal defaults to Swim not one of the fragmented silver lums.
            create("Menu", "Hall of Doors", levelInfo.portalId, "Swim", ItemClassification.progression | ItemClassification.useful, [1, 2, 3, 4, 5], Tech(), False, levelInfo.chain)
        else:
            create("Menu", "Hall of Doors", levelInfo.portalId, fragmented_names.pop(0), ItemClassification.progression | ItemClassification.useful, [1, 2, 3, 4, 5], Tech(), True, levelInfo.chain)