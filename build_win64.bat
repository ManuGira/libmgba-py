@echo off

REM Run this script from a 'Native Tools Command Prompt for VS 2022' or similar.

SET MGBA_VERSION_LIST=0.10.5
SET PYTHON_VERSION_LIST=3.13

FOR %%M IN (%MGBA_VERSION_LIST%) DO (
    REM call build_win64_dll.bat %%M

    FOR %%P IN (%PYTHON_VERSION_LIST%) DO (   
        call build_win64_whl.bat %%P
    )
)

