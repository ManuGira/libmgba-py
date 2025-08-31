@echo off

REM Ensure cl.exe is available
WHERE /q cl.exe
IF %ERRORLEVEL% NEQ 0 (
    echo cl.exe cannot be found in PATH. Is Visual Studio installed? Are you running the 'Native Tools Command Prompt'?
    EXIT /B 1
)

REM Ensure uv is available
WHERE /q uv.exe
IF %ERRORLEVEL% NEQ 0 (
    echo uv.exe cannot be found in PATH. See https://docs.astral.sh/uv/
    EXIT /B 1
)

REM Ensure mgba.dll is built
IF NOT EXIST mgba-src\build\Release\mgba.dll (
    echo mgba.dll not found. Did you run build_win64_dll.bat first?
    EXIT /B 1
)

REM Copy DLLs into package directory before building
mkdir mgba
copy mgba-py\*.py mgba\
copy mgba-src\build\Release\*.dll mgba\

REM Build wheel directly from pyproject.toml
uv run pip wheel --wheel-dir dist .

@echo on
@echo Done!
@echo Wheel file is located in the .\dist\ directory.
@echo off
