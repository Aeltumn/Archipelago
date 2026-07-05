from dataclasses import dataclass
from typing import List

from Options import FreeText, Range, DeathLink, Choice, OptionGroup, Toggle
from worlds.AutoWorld import PerGameCommonOptions

class EndGoal(Choice):
    """The end goal required to beat the game.

    Crow's Nest: Defeat Razorbeard in the Crow's Nest.
    Treasure%: Take Jano's offer in the Cave of Bad Dreams.
    100%: Requires collecting all 1000 lums, 80 cages, and 4 masks, then defeating Razorbeard.
    """
    display_name = "End Goal"
    option_crows_nest = 1
    option_treasure = 2
    option_100 = 3
    default = 1

    @classmethod
    def get_option_name(cls, value) -> str:
        if value == 1:
            return "Crow's Nest"
        elif value == 2:
            return "Treasure%"
        else:
            return "100%"

class RoomRandomisation(Toggle):
    """Whether to enable room randomization which will randomize the order of all levels."""
    display_name = "Room Randomisation"
    default = True

class Lumsanity(Toggle):
    """Whether all individual yellow lums should be their own checks instead of only super lums. This will add 710 extra progression checks!"""
    display_name = "Lumsanity"
    default = False

class LumBundleSize(Range):
    """If lumsanity is enabled, decides how many lums should be bundled together into a single check."""
    display_name = "Lum Bundle Size"
    range_start = 1
    range_end = 50
    default = 1

class InstantPortalAccess(Toggle):
    """Whether all portals should be accessible as soon as you obtain enough lums. Will speed up the game considerably."""
    display_name = "Instant Portal Access"
    default = False

class FixedLevelLengths(Toggle):
    """Whether to use fixed level lengths with room randomisation, which ensures every level has as many rooms as it does in the base game."""
    display_name = "Fixed Level Lengths"
    default = False

class BetterLevelPortals(Toggle):
    """Whether portals in the Hall of Doors should allow you to teleport to individual sub-levels instead of always going to the first sub-level. Makes it easier to revisit levels and get missed checks."""
    display_name = "Better Level Portals"
    default = False

class RoomRandomisationSeed(FreeText):
    """A seed to use for room randomisation. If left blank the randomisation will be random. Can be used to use the same randomised layout in multiple games."""
    display_name = "Randomisation Seed"

class DeathLinkAmnesty(Range):
    """The amount of deaths required to send a single death link."""
    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 30
    default = 1

class GlitchedLySkip(Toggle):
    """Includes checks behind Ly skip in The Fairy Glade 4 within logic before getting a Silver Lum."""
    display_name = "Include Ly Skip"
    default = False

class GlitchedBackwardsSlideJumps(Toggle):
    """Includes checks behind backwards slide jumps in The Sanctuary of Water and Ice within logic before getting a Silver Lum."""
    display_name = "Include Backwards Slide Jumps"
    default = False

class GlitchedEarlyEchoingCaves(Toggle):
    """Includes checks behind the Early Echoing Caves skip within logic."""
    display_name = "Include Early Echoing Caves Skip"
    default = False

class GlitchedKapouehSkip(Toggle):
    """Includes checks behind Kapoueh skip within logic before getting a Silver Lum."""
    display_name = "Include Kapoueh Skip"
    default = False

class GlitchedDamageBoosts(Toggle):
    """Includes checks behind damage boosts within logic before getting a Silver Lum, such as in The Bayou 1."""
    display_name = "Include Damage Boosts"
    default = False

class GlitchedPlumWallClimb(Toggle):
    """Includes checks obtainable in The Sanctuary of Stone and Fire 1 by climbing the wall with a plum within logic."""
    display_name = "Include Plum Wall Climb"
    default = False

class GlitchedAirswims(Toggle):
    """Includes checks behind airswims within logic before getting a Silver Lum, such as exiting The Whale Bay 1."""
    display_name = "Include Airswims"
    default = False

class GlitchedTornadoSkip(Toggle):
    """Includes checks behind completing The Fairy Glade 5 within logic before getting a Silver Lum, which requires using Tornado skip without needing the purple lum."""
    display_name = "Include Tornado Skip"
    default = False

class GlitchedCOBDSkip(Toggle):
    """Includes checks behind obtaining the Elixir of Life within logic, which requires using COBD skip."""
    display_name = "Include COBD Skip"
    default = False

class GlitchedTechnicalTricks(Toggle):
    """Includes checks behind technical tricks (GLM/NaN) within logic before getting a Silver Lum, this includes any trick that can be easily executed by following precise technical steps. This includes The Sanctuary of Stone and Fire 1 GLM, The Sanctuary of Stone and Fire 2 NaN Plum."""
    display_name = "Include Technical Tricks"
    default = False

class FirstGateRequirement(Range):
    """The amount of lums required to enter the Sanctuary of Water and Ice."""
    display_name = "First Lum Gate Requirement"
    range_start = 0
    range_end = 200
    default = 100

class SecondGateRequirement(Range):
    """The amount of lums required to enter the Sanctuary of Stone & Fire."""
    display_name = "Second Lum Gate Requirement"
    range_start = 0
    range_end = 450
    default = 300

class ThirdGateRequirement(Range):
    """The amount of lums required to enter Beneath the Sanctuary of Rock & Lava."""
    display_name = "Third Lum Gate Requirement"
    range_start = 0
    range_end = 600
    default = 450

class FourthGateRequirement(Range):
    """The amount of lums required to enter the Iron Mountains."""
    display_name = "Fourth Lum Gate Requirement"
    range_start = 0
    range_end = 800
    default = 550

class WalkOfLifeRequirement(Range):
    """The amount of lums required to enter the Walk of Life."""
    display_name = "Walk of Life Lum Requirement"
    range_start = 0
    range_end = 750
    default = 60

class WalkOfPowerRequirement(Range):
    """The amount of lums required to enter the Walk of Power."""
    display_name = "Walk of Power Lum Requirement"
    range_start = 0
    range_end = 750
    default = 475

@dataclass
class Rayman2Options(PerGameCommonOptions):
    end_goal: EndGoal

    death_link: DeathLink
    death_link_amnesty: DeathLinkAmnesty

    room_randomisation: RoomRandomisation
    room_randomisation_seed: RoomRandomisationSeed
    lum_bundle_size: LumBundleSize
    lumsanity: Lumsanity

    instant_portal_access: InstantPortalAccess
    fixed_level_lengths: FixedLevelLengths
    better_level_portals: BetterLevelPortals

    glitched_ly_skip: GlitchedLySkip
    glitched_backwards_slide_jumps: GlitchedBackwardsSlideJumps
    glitched_early_echoing_caves: GlitchedEarlyEchoingCaves
    glitched_kapoueh_skip: GlitchedKapouehSkip
    glitched_damage_boosts: GlitchedDamageBoosts
    glitched_plum_wall_climb: GlitchedPlumWallClimb
    glitched_airswims: GlitchedAirswims
    glitched_tornado_skip: GlitchedTornadoSkip
    glitched_cobd_skip: GlitchedCOBDSkip
    glitched_technical_tricks: GlitchedTechnicalTricks

    first_gate_required: FirstGateRequirement
    second_gate_required: SecondGateRequirement
    third_gate_required: ThirdGateRequirement
    fourth_gate_required: FourthGateRequirement
    walk_of_life_required: WalkOfLifeRequirement
    walk_of_power_required: WalkOfPowerRequirement


def create_option_groups() -> List[OptionGroup]:
    return [
        OptionGroup(name="Glitched Logic Options",
                    options=[GlitchedLySkip, GlitchedBackwardsSlideJumps, GlitchedEarlyEchoingCaves, GlitchedKapouehSkip,
                             GlitchedDamageBoosts, GlitchedPlumWallClimb, GlitchedAirswims, GlitchedTornadoSkip,
                             GlitchedCOBDSkip, GlitchedTechnicalTricks]),
        OptionGroup(name="Lum Requirement Options",
                    options=[WalkOfLifeRequirement, FirstGateRequirement, SecondGateRequirement, WalkOfPowerRequirement,
                             ThirdGateRequirement, FourthGateRequirement])
    ]
