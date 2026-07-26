from dataclasses import dataclass
from typing import List

from Options import FreeText, Range, DeathLink, Choice, OptionGroup, Toggle
from worlds.AutoWorld import PerGameCommonOptions

class EndGoal(Choice):
    """The end goal required to beat the game.

    All Masks: Defeat Razorbeard in the Crow's Nest after gathering 4 masks.
    Treasure%: Take Jano's offer in the Cave of Bad Dreams.
    100%: Requires collecting all 1000 lums, 80 cages, and 4 masks, then defeating Razorbeard.
    Any%: Defeat Razorbeard in the Crow's Nest by any means.
    All Cages: Defeat Razorbeard in the Crow's Nest after gathering 4 masks and 80 cages.
    """
    display_name = "End Goal"
    option_all_masks = 1
    option_treasure = 2
    option_100 = 3
    option_any = 4
    option_cages = 5
    default = 1

    @classmethod
    def get_option_name(cls, value) -> str:
        if value == 1:
            return "All Masks"
        elif value == 2:
            return "Treasure%"
        elif value == 3:
            return "100%"
        elif value == 4:
            return "Any%"
        elif value == 5:
            return "All Cages"
        return "Unknown"

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
    """Whether portals in the Hall of Doors in room randomisation mode should allow you to teleport to individual sub-levels instead of always going to the first sub-level. Makes it easier to revisit levels and get missed checks."""
    display_name = "Better Level Portals"
    default = False

class RoomRandomisationSeed(FreeText):
    """A seed to use for room randomisation. If left blank the randomisation will be random. Can be used to use the same randomised layout in multiple games."""
    display_name = "Randomisation Seed"
    default = ""

class RestrictiveRoomRandomisationPositions(Toggle):
    """Restricts where rooms can be placed so all rooms have to match the same entrance-exit combination as the one they replace. This looks better visually but results in worse randomization of some levels."""
    display_name = "Restrictive Room Randomisation Positions"
    default = False

class DamageLink(Toggle):
    """Whether death links should trigger every time Rayman takes damage instead of only when he respawns."""
    display_name = "Damage Link"
    default = False

class DeathLinkAmnesty(Range):
    """The amount of deaths required to send a single death link."""
    display_name = "Death Link Amnesty"
    range_start = 1
    range_end = 30
    default = 1

class FragmentedSilverLums(Toggle):
    """Whether Silver Lums should be fragmented into 22 individual checks instead of 2. This changes every individual sub-level with swings into a separate check to be able to use the swings in that level."""
    display_name = "Fragmented Silver Lums"
    default = False

class MovementHover(Toggle):
    """Whether the ability for Rayman to hover should be randomized and require a check to use."""
    display_name = "Randomize Hover"
    default = False

class MovementSwim(Toggle):
    """Whether the ability for Rayman to swim should be randomized and require a check to use. Rayman will be killed for touching water without receiving Swim, if this causes a softlock by e.g. entering Whale Bay 3, run `stuck` in the in-game console."""
    display_name = "Randomize Swim"
    default = False

class MovementLedgeGrab(Toggle):
    """Whether the ability for Rayman to grab ledges should be randomized and require a check to use."""
    display_name = "Randomize Ledge Grab"
    default = False

class MovementLavaHover(Toggle):
    """Whether the ability for Rayman to hover above lava in Beneath the Sanctuary of Rock and Lava should be randomized and require a check to use."""
    display_name = "Randomize Lava Hover"
    default = False

class GlitchedLySkip(Toggle):
    """Includes checks behind Ly skip in The Fairy Glade 4 within logic before getting a Silver Lum."""
    display_name = "Include Ly Skip"
    default = False

class GlitchedBackwardsSlideJumps(Toggle):
    """Includes checks behind backwards slide jumps in The Sanctuary of Water and Ice within logic before getting a Silver Lum."""
    display_name = "Include Backwards Slide Jumps"
    default = False

class GlitchedEarlyEchoingCaves(Toggle):
    """Includes the Early Echoing Caves skip as a valid way to reach other levels."""
    display_name = "Include Early Echoing Caves Skip"
    default = False

class GlitchedReverseEarlyEchoingCaves(Toggle):
    """Includes the lum boost from The Fairy Glade Revisit area to get back to the main area as a valid way to reach other levels."""
    display_name = "Include Reverse EEC"
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
    """Includes checks behind obtaining the Elixir of Life within logic, which requires using COBD skip. Includes the cage after talking to Clark in The Menhir Hills 2."""
    display_name = "Include COBD Skip"
    default = False

class GlitchedTechnicalTricks(Toggle):
    """Includes checks behind technical tricks (GLM/NaN) within logic before getting a Silver Lum, this includes any trick that can be easily executed by following precise technical steps. This includes The Sanctuary of Stone and Fire 1 GLM including backwards completion of that level and The Sanctuary of Stone and Fire 2 NaN Plum. It also includes the precise jump to complete Whale Bay 1 at the end."""
    display_name = "Include Technical Tricks"
    default = False

class GlitchedJanoSkip(Toggle):
    """Includes checks behind using the various Jano Skips before getting a Silver Lum, this includes the Super Lum in the boss fight area."""
    display_name = "Include Jano Tricks"
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
    damage_link: DamageLink

    room_randomisation: RoomRandomisation
    room_randomisation_seed: RoomRandomisationSeed
    restrictive_room_randomisation: RestrictiveRoomRandomisationPositions
    lum_bundle_size: LumBundleSize
    lumsanity: Lumsanity
    fragmented_silver_lums: FragmentedSilverLums

    instant_portal_access: InstantPortalAccess
    fixed_level_lengths: FixedLevelLengths
    better_level_portals: BetterLevelPortals
    
    movement_hover: MovementHover
    movement_ledge_grab: MovementLedgeGrab
    movement_swim: MovementSwim
    movement_lava_hover: MovementLavaHover

    glitched_early_echoing_caves: GlitchedEarlyEchoingCaves
    glitched_technical_tricks: GlitchedTechnicalTricks
    glitched_jano_skip: GlitchedJanoSkip
    glitched_tornado_skip: GlitchedTornadoSkip
    glitched_plum_wall_climb: GlitchedPlumWallClimb
    glitched_damage_boosts: GlitchedDamageBoosts
    glitched_backwards_slide_jumps: GlitchedBackwardsSlideJumps
    glitched_airswims: GlitchedAirswims
    glitched_cobd_skip: GlitchedCOBDSkip
    glitched_kapoueh_skip: GlitchedKapouehSkip
    glitched_reverse_early_echoing_caves: GlitchedReverseEarlyEchoingCaves
    glitched_ly_skip: GlitchedLySkip

    first_gate_required: FirstGateRequirement
    second_gate_required: SecondGateRequirement
    third_gate_required: ThirdGateRequirement
    fourth_gate_required: FourthGateRequirement
    walk_of_life_required: WalkOfLifeRequirement
    walk_of_power_required: WalkOfPowerRequirement


def create_option_groups() -> List[OptionGroup]:
    return [
        OptionGroup(name="Randomized Movement Ability Options",
                    options=[MovementHover, MovementLedgeGrab, MovementSwim, MovementLavaHover]),
        OptionGroup(name="Glitched Logic Options",
                    options=[GlitchedLySkip, GlitchedBackwardsSlideJumps, GlitchedEarlyEchoingCaves, GlitchedReverseEarlyEchoingCaves, GlitchedKapouehSkip,
                             GlitchedDamageBoosts, GlitchedPlumWallClimb, GlitchedAirswims, GlitchedTornadoSkip,
                             GlitchedCOBDSkip, GlitchedTechnicalTricks, GlitchedJanoSkip]),
        OptionGroup(name="Lum Requirement Options",
                    options=[WalkOfLifeRequirement, FirstGateRequirement, SecondGateRequirement, WalkOfPowerRequirement,
                             ThirdGateRequirement, FourthGateRequirement])
    ]
