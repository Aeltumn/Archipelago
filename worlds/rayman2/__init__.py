from typing import Type, ClassVar

from BaseClasses import Tutorial
from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World
from .Options import create_option_groups, Rayman2Options


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
    item_name_to_id = {}
    location_name_to_id = {}

    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = Rayman2Options
    options: Rayman2Options
