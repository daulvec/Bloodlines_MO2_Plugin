# Bloodlines MO2 Plugin

A comprehensive Mod Organizer 2 plugin for **Vampire: The Masquerade - Bloodlines** that provides advanced game management and configuration options.

## Features

### Dynamic Directory Detection
- **Save Games**: Automatically detects save locations across different setups (Unofficial Patch, stock game, custom installations)
- **Configuration Files**: Dynamically finds CFG files in the appropriate directories
- **Game Data**: Flexible game data path configuration through bloodlines.ini

### Flexible Configuration
- **Profile-specific settings**: Each MO2 profile gets its own bloodlines.ini configuration file
- **Multiple install support**: Works with stock game, Unofficial Patch, and custom mod configurations
- **RTX mod compatibility**: Supports complex setups where mods are installed directly to game folder

### Advanced Save Management
- Detects saves in multiple locations automatically:
  - Unofficial_Patch/save (for UP installed in game folder)
  - vampire/save (stock game location)
  - Custom mod-specific save directories
- Supports .sav file format with proper metadata handling

## Installation

1. Download the latest release or clone this repository
2. Copy the plugin files to your Mod Organizer 2 plugins directory:
   ```
   ModOrganizer2/plugins/
   ```
3. Restart Mod Organizer 2
4. Select "Vampire - The Masquerade: Bloodlines" as your managed game

## Configuration

### bloodlines.ini Settings

The plugin creates a `bloodlines.ini` file in each profile with the following options:

```ini
[GAME]
GameData=
Saves=
CfgMod=
```

**GameData**: Specify a subdirectory for game data files
- Leave blank to use the game root directory
- Set to "vampire" for stock game structure  
- Set to "Unofficial_Patch" when UP is installed in game folder

**Saves**: Override save game location with a specific mod
- Leave blank for automatic detection
- Set to mod name to use that mod's save directory

**CfgMod**: Override configuration file location
- Leave blank for automatic detection  
- Set to mod name to use that mod's cfg directory

## Supported Game Versions

- Steam version (App ID: 2600)
- GOG version (ID: 1207659240)
- Retail/disc versions

## Supported Mods

- Unofficial Patch (all versions)
- Clan Quest Mod
- Final Nights
- And many others through flexible directory detection

## Usage Examples

### Stock Game Setup
Leave all bloodlines.ini settings blank - the plugin will automatically detect the standard vampire/ directories.

### Unofficial Patch in Game Folder
Leave GameData blank - the plugin will automatically detect Unofficial_Patch/save and Unofficial_Patch/cfg directories.

### Custom Mod Configuration
Set GameData to your desired subdirectory name for complete control over file locations.

## Requirements

- Mod Organizer 2 (version 2.4.0 or later)
- Vampire: The Masquerade - Bloodlines (any version)
- Python 3.8+ (included with MO2)

## Troubleshooting

### Save Games Not Detected
1. Check that save files exist in expected locations
2. Verify bloodlines.ini settings in your profile directory
3. Ensure proper directory structure in game folder

### Configuration Files Not Loading
1. Confirm CFG files exist in the detected directory
2. Check CfgMod setting in bloodlines.ini
3. Verify file permissions in game directories

## Development

### Building from Source
1. Clone the repository
2. Ensure you have the MO2 plugin development environment set up
3. Copy files to your MO2 plugins directory for testing

### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## Acknowledgments

- The Mod Organizer 2 development team
- The Vampire: The Masquerade - Bloodlines modding community
- Wesp5 for the Unofficial Patch

## Support

For issues, questions, or feature requests, please use the GitHub Issues page.

