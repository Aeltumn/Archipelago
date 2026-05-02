# Rayman 2

## What are checks in this game?

The following things count as checks:
- Picking up Super Yellow Lums
- Destroying Cages
- Receiving Silver Lums
- Obtaining Masks
- Learning about the location of the Cave of Bad Dreams
- Obtaining the Elixir of Life

If lumsanity is enabled, all yellow lums become checks instead of just the super lums.

## What does randomization do to this game?

When the game is randomised sub-levels are shuffled around. Levels may be built up of any randomised sub levels inside. The contents of cages are not changed. The new order of sub levels can be seen in-game after completing a full level.

# Frequently Asked Questions
Here's some frequently asked questions related to issues while setting up the mod.

### I get errors when trying to generate this game, why?
Rayman 2 has lum gates which require progression items to be obtained consistently throughout many checks, this can make the game un-completable if too many cages or single lums are placed in early check locations. Try lowering the lum gate requirements if errors occur. The maximum values are set to the highest feasible values at which generations still frequently succeed, but it's advised to put them lower.

### I installed the mod, but it says `ap` is an unknown command?
Sometimes the installed mods can get loaded out of order, which causes the custom commands to not get registered. Open up `LoadOrder.cfg` and ensure `R2Console.dll` is listed above `Rayman2APMod.dll`.

### The `~` key doesn't open the console.
Due to Rayman 2 being an old game the `~` key may not be the same on all keyboards. You can check [this website](https://kbdlayout.info/features/virtualkeys/VK_OEM_3) to see which button corresponds to the console on each keyboard type. Alternatively, check the pinned message in the Rayman 2 thread with a different version of the console mod which adds `F12` as a key to open the console.