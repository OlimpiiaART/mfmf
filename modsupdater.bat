@echo off

:: Set variables
set "repo=OlimpiiaART/mfmf"
set "tag=mods"
set "zip_filename=BepInEx.zip"
set "download_url=https://github.com/%repo%/releases/download/%tag%/%zip_filename%"
set "bepinex_folder=%cd%\BepInEx"
set "temp_folder=%TEMP%"

:: Check if the BepInEx folder exists
if exist "%bepinex_folder%" (
    echo BepInEx folder found

    if exist "%bepinex_folder%\config" (
        rmdir /S /Q "%bepinex_folder%\config"
        echo old config folder deleted
    )
    
    if exist "%bepinex_folder%\plugins" (
        rmdir /S /Q "%bepinex_folder%\plugins"
        echo old plugins folder deleted
    )

    echo.
    echo Downloading archive %zip_filename%...
    curl -L -o "%zip_filename%" %download_url%

    if exist "%zip_filename%" (
        echo.
        echo Archive downloaded successfully.
        echo.

        echo Extracting %zip_filename%...

        :: Extract archive to game root to avoid BepInEx\BepInEx
        tar -xf "%zip_filename%" -C "%cd%"
        
        if errorlevel 1 (
            echo Extraction failed. Please check the archive or try again.
            del /q "%zip_filename%"
            pause
            exit /b 1
        )

        echo Extraction completed
        echo.

        del /q "%zip_filename%"
    ) else (
        echo Failed to download the archive
    )
) else (
    echo BepInEx folder not found. Put the script in the root of the game
)

pause
