# Bloodlines MO2 Plugin

Mod Organizer 2 plugin for *Vampire: The Masquerade – Bloodlines*

---

## Installation

### File Placement

```text
[MO2 Installation Directory]/
├── ModOrganizer.exe
└── plugins/
    └── basic_games/
        └── games/
          └── game_vampirebloodlines.py
```

### Steps

1. Copy `game_vampirebloodlines.py` into:

   ```
   ModOrganizer2/plugins/basic_games/games/
   ```
2. Restart Mod Organizer 2
3. Select **"Vampire - The Masquerade: Bloodlines"** as the managed game

---

## Executable Setup (MO2)

You might need to change the Argument on the `vampire.exe` to point torwards the path of the Overhaul you are using.

This is normally

`-game Unofficial_Patch`

But other Overhauls might use another Patch such as Clan Quest mod using `CQM` so in these cases you would use `-game CQM` or whatever the folder that the overhaul uses

I have listed all the ones I am aware of below

- Unoffical_Patch
- Antitribu_Mod
- Barabbah_Addon
- Bloodlines_Prelude_I
- Bloodlines_Prelude_II
- CQU
- Comp_Mod
- CE_reborn
- LAbyNightV2
- Undisciplined_Caitiff
- War_Games
- TFN_reborn

When using Root Builder, each overhaul needs a target folder under the actual game installation, for example `<Game Path>\Unofficial_Patch` or `<Game Path>\CQM`. Remember that Root builder will clear anything out of the folder so you probably need to delete the Backup and Cache and then create that folders, then rebuild Root Builder.

---

## Profile Configuration (`bloodlines.ini`)

Location:

```
ModOrganizer2/profiles/<Profile Name>/bloodlines.ini
```

Auto-generated when creating a profile, but can be created manually.

### Example

```ini
[GAME]
; Game-data folder under the game directory; use the matching MO2 executable.
; Blank defaults to vampire.
GameData=Unofficial_Patch
```

---

## Configuration Reference

### GameData

Defines which game subdirectory is used as the active data root.

* Default → `{blank}`
* Blank → treated as `vampire`
* `Unofficial_Patch` → UP install
* Custom overhaul → use its folder name

---

### Profile-Specific Saves and INI Files

Enable **Profile-specific saves** and **Profile-specific game INI files** in MO2's profile settings to keep these files separate per profile without creating dedicated MO2 mods.

When profile-specific saves are enabled, MO2 stores saves in:

```text
ModOrganizer2/profiles/<Profile Name>/saves/
```

While the game runs, the plugin maps `<MO2>/profiles/<Profile Name>/saves/` to `<Game Path>/<GameData>/save/`. For example, an Unofficial Patch profile maps its saves to `<Game Path>/Unofficial_Patch/save/`. With profile-specific saves disabled, the game uses the game-data folder's `save` directory directly.

With profile-specific game INI files enabled, MO2 keeps `autoexec.cfg` and `user.cfg` in the profile folder and uses them in place of files under `<GameData>/cfg`. These filenames are registered by the plugin even when Root Builder keeps the source CFG files virtual.

`GameData` remains in `bloodlines.ini` because it identifies which game folder the profile uses. Save and CFG paths are managed by MO2's profile settings; there is no `ModName`, `Saves`, or `CfgMod` setting in the new INI format.

---

## Troubleshooting

### Game Does Not Launch

* Confirm the matching `Bloodlines - <folder>` executable is selected in MO2
* Verify the active profile's `GameData` folder exists under the game directory

---

### Mods Not Loading

* Verify correct `-game` argument
* Confirm mod folder exists in game directory
* Check `GameData` matches folder name

---

### Saves Not Detected

* Confirm save files exist
* Confirm **Profile-specific saves** is enabled if saves should be in the profile
* Confirm the matching `<Game Path>/<GameData>` target folder exists when using Root Builder
* Check the active profile's `saves` folder; existing Overwrite saves are not moved automatically

---

### Config Files Not Applied

* Confirm profile-specific game INI files are enabled in MO2
* Confirm `autoexec.cfg` and `user.cfg` exist in the active profile folder
* Check file permissions

---

## Contributing

Pull requests are accepted. For structural changes, open an issue first.

---

## License

GPL-3.0 License

---

## Acknowledgments

* Mod Organizer 2 team
* Bloodlines modding community
* Wesp5 (Unofficial Patch)
* Thanks to SulfurNitride for the Profile Executable Selector plugin.
* Thanks to the Wabbajack community, especially iAmMe, Gallahorn, Luca | EzioTheDeadPoet, iAmMascha, Swagmeister, Zeefa, Schrubbls, Neochiken, ShifuYaku, Kaeltis, Decimal, Miss Corruption, Scrab, and others for their help, encouragement, and patience.

---

## Support

* GitHub Issues
* iAmModlist Discord
