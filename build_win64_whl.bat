@echo off

REM Ensure that we are running in the right environment
WHERE /q cl.exe
IF %ERRORLEVEL% NEQ 0 (
    echo cl.exe cannot be found in PATH. Is Visual Studio installed? Are you running the 'Native Tools Command Prompt'?
    EXIT /B 1
)

WHERE /q uv.exe
IF %ERRORLEVEL% NEQ 0 (
    echo uv.exe cannot be found in PATH. See https://docs.astral.sh/uv/
    EXIT /B 1
)

REM Ensure that mgba-src/build/Release contains the dlls built by build_win64_dll.bat
IF NOT EXIST mgba-src\build\Release\mgba.dll (
    echo mgba.dll not found. Did you run build_win64_dll.bat first?
    EXIT /B 1
)

REM Build Python bindings and create the wheel
uv run setup.py build --build-lib build\win64
copy mgba-src\build\Release\*.dll build\win64\mgba
uv run python -m build --wheel --outdir build\win64

@echo on
@echo Done!
@echo Distributable files are located in `.\build\win64\mgba\`.
@echo off

