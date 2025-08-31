mGBA Python Bindings
=====================

This is a fork of Hanzi's [libmgba-py](https://github.com/hanzi/libmgba-py) project, which itself is a fork of the Python bindings of the [mGBA repository](https://github.com/mgba-emu/mgba/tree/master/src/platform/python)
with some modifications to get it to build easily on my machine.

The main changes I (ManuGira) added to Hanzi's version are:
- Added python venv maintained with `uv` from [Astral](https://docs.astral.sh/uv/)
- Split the build_win64.bat script into two scripts:
  - `build_win64_dll.bat` to build the libmgba dlls
  - `build_win64_whl.bat` to build the python bindings and create the wheel
- Fixed some path issues in `_builder.py` to get it to build on my machine
- Generate a wheel file for easier distribution. The wheel file can be installed in other python projects using `pip install <path-to-wheel-file>`
- Removed the linux and macOS build scripts, as I don't need them. See the original repository if you need them.
- Added the `.vscode/settings.json` file to be able to open the **x64 Native Tools Command Prompt** from within **VS Code**.


## What this is (and isn't)

This provides Python bindings to libmgba, which is a library of
functions that mGBA uses internally.

Thus, you can use it to create a 'headless' emulator instance and
interact with its internal functions using Python.

It does **not** come with any GUI, i.e. you can't use it to just
remote control an instance of the mGBA emulator.


## Build Instructions (Windows 64-bit only)

### Prequisites

Heads up: This will require a couple of GB of disk space.

1. Have [Visual Studio](https://visualstudio.microsoft.com/vs/community/) installed (the free Community Edition is enough.)
1. Have [uv from Astral](https://docs.astral.sh/uv/) installed and available in your PATH.
1. Have [Git](https://git-scm.com/download/win) installed.
1. Download this repository to somewhere on your hard drive (using `git clone` or by just downloading it as a ZIP file.)

The build scripts need to be run from a special command prompt that
comes with Visual Studio. You can either open it from the **Start menu** or from **VS Code** (see the note below.)

#### Opening the **x64 Native Tools Command Prompt** from Start menu

   1. Open the Start menu, look for the `Visual Studio 2022` directory, and run the `x64 Native Tools Command Prompt`.
   1. Navigate to wherever you have extracted this repository (e.g. `cd /D C:\Users\someone\Desktop\libmgba-py`.)


Afterwards, distributable files should be available in the `build\win64\mgba` directory. You can copy that entire directory into your Python project, or create a package from it.

#### Opening the **x64 Native Tools Command Prompt** from VS Code

The `.vscode\settings.json` is set up to allow you to open the `x64 Native Tools Command Prompt` from within VS Code. You need to modify the path to `vcvars64.bat` in the `settings.json` file to match your Visual Studio installation:

```json
"terminal.integrated.profiles.windows": {
   "VS2022 Native Tools": {
      "path": "C:\\Windows\\System32\\cmd.exe",
      "args": [
            "/k",
            "C:\\Program Files\\Microsoft Visual tudio\\2022\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat"  // <-- MODIFY THIS PATH TO MATCH YOUR INSTALLATION
      ]
   }
},
"terminal.integrated.defaultProfile.windows": "VS2022 Native Tools"
```
 Open the `x64 Native Tools Command Prompt` from within VS Code by using the `Terminal > New Terminal` menu option.

> Note: the main advantage of opening the command prompt from within VS Code is that is it will open in the current folder, so you don't have to `cd` to the right folder.

### Building mGBA's dlls
Open current folder in the `x64 Native Tools Command Prompt` (see above.) and run the `build_win64_dll.bat`

This will automatically:
 - Download the mGBA sources to `mgba-src` folder
 - Download **vcpkg** to `mgba-src/build/vcpkg`
 - Install dependencies with **vcpkg**
 - build libmgba and its dlls
 
Resulting dlls will be located into the `mgba-src/build/Release` folder.

### Building mGBA's python wheel file
> The dlls built in the previous step are needed to build the python bindings and create the wheel file.

Open current folder in the `x64 Native Tools Command Prompt` (see above.) and run the `build_win64_whl.bat`

## License

This code was taken from the offical mGBA repository and only modified
a bit, so [the original license terms](https://github.com/mgba-emu/mgba/#copyright)
apply:

> mGBA is Copyright © 2013 – 2023 Jeffrey Pfau.
> 
> It is distributed under the Mozilla Public License version 2.0.  
> A copy of the license is available in the distributed LICENSE file.
