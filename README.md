# Bloodlines MO2 Plugin & Launcher

MO2 plugin for Vampire: The Masquerade - Bloodlines with per-profile configuration and save management.

## Features

### Plugin Features
- Automatic save location detection
- Per-profile configuration via bloodlines.ini
- Multiple save location support
- Stock game, Unofficial Patch, and custom mod support
- MO2 game management integration

### Launcher Features
- Reads game path from ModOrganizer.ini
- Current MO2 profile detection
- Profile-specific launch arguments
- Wabbajack modlist compatibility

## Components

### 1. MO2 Plugin (`game_vampirebloodlines.py`) (Required)
Provides Bloodlines game support in MO2.

### 2. Standalone Launcher (`bloodlines_launcher.bat`) (Optional)
Batch script for launching Bloodlines with profile-specific arguments. Designed for Wabbajack integration.

## Quick Start

Setup steps:

1. Copy `game_vampirebloodlines.py` to `ModOrganizer2/plugins/basic_games/games/`
2. Restart Mod Organizer 2
3. Select "Vampire - The Masquerade: Bloodlines" as managed game
4. Configure arguments in profile `bloodlines.ini` files as needed

## Installation

For complete installation:

### File Structure

```text
[MO2 Installation Directory]/
├── ModOrganizer.exe
└── plugins/                          # MO2 plugin files (required)
    └── basic_games/
        └── games/
            └── game_vampirebloodlines.py    # Required MO2 plugin file
├── bloodlines_launcher.bat           # Optional launcher
```

### Installation Steps
1. **Required**: Copy `game_vampirebloodlines.py` to `ModOrganizer2/plugins/basic_games/games/`
2. **Optional**: Copy `bloodlines_launcher.bat` to MO2 directory
3. Restart Mod Organizer 2
4. Select "Vampire - The Masquerade: Bloodlines" as managed game

## Setting Up the bloodlines_launcher.bat file in MO2

1. In MO2, go to the executable dropdown and select "Edit..."
2. Add a new executable:
   - **Title**: `Bloodlines Launcher` (or any name you prefer)
   - **Binary**: `[Path to your MO2]\bloodlines_launcher.bat`
   - **Arguments**: (leave blank)
   - **Working Directory**: `[Path to your game installation]`

## Setting up vampire.exe in MO2 if not using bloodlines_launcher.bat

1. In MO2, go to the executable dropdown and select "Edit..."
2. Add a new executable:
   - **Title**: `Bloodlines` (or any name you prefer)
   - **Binary**: `[Path to your game installation]\vampire.exe`
   - **Arguments**: Add your launch arguments here (e.g., `-game Unofficial_Patch -window`)
   - **Working Directory**: `[Path to your game installation]`
3. Create separate executables for different overhauls with different arguments
4. Configure profile-specific arguments in `bloodlines.ini` files to override executable settings

## bloodlines.ini Configuration

Create or edit `bloodlines.ini` in each profile directory:
`ModOrganizer2/profiles/[Profile Name]/bloodlines.ini`

The Bloodlines.ini should be auto created when you make a new profile in MO2 in the proper location but you can also manually create it if needed.

```ini
[GAME]
GameData=Unofficial_Patch
Saves=Unofficial_Patch Plus Override
CfgMod=Unofficial_Patch Plus Override
Arguments=-game Unofficial_Patch -window
```

### Arguments
Launch arguments for the game. Used by both the launcher script and MO2 direct launching.
This is normally used for Mod Folder switching with the -game argument or

**Common argument examples:**
- `-game Unofficial_Patch ` - Launch Unofficial Patch
- `-window` - Launch the game in windowed mode.

Arguments can be combined

### GameData
Specify a subdirectory for game data files.
- Leave blank to use the game root directory
- Set to "vampire" for stock game structure  
- Set to "Unofficial_Patch" when UP is installed in game folder
- If using another overhaul, check its documentation for the correct argument

### Saves
Override save game location with a specific mod in MO2.
- Mostly useful for keeping saves seperated between Overhauls
  - To do this use the "create files in mod instead of overwrite" on the exe in MO2
- Leave blank for automatic detection
- Set to mod name to use that mod's save directory

### CfgMod
Override configuration file location.
- Leave blank for automatic detection  
- Set to mod name to use that mod's cfg directory
- Mostly useful for keeping cfg seperated between Overhauls

## Troubleshooting

### Launcher Issues

#### Game not launching
1. Check that `ModOrganizer.ini` exists in your MO2 directory
2. Verify the game path in ModOrganizer.ini is correct
3. Ensure `vampire.exe` exists at the configured game path
4. Check the debug log at `%TEMP%\bloodlines_launcher_debug.log`

#### Wrong profile being detected
1. Make sure you've selected the correct profile in MO2 before running the launcher
2. Check that the profile has a `bloodlines.ini` file
3. Verify the profile name matches what's in ModOrganizer.ini

### General Issues

#### Loader.exe will not launch through MO2
MO2 has issues with launching this file through the Virtual File System. Use `vampire.exe` instead and set launch arguments:
- Use the launcher script (recommended)
- Or set arguments manually: `-game Unofficial_Patch -window`

#### Mods are not loading
- Ensure you're using the correct `-game` argument for your overhaul
- Check that the mod directory exists in your game folder
- Common overhauls: `Unofficial_Patch`, `CE_reborn`, `CQM`, `Antitribu_Mod`

### Plugin-Specific Issues (Full Installation Only)

#### Save Games Not Detected
1. Check that save files exist in expected locations
2. Verify GameData and Saves settings in bloodlines.ini
3. Ensure proper directory structure in game folder

#### Configuration Files Not Loading
1. Confirm CFG files exist in the detected directory
2. Check CfgMod setting in bloodlines.ini
3. Verify file permissions in game directories

### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## Acknowledgments

- The Mod Organizer 2 development team
- The Vampire: The Masquerade - Bloodlines modding community
- Wesp5 for the Unofficial Patch
- Everyone in the iAmModlist discord for all there help.

## Support

For issues, questions, or feature requests, please use the GitHub Issues page.

Or I can be found in the Fashionista Channels in this Discord

<https://discord.gg/iAmModlist>
