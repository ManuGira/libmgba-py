@echo off

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

REM Python bindings and create the wheel
copy mgba-script\*.py 
uv run setup.py build --build-lib build/win64
copy mgba-src\build\Release\*.dll build\win64\mgba

@echo on
@echo Done!
@echo Distributable files are located in `.\build\win64\mgba\`.
@echo off

