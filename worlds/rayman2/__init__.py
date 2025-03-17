from typing import Type, ClassVar

from BaseClasses import Tutorial, ItemClassification, Item, Region, LocationProgressType, Location
from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World
from .Layout import levels
from .Options import create_option_groups, Rayman2Options


class Rayman2Item(Item):
    game: str = "Rayman 2"

class Rayman2Location(Location):
    game: str = "Rayman 2"

class Rayman2Web(WebWorld):
    option_groups = create_option_groups()
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide for setting up Rayman 2 with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Aeltumn"]
    )]


class Rayman2World(World):
    """
    Rayman 2 is a classic 3D platformer where Rayman sets out on an adventure to obtain four
    masks to defeat an army of Robo-Pirates attacking the Glade of Dreams.
    """

    game = "Rayman 2"
    web = Rayman2Web()
    topology_present = False

    item_name_to_id = {}
    location_name_to_id = {}

    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = Rayman2Options
    options: Rayman2Options

    def __init__(self, multiworld, player):
        super(Rayman2World, self).__init__(multiworld, player)

        # Initialize initial values
        self.base_id = 1651615

        # Store variables with the level shuffle and lum gates
        self.levelSwaps = {}
        self.lumGates = {}
        self.item_pool = []

    def create_regions(self) -> None:
        # Go through all levels in the level layout and create item/location objects,
        # every location is an item and every item is a location in Rayman 2.

        # This is because the game engine has a set id for every single item and all
        # items are tracked individually as completion, so we want to properly track
        # which specific cage or super lum was picked up. For now we use the internal
        # engine names for them all so they are easily distinguished in the game which
        # can be changed later.

        # Start by creating the menu
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        lumTally = 0
        silverLumTally = 0
        for levelName, levelInfo in levels.items():
            # TODO Check for lum gates

            lastRegion = menu
            for subLevelName, subLevelInfo in levelInfo.sublevels.items():
                # TODO Randomly swap around sub levels based on whether we need a silver
                # Determine the level that gets put here


                # TODO Add access rules for masks to enter the Pirate Ship

                # Create this level and connect it
                region = Region(subLevelName, self.player, self.multiworld)
                self.multiworld.regions.append(region)
                lastRegion.connect(region)
                lastRegion = region

                lumTally += subLevelInfo.regularLums
                silverLumTally += subLevelInfo.silverLums

                # Create checks for all super lums
                for superLum in subLevelInfo.superLums:
                    self.create(region, superLum, ItemClassification.filler, LocationProgressType.DEFAULT)

                # Create checks for all cages
                for cage, lumsInside in subLevelInfo.cages.items():
                    self.create(region, cage, ItemClassification.useful, LocationProgressType.PRIORITY)
                    lumTally += lumsInside
                    # TODO Update the lum tally based on which cage gets swapped in as it may contain
                    # a different amount!

                # Create checks for all special checks
                for specialItem in subLevelInfo.special:
                    self.create(region, specialItem, ItemClassification.progression, LocationProgressType.PRIORITY)

            # Connect the last sub-level back to the menu
            if lastRegion.name != menu.name:
                lastRegion.connect(menu)

            # TODO Process the extra level

    def create_item(self, item: str,
                    classification: ItemClassification = ItemClassification.progression) -> Rayman2Item:
        return Rayman2Item(item, classification, self.item_name_to_id[item], self.player)

    def create_items(self):
        self.multiworld.itempool += self.item_pool

    # Creates items and locations for every input
    def create(self, region, name, classification: ItemClassification, progression: LocationProgressType):
        id = self.claim_id()

        # Add the item to the mappings
        self.item_name_to_id[name] = id
        self.item_id_to_name[id] = name
        self.location_name_to_id[name] = id
        self.location_id_to_name[id] = name

        # Add the item to the item pool
        self.item_pool.append(self.create_item(name, classification))

        # Add the item to the region
        location = Rayman2Location(self.player, name, id, region)
        location.progression_type = progression
        region.locations.append(location)

    # Claim a new id for an item and location
    def claim_id(self):
        result = self.base_id
        self.base_id = result + 1
        return result

    # Include level swaps and lum gate information in the slot data
    # sent to the game on connection
    def fill_slot_data(self):
        slot_data = {}
        slot_data["level_swaps"] = self.levelSwaps
        slot_data["lum_gates"] = self.lumGates
        return slot_data
