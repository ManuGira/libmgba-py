import os
import platform
from pathlib import Path

relative_path_to_libmgba_py = Path(".")
path_to_libmgba_py = relative_path_to_libmgba_py.absolute()

if platform.system() in ("Windows", "Darwin"):
    path_to_mgba_root = Path("./mgba-src").absolute()
    path_to_mgba_build = Path("./mgba-src/build").absolute()
elif platform.system() == "Linux":
    # This only works for Ubuntu-based Docker images provided by the mGBA project
    # see: https://hub.docker.com/r/mgba/ubuntu/tags
    build_directory = os.environ["BUILD_DIR"]

    path_to_mgba_root = Path("/home/mgba/src")
    path_to_mgba_build = Path(f"/home/mgba/src/{build_directory}")
else:
    raise RuntimeError("Unsupported platform: " + platform.system())
