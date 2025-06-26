set GAME_FOLDER=D:\Plutonium\bo2
set OAT_BASE=D:\OpenAssetTools
set MOD_BASE=%cd%
set MOD_NAME=mp_raygun
"%OAT_BASE%\Linker.exe" ^
-v ^
--load "%GAME_FOLDER%\zone\all\zm_transit.ff" ^
--base-folder "%OAT_BASE%" ^
--asset-search-path "%MOD_BASE%" ^
--source-search-path "%MOD_BASE%\zone_source" ^
--output-folder "%MOD_BASE%\zone" ^ mod

if %ERRORLEVEL% NEQ 0 pause
set err=%ERRORLEVEL%

powershell -Command "Compress-Archive -Force -Path scripts,weapons,images,sound,materials -DestinationPath mod.zip"
powershell -Command "Rename-Item -Path mod.zip -NewName mod.iwd"

if %err% EQU 0 (
XCOPY "%MOD_BASE%\zone\mod.ff" "%LOCALAPPDATA%\Plutonium\storage\t6\mods\%MOD_NAME%\mod.ff" /Y
XCOPY "%MOD_BASE%\mod.iwd" "%LOCALAPPDATA%\Plutonium\storage\t6\mods\%MOD_NAME%\mod.iwd" /Y
XCOPY "%MOD_BASE%\zone\mod.all.sabl" "%LOCALAPPDATA%\Plutonium\storage\t6\mods\%MOD_NAME%\mod.all.sabl" /Y
XCOPY "%MOD_BASE%\mod.json" "%LOCALAPPDATA%\Plutonium\storage\t6\mods\%MOD_NAME%\mod.json" /Y
) ELSE (
COLOR C
echo FAIL!
)

pause