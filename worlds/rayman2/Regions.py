# All level names that can be shuffled.
levels = [
    "The Woods of Light",
    "The Fairy Glade",
    "The Marshes of Awakening",
    "The Bayou",
    "The Menhir Hills",
    "The Canopy",
    "Whale Bay",
    "The Echoing Caves",
    "The Precipice",
    "The Top of the World",
    "The Sanctuary of Rock and Lava",
    "Tomb of the Ancients"
    # We don't randomise the last two levels.
]

# All mask levels that can only be shuffled with one another.
mask_levels = [
    "The Sanctuary of Water and Ice",
    "The Sanctuary of Stone and Fire",
    "Beneath the Sanctuary of Rock and Lava",
    "The Iron Mountains"
]

# All extra levels that have a region but aren't random.
extra_regions = {
    "The Walk of Life": "The Bayou",
    "The Cave of Bad Dreams": "The Menhir Hills",
    "The Walk of Power": "The Sanctuary of Rock and Lava",
    "The Prison Ship": "Menu",
    "The Crow's Nest": "The Crow's Nest"
}

# A list of levels mapped to the levels they must be after.
goes_before_requirements = {
    "The Menhir Hills": ["The Marshes of Awakening"] # To completely Menhir you need to be able to backtrack to the cave of bad dreams
}

# How many levels are un-completable without the first silver lum.
purple_lum_levels = [
    "The Bayou",
    "The Sanctuary of Water and Ice",
    "The Menhir Hills", # by proxy because Cave of Bad Dreams needs them
]

# All levels that give you a silver lum. One of these will be in the first 4 levels.
silver_lum_levels = [
    "The Fairy Glade"
]

# The internal names of all levels.
internal_names = {
    "The Woods of Light": "Learn_10",
    "The Fairy Glade": "Learn_30",
    "The Marshes of Awakening": "Ski_10",
    "The Bayou": "Chase_10",
    "The Sanctuary of Water and Ice": "Water_10",
    "The Menhir Hills": "Rodeo_10",
    "The Canopy": "Glob_30",
    "Whale Bay": "Whale_00",
    "The Sanctuary of Stone and Fire": "Plum_00",
    "The Echoing Caves": "Bast_10",
    "The Precipice": "Nave_10",
    "The Top of the World": "Seat_10",
    "The Sanctuary of Rock and Lava": "Earth_10",
    "Beneath the Sanctuary of Rock and Lava": "Helic_10",
    "Tomb of the Ancients": "Morb_00",
    "The Iron Mountains": "Learn_40"
}


def create_regions(world: "Rayman2World"):
    pass