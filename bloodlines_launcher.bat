@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "DEBUG_LOG=%TEMP%\bloodlines_launcher_debug.log"

echo [DEBUG] Script started at %date% %time% > "%DEBUG_LOG%"
echo [DEBUG] Script directory: %SCRIPT_DIR% >> "%DEBUG_LOG%"

:: Find vampire.exe from MO2's configuration
set "GAME_EXE="

echo [DEBUG] Looking for MO2 configuration to get game path... >> "%DEBUG_LOG%"

:: Look for MO2's main config file (ModOrganizer.ini)
set "MO2_CONFIG="
if exist "%SCRIPT_DIR%ModOrganizer.ini" (
    set "MO2_CONFIG=%SCRIPT_DIR%ModOrganizer.ini"
    echo [DEBUG] Found MO2 config: %SCRIPT_DIR%ModOrganizer.ini >> "%DEBUG_LOG%"
) else if exist "%SCRIPT_DIR%..\ModOrganizer.ini" (
    set "MO2_CONFIG=%SCRIPT_DIR%..\ModOrganizer.ini"
    echo [DEBUG] Found MO2 config: %SCRIPT_DIR%..\ModOrganizer.ini >> "%DEBUG_LOG%"
) else (
    echo [ERROR] ModOrganizer.ini not found >> "%DEBUG_LOG%"
    echo Error: Could not find ModOrganizer.ini file
    pause
    exit /b 1
)

:: Read the game path from MO2 config
echo [DEBUG] Reading MO2 configuration for game path... >> "%DEBUG_LOG%"
for /f "tokens=1,* delims==" %%a in ('type "%MO2_CONFIG%" 2^>nul') do (
    if /i "%%a"=="gamePath" (
        :: Extract game path from @ByteArray(GamePath) format
        set "GAME_PATH_LINE=%%b"
        set "GAME_PATH_LINE=!GAME_PATH_LINE:@ByteArray(=!"
        set "GAME_PATH_LINE=!GAME_PATH_LINE:)=!"
        :: Convert forward slashes to backslashes
        set "GAME_PATH_LINE=!GAME_PATH_LINE:/=\!"
        if exist "!GAME_PATH_LINE!\vampire.exe" (
            set "GAME_EXE=!GAME_PATH_LINE!\vampire.exe"
            echo [DEBUG] Found vampire.exe via MO2 config: !GAME_EXE! >> "%DEBUG_LOG%"
        )
    )
)

:: If game not found, exit with error
if "%GAME_EXE%"=="" (
    echo [ERROR] vampire.exe not found at MO2 configured path >> "%DEBUG_LOG%"
    echo Error: Could not find vampire.exe at the path configured in ModOrganizer.ini
    pause
    exit /b 1
)

:start_profile_detection
:: Find MO2 profiles directory
echo [DEBUG] Game found, continuing to profile detection... >> "%DEBUG_LOG%"

:: Check for portable/local MO2 profiles first (common in Wabbajack setups)
if exist "%SCRIPT_DIR%profiles" (
    set "PROFILES_DIR=%SCRIPT_DIR%profiles"
    echo [DEBUG] Found portable profiles at: %PROFILES_DIR% >> "%DEBUG_LOG%"
) else if exist "%SCRIPT_DIR%..\profiles" (
    set "PROFILES_DIR=%SCRIPT_DIR%..\profiles"  
    echo [DEBUG] Found profiles one level up: %PROFILES_DIR% >> "%DEBUG_LOG%"
) else if exist "%USERPROFILE%\AppData\Local\ModOrganizer\Vampire - Bloodlines\profiles" (
    set "PROFILES_DIR=%USERPROFILE%\AppData\Local\ModOrganizer\Vampire - Bloodlines\profiles"
    echo [DEBUG] Found profiles in user AppData: %PROFILES_DIR% >> "%DEBUG_LOG%"
) else if exist "%LOCALAPPDATA%\ModOrganizer\Vampire - Bloodlines\profiles" (
    set "PROFILES_DIR=%LOCALAPPDATA%\ModOrganizer\Vampire - Bloodlines\profiles"
    echo [DEBUG] Found profiles in local AppData: %PROFILES_DIR% >> "%DEBUG_LOG%"
) else (
    echo [ERROR] MO2 profiles directory not found >> "%DEBUG_LOG%"
    echo [DEBUG] Checked locations: >> "%DEBUG_LOG%"
    echo [DEBUG] - %SCRIPT_DIR%profiles >> "%DEBUG_LOG%"
    echo [DEBUG] - %SCRIPT_DIR%..\profiles >> "%DEBUG_LOG%"
    echo [DEBUG] - %USERPROFILE%\AppData\Local\ModOrganizer\Vampire - Bloodlines\profiles >> "%DEBUG_LOG%"
    echo [DEBUG] - %LOCALAPPDATA%\ModOrganizer\Vampire - Bloodlines\profiles >> "%DEBUG_LOG%"
    echo Error: Could not find MO2 profiles directory
    pause
    exit /b 1
)

echo [DEBUG] Profiles directory: %PROFILES_DIR% >> "%DEBUG_LOG%"

:: Read the selected profile from the same MO2 config
echo [DEBUG] Reading MO2 configuration for selected profile... >> "%DEBUG_LOG%"

for /f "tokens=1,* delims==" %%a in ('type "%MO2_CONFIG%" 2^>nul') do (
    if /i "%%a"=="selected_profile" (
        :: Extract profile name from @ByteArray(ProfileName) format
        set "PROFILE_LINE=%%b"
        set "PROFILE_LINE=!PROFILE_LINE:@ByteArray(=!"
        set "PROFILE_LINE=!PROFILE_LINE:)=!"
        set "LATEST_PROFILE=!PROFILE_LINE!"
        echo [DEBUG] Found selected_profile: !LATEST_PROFILE! >> "%DEBUG_LOG%"
    )
)

:: If no profile found, fall back to first available
if "%LATEST_PROFILE%" == "" (
    echo [DEBUG] No profile found in MO2 config, using first available... >> "%DEBUG_LOG%"
    for /d %%p in ("%PROFILES_DIR%\*") do (
        if exist "%%p\bloodlines.ini" (
            set "LATEST_PROFILE=%%~nxp"
            echo [DEBUG] Using fallback profile: %%~nxp >> "%DEBUG_LOG%"
            goto profile_found
        )
    )
)

:profile_found
if "%LATEST_PROFILE%" == "" (
    echo [ERROR] No profiles with bloodlines.ini found >> "%DEBUG_LOG%"
    echo Error: No MO2 profiles found with bloodlines.ini
    pause
    exit /b 1
)

echo [DEBUG] Selected profile: %LATEST_PROFILE% >> "%DEBUG_LOG%"

:: Read arguments from the selected profile's bloodlines.ini
set "PROFILE_DIR=%PROFILES_DIR%\%LATEST_PROFILE%"
set "INI_FILE=%PROFILE_DIR%\bloodlines.ini"
set "ARGUMENTS="
set "SAVES_MOD="

echo [DEBUG] Reading from: %INI_FILE% >> "%DEBUG_LOG%"

if exist "%INI_FILE%" (
    for /f "usebackq tokens=1,* delims==" %%a in ("%INI_FILE%") do (
        if /i "%%a"=="Arguments" (
            :: Trim leading spaces
            for /f "tokens=*" %%c in ("%%b") do set "ARGUMENTS=%%c"
            echo [DEBUG] Found arguments: [!ARGUMENTS!] >> "%DEBUG_LOG%"
        )
        if /i "%%a"=="Saves" (
            :: Trim leading spaces
            for /f "tokens=*" %%c in ("%%b") do set "SAVES_MOD=%%c"
            echo [DEBUG] Found Saves mod: [!SAVES_MOD!] >> "%DEBUG_LOG%"
        )
    )
) else (
    echo [ERROR] bloodlines.ini not found in profile directory >> "%DEBUG_LOG%"
)

:: ----- accept mode arg (window default) and append to arguments -----
set "MODE=window"
if not "%~1"=="" (
    if /i "%~1"=="fullscreen" (
        set "MODE=fullscreen"
    ) else if /i "%~1"=="window" (
        set "MODE=window"
    )
)
if not "!ARGUMENTS!"=="" (
    set "ARGUMENTS=!ARGUMENTS! -%MODE%"
) else (
    set "ARGUMENTS=-%MODE%"
)

:: Handle Saves mod folder if specified
if not "%SAVES_MOD%"=="" (
    echo [DEBUG] Saves mod specified: %SAVES_MOD% >> "%DEBUG_LOG%"
    
    :: Find MO2's mods directory
    set "MODS_DIR="
    if exist "%SCRIPT_DIR%mods" (
        set "MODS_DIR=%SCRIPT_DIR%mods"
        echo [DEBUG] Found mods directory: %SCRIPT_DIR%mods >> "%DEBUG_LOG%"
    ) else if exist "%SCRIPT_DIR%..\mods" (
        set "MODS_DIR=%SCRIPT_DIR%..\mods"
        echo [DEBUG] Found mods directory: %SCRIPT_DIR%..\mods >> "%DEBUG_LOG%"
    ) else (
        echo [DEBUG] Could not find MO2 mods directory >> "%DEBUG_LOG%"
        echo [ERROR] Saves mod specified but mods directory not found
        pause
        exit /b 1
    )
    
    set "TARGET_MOD_DIR=!MODS_DIR!\!SAVES_MOD!"
    echo [DEBUG] Checking for mod directory: !TARGET_MOD_DIR! >> "%DEBUG_LOG%"
    echo [DEBUG] MODS_DIR: !MODS_DIR! >> "%DEBUG_LOG%"
    echo [DEBUG] SAVES_MOD: !SAVES_MOD! >> "%DEBUG_LOG%"
    
    :: List what's actually in the mods directory for debugging
    echo [DEBUG] Contents of mods directory: >> "%DEBUG_LOG%"
    for /d %%d in ("!MODS_DIR!\*") do (
        echo [DEBUG] - %%~nxd >> "%DEBUG_LOG%"
    )
    
    :: Check if the mod directory exists
    if not exist "!TARGET_MOD_DIR!" (
        echo [ERROR] Saves mod directory does not exist: !TARGET_MOD_DIR! >> "%DEBUG_LOG%"
        echo [ERROR] Mod directory '!SAVES_MOD!' not found in MO2 mods folder
        echo [ERROR] Please create the mod in MO2 first or check the Saves setting in bloodlines.ini
        echo [DEBUG] Check debug log for directory listing: %DEBUG_LOG%
        pause
        exit /b 1
    )
    
    echo [INFO] Using mod folder for saves: %SAVES_MOD%
    echo [INFO] Files will be created in: !TARGET_MOD_DIR!
)

:: Launch the game with whatever arguments we have (empty is fine)
echo [DEBUG] Launching game with arguments: [!ARGUMENTS!] >> "%DEBUG_LOG%"
echo Launching Vampire: The Masquerade - Bloodlines (Profile: %LATEST_PROFILE%)
if not "!ARGUMENTS!"=="" echo Arguments: !ARGUMENTS!
echo [DEBUG] Launch command: "%GAME_EXE%" !ARGUMENTS! >> "%DEBUG_LOG%"
timeout /t 2 /nobreak >nul
echo [DEBUG] Executing game launch now >> "%DEBUG_LOG%"
"%GAME_EXE%" !ARGUMENTS!
echo [DEBUG] Game exited >> "%DEBUG_LOG%"

:launch_complete

echo [DEBUG] Script completed >> "%DEBUG_LOG%"

exit /b 0