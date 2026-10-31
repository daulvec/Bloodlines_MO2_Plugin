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


class VampireLocalSavegames(mobase.LocalSavegames):
    def __init__(self, game: "VampireTheMasqueradeBloodlinesGame"):
        super().__init__()
        self._game = game

    def mappings(self, profile_save_dir: QDir):
        return [
            mobase.Mapping(
                source=profile_save_dir.absolutePath(),
                destination=self._game.savesDirectory().absolutePath(),
                is_directory=True,
                create_target=True,
            )
        ]

    def prepareProfile(self, profile: mobase.IProfile) -> bool:
        return profile.localSavesEnabled()


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
    Version = "1.1.0"
    Description = "Adds support for Vampires: The Masquerade - Bloodlines"

    GameName = "Vampire - The Masquerade: Bloodlines"
    GameShortName = "vampirebloodlines"
    GameNexusName = "vampirebloodlines"
    GameNexusId = 437
    GameSteamId = [2600]
    GameGogId = [1207659240]
    GameBinary = "vampire.exe"
    GameDataPath = "vampire"
    GameSaveExtension = "sav"
    GameSupportURL = (
        r"https://github.com/daulvec/Bloodlines_MO2_Plugin/wiki/"
        "Game:-Vampire:-The-Masquerade-%E2%80%90-Bloodlines"
    )

    def init(self, organizer: mobase.IOrganizer) -> bool:
        super().init(organizer)
        self._register_feature(VampireModDataChecker())
        self._register_feature(VampireLocalSavegames(self))
        return True

    def initializeProfile(self, directory: QDir, settings: mobase.ProfileSetting):
        # Create Bloodlines.ini vars
        profile_path = Path(directory.absolutePath())
        ini_path = profile_path / "bloodlines.ini"

        # Create the file if it doesn't exist
        if not ini_path.exists():
            ini_path.write_text(
                "[GAME]\n"
                "; Game-data folder under the game directory; use the matching MO2 executable.\n"
                "; Blank defaults to vampire.\n"
                "GameData=\n",
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

    def dataDirectory(self) -> QDir:
        game_data = self._read_game_data_from_ini()
        return QDir(
            self.gameDirectory().absoluteFilePath(game_data or self.GameDataPath)
        )

    def savesDirectory(self) -> QDir:
        game_data = self._read_game_data_from_ini() or self.GameDataPath
        virtual_path = f"{game_data}/save"
        real_path = self._organizer.resolvePath(virtual_path)

        if real_path:
            return QDir(real_path)

        fallback = self.gameDirectory().absoluteFilePath(virtual_path)
        return QDir(fallback)

    def version(self):
        return mobase.VersionInfo(1, 1, 0, mobase.ReleaseType.FINAL)

    def iniFiles(self):
        return ["autoexec.cfg", "user.cfg"]

    def listSaves(self, folder: QDir) -> List[mobase.ISaveGame]:
        ext = self._mappings.savegameExtension.get()
        return [
            VampireSaveGame(path)
            for path in Path(folder.absolutePath()).glob(f"*.{ext}")
        ]

    def documentsDirectory(self) -> QDir:
        game_data = self._read_game_data_from_ini() or self.GameDataPath
        return QDir(self.gameDirectory().absoluteFilePath(f"{game_data}/cfg"))
