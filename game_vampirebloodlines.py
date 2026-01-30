from pathlib import Path
from typing import List

import mobase
from PyQt6.QtCore import QDir

from ..basic_game import BasicGame, BasicGameSaveGame


class VampireModDataChecker(mobase.ModDataChecker):
    def __init__(self):
        super().__init__()
        self.validDirNames = [
            "cfg",
            "cl_dlls",
            "dlg",
            "dlls",
            "maps",
            "materials",
            "media",
            "models",
            "particles",
            "python",
            "resource",
            "scripts",
            "sound",
            "vdata",
        ]

    def dataLooksValid(
        self, filetree: mobase.IFileTree
    ) -> mobase.ModDataChecker.CheckReturn:
        for entry in filetree:
            if not entry.isDir():
                continue
            if entry.name().casefold() in self.validDirNames:
                return mobase.ModDataChecker.VALID
        return mobase.ModDataChecker.INVALID


class VampireSaveGame(BasicGameSaveGame):
    _filepath: Path

    def __init__(self, filepath: Path):
        super().__init__(filepath)
        self._filepath = filepath
        self.name = None
        self.elapsedTime = None


class VampireTheMasqueradeBloodlinesGame(BasicGame):
    Name = "Vampire - The Masquerade: Bloodlines Support Plugin"
    Author = "iunpause"
    Version = "1.0.1"
    Description = "Adds support for Vampires: The Masquerade - Bloodlines"

    GameName = "Vampire - The Masquerade: Bloodlines"
    GameShortName = "vampirebloodlines"
    GameNexusName = "vampirebloodlines"
    GameNexusId = 437
    GameSteamId = [2600]
    GameGogId = [1207659240]
    GameBinary = "vampire.exe"
    GameDataPath = ""
    GameDocumentsDirectory = "%GAME_PATH%/vampire/cfg"
    GameSavesDirectory = "%GAME_PATH%/vampire/SAVE"
    GameSaveExtension = "sav"
    GameSupportURL = (
        r"https://github.com/daulvec/Bloodlines_MO2_Plugin"
        "Game:-Vampire:-The-Masquerade-%E2%80%90-Bloodlines"
    )

    def init(self, organizer: mobase.IOrganizer) -> bool:
        super().init(organizer)
        self._register_feature(VampireModDataChecker())
        return True

    def initializeProfile(self, directory: QDir, settings: mobase.ProfileSetting):
        # Create Bloodlines.ini vars
        profile_path = Path(directory.absolutePath())
        ini_path = profile_path / "bloodlines.ini"

        # Create the file if it doesn't exist
        if not ini_path.exists():
            ini_path.write_text(
                "[GAME]\n"
                "GameData=\n"
                "Saves=\n"
                "CfgMod=\n",
                encoding="utf-8",
            )

        super().initializeProfile(directory, settings)

    # Helper method to read GameData from bloodlines.ini
    def _read_game_data_from_ini(self) -> str:
        ini_path = Path(self._organizer.profilePath()) / "bloodlines.ini"

        if not ini_path.exists():
            return ""

        game_data = ""

        with ini_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GameData="):
                    game_data = line[len("GameData=") :].strip()
                    break

        return game_data

    def _read_saves_mod_from_ini(self) -> str:
        
        ini_path = Path(self._organizer.profilePath()) / "bloodlines.ini"

        if not ini_path.exists():
            return ""

        saves_mod = ""

        with ini_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("Saves="):
                    saves_mod = line[len("Saves=") :].strip()
                    break

        return saves_mod

    def _read_cfg_mod_from_ini(self) -> str:
        ini_path = Path(self._organizer.profilePath()) / "bloodlines.ini"

        if not ini_path.exists():
            return ""

        cfg_mod = ""

        with ini_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("CfgMod="):
                    cfg_mod = line[len("CfgMod=") :].strip()
                    break

        return cfg_mod

    def dataDirectory(self) -> QDir:
        game_data = self._read_game_data_from_ini()
        
        # If GameData is blank, use the game directory root
        if not game_data:
            return self.gameDirectory()

        return QDir(self.gameDirectory().absoluteFilePath(game_data))

    def savesDirectory(self) -> QDir:

        saves_mod = self._read_saves_mod_from_ini()
        
        if saves_mod:
            mods_path = Path(self._organizer.modsPath()) / saves_mod / "save"
            return QDir(str(mods_path))
        
        game_data = self._read_game_data_from_ini()

        # If GameData is blank, check common save locations in order of preference
        if not game_data:
            # Check for common save directories
            potential_save_dirs = [
                "Unofficial_Patch/save",  # Unofficial Patch location
                "vampire/save",           # Stock game location  
                "save",                   # Root save location
            ]
            
            for save_dir in potential_save_dirs:
                save_path = Path(self.gameDirectory().absolutePath()) / save_dir
                if save_path.exists():
                    return QDir(str(save_path))
            
            # If none exist, default to vampire/save for new saves
            fallback = self.gameDirectory().absoluteFilePath("vampire/save")
            return QDir(fallback)

        # If GameData has a value, use it as before
        virtual_path = f"{game_data}/save"
        real_path = self._organizer.resolvePath(virtual_path)

        if real_path:
            return QDir(real_path)

        fallback = self.gameDirectory().absoluteFilePath(virtual_path)
        return QDir(fallback)

    def version(self):
        # Don't forget to import mobase!
        return mobase.VersionInfo(1, 0, 0, mobase.ReleaseType.FINAL)

    def iniFiles(self):
        cfg_mod = self._read_cfg_mod_from_ini()
        
        if cfg_mod:
            # Use specific cfg mod directory
            cfg_path = Path(self._organizer.modsPath()) / cfg_mod / "cfg"
        else:
            # Use the detected documents directory (which has the dynamic detection logic)
            cfg_path = Path(self.documentsDirectory().absolutePath())
        
        cfg_files = []
        if cfg_path.exists():
            cfg_files = [f.name for f in cfg_path.glob("*.cfg") if f.is_file()]
        
        return cfg_files if cfg_files else []

    def listSaves(self, folder: QDir) -> List[mobase.ISaveGame]:
        ext = self._mappings.savegameExtension.get()
        return [
            VampireSaveGame(path)
            for path in Path(folder.absolutePath()).glob(f"*.{ext}")
        ]

    def documentsDirectory(self) -> QDir:
        cfg_mod = self._read_cfg_mod_from_ini()
        
        if cfg_mod:
            cfg_path = Path(self._organizer.modsPath()) / cfg_mod / "cfg"
            return QDir(str(cfg_path))
        
        game_data = self._read_game_data_from_ini()
        
        # If GameData is blank, check common cfg locations in order of preference
        if not game_data:
            # Check for common cfg directories (Unofficial Patch first)
            potential_cfg_dirs = [
                "Unofficial_Patch/cfg",  # Unofficial Patch location (check first)
                "vampire/cfg",           # Stock game location
                "cfg",                   # Root cfg location
            ]
            
            for cfg_dir in potential_cfg_dirs:
                cfg_path = Path(self.gameDirectory().absolutePath()) / cfg_dir
                if cfg_path.exists():
                    return QDir(str(cfg_path))
            
            # If none exist, default to vampire/cfg
            fallback = self.gameDirectory().absoluteFilePath("vampire/cfg")
            return QDir(fallback)
        
        # If GameData has a value, use it as before
        return QDir(self.gameDirectory().absoluteFilePath(f"{game_data}/cfg"))
