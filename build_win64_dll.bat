@echo off

REM mGBA version that should be checked out from the Git repository. Must be a valid Git ref.
:: get version from argument, default to 0.10.2
IF "%1"=="" (
    SET MGBA_VERSION=0.10.2
) ELSE (
    SET MGBA_VERSION=%1
)

WHERE /q git
IF %ERRORLEVEL% NEQ 0 (
    echo Git is not installed, or cannot be found in PATH.
    EXIT /B 1
)

WHERE /q cmake
IF %ERRORLEVEL% NEQ 0 (
    echo cmake cannot be found in PATH. Is Visual Studio installed? Are you running the 'Native Tools Command Prompt'?
    EXIT /B 1
)

WHERE /q msbuild
IF %ERRORLEVEL% NEQ 0 (
    echo msbuild cannot be found in PATH. Is Visual Studio installed? Are you running the 'Native Tools Command Prompt'?
    EXIT /B 1
)

PUSHD .

REM Download the mGBA sources so we can compile libmgba and its dlls
git clone https://github.com/mgba-emu/mgba.git mgba-src
REM git reset to version %MGBA_VERSION%
PUSHD mgba-src
git reset --hard %MGBA_VERSION%
REM set cmake minimum required to 3.5
powershell -Command "(Get-Content .\CMakeLists.txt) -replace 'cmake_minimum_required\(VERSION 3\.1\)', 'cmake_minimum_required(VERSION 3.5)' | Set-Content .\CMakeLists.txt"

mkdir build
REM clean previous build files except vcpkg
for /d %%D in ("build\*") do if /I not "%%~nxD"=="vcpkg" rd /s /q "%%D"
for %%F in ("build\*") do if /I not "%%~nxF"=="vcpkg" del /q "%%F"

PUSHD build
REM Download vcpkg because the version included in Visual Studio might not work
REM (that's the case as of 2023-09-22.)
git clone https://github.com/microsoft/vcpkg
call vcpkg\bootstrap-vcpkg.bat

REM Build mGBA (this also creates mgba.dll)
vcpkg\vcpkg.exe install ffmpeg[vpx,x264] libepoxy libpng libzip lua sdl2 sqlite3 --triplet=x64-windows
cmake -G "Visual Studio 17 2022" -A x64 -DCMAKE_TOOLCHAIN_FILE=./vcpkg/scripts/buildsystems/vcpkg.cmake -DBUILD_SHARED=ON -DBUILD_STATIC=ON -DUSE_FFMPEG=OFF -DUSE_DISCORD_RPC=OFF ..
msbuild ALL_BUILD.vcxproj /property:Configuration=Release

REM dlls build done
POPD
POPD
