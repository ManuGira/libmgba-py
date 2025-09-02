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

REM Python versions to build wheels for
IF "%1"=="" (
    SET PYTHON_VERSION=3.13
) ELSE (
    SET PYTHON_VERSION=%1
)

echo.
echo ===============================
echo Building wheel with Python %PYTHON_VERSION%
echo ===============================

REM Pin Python version
uv python pin %PYTHON_VERSION%

REM Clean previous build
rmdir /s /q build
rmdir /s /q mgba
rmdir /s /q Release
rmdir /s /q mgba.egg-info
mkdir mgba

REM Copy source files and DLLs
copy mgba-py\*.py mgba\
copy mgba-src\build\Release\*.dll mgba\

REM Build wheel
uv run setup.py bdist_wheel

@echo on
@echo Done!
@echo Wheel file is located in the .\dist\ directory.
@echo All done!
@echo Wheels are located in the .\dist\ directory.
@echo off
