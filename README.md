# Bloodlines MO2 Plugin

Mod Organizer 2 plugin for *Vampire: The Masquerade – Bloodlines* with per-profile configuration and save management.

---

## Features

### Core Capabilities

* Automatic save location detection
* Per-profile configuration via `bloodlines.ini`
* Multiple save location support
* Supports:

  * Stock game
  * Unofficial Patch (UP / UP+)
  * Custom overhauls
* Native MO2 integration (no external launcher required)

---

## Components

### Required

* `game_vampirebloodlines.py`
  Provides Bloodlines support inside MO2.

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

1. Open MO2 → Executables → **Edit**

2. Add a new executable:
<<<<<<< HEAD
=======
   - **Title**: `Bloodlines Launcher` (or any name you prefer)
   - **Binary**: `[Path to your MO2]\bloodlines_launcher.bat`
   - **Arguments**: (leave blank or use window or fullscreen)
   - **Working Directory**: `[Path to your game installation]`
>>>>>>> 562112195e0c4a51f08d6e53f3bc089aeb47eca2

   * **Title**: `Bloodlines`
   * **Binary**: `<Game Path>\vampire.exe`
   * **Working Directory**: `<Game Path>`
   * **Arguments** (optional):

     ```
     -game Unofficial_Patch -window
     ```

3. (Optional) Create multiple executables for different overhauls
   Example:

   * `UP`
   * `CQM`
   * `Antitribu`

4. Profile-level configuration in `bloodlines.ini` will override executable arguments when present

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
GameData=Unofficial_Patch
Saves=Unofficial_Patch Plus Override
CfgMod=Unofficial_Patch Plus Override
Arguments=-game Unofficial_Patch -window
```

---

## Configuration Reference

### Arguments

Launch arguments passed to `vampire.exe`.

Typical usage:

* `-game <mod folder>` → selects overhaul
* `-window` → windowed mode

---

### GameData

Defines which subdirectory is treated as the active game data root.

* Blank → root `/vampire`
* `vampire` → vanilla structure
* `Unofficial_Patch` → UP install
* Custom overhaul → use its folder name

---

### Saves

Overrides save location.

Use cases:

* Separate saves per overhaul
* Redirect saves into MO2-managed mods

Behavior:

* Blank → automatic detection
* Set to mod name → saves written to that mod

Recommended:
Enable **"Create files in mod instead of overwrite"** for the executable when using this.

---

### CfgMod

Overrides configuration file location.

* Blank → automatic detection
* Set to mod name → isolates config per overhaul

---

## Recommendations

### 1. Use MO2-Native Execution Only

Avoid external launchers or batch wrappers.

Reasons:

* MO2 VFS injection is reliable with `vampire.exe`
* External launchers frequently break file virtualization
* Argument handling is already supported via:

  * Executables
  * `bloodlines.ini`

---

### 2. Prefer Profile-Level Configuration

Treat each overhaul as a separate MO2 profile.

Benefits:

* Isolated saves
* Isolated configs
* No argument conflicts
* Cleaner debugging

Minimum setup per profile:

```ini
GameData=<mod>
Arguments=-game <mod>
```

---

### 3. Use Profile Executable Selector (Recommended)

Use SulfurNitride’s plugin to bind executables per profile.

Purpose:

* Assign default executable per profile
* Hide irrelevant executables
* Remove manual switching overhead

This replaces older workflow patterns that relied on:

* Batch files
* Launcher scripts
* Manual argument switching

---

### 4. Keep Overhauls Physically Separate

Each overhaul should exist as its own directory inside the game folder:

```text
/vampire
/Unofficial_Patch
/CQM
/Antitribu_Mod
```

Do not merge or overlap directories.

---

### 5. Avoid `loader.exe`

Do not use `loader.exe` through MO2.

Reason:

* Known incompatibility with MO2’s virtual file system

Use:

```
vampire.exe -game <mod>
```

---

## Troubleshooting

### Game Does Not Launch

* Confirm `vampire.exe` is used
* Verify working directory is correct
* Check arguments for typos

---

### Mods Not Loading

* Verify correct `-game` argument
* Confirm mod folder exists in game directory
* Check `GameData` matches folder name

---

### Saves Not Detected

* Confirm save files exist
* Check `Saves` override setting
* Ensure MO2 overwrite behavior is configured correctly

---

### Config Files Not Applied

* Verify `CfgMod` value
* Confirm config files exist in expected location
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
