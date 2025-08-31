import os.path
from pathlib import Path
import platform
import re
import subprocess

import cffi

from _config import relative_path_to_libmgba_py, path_to_libmgba_py, path_to_mgba_build, path_to_mgba_root

source_files = [
    relative_path_to_libmgba_py / "vfs-py.c",
    relative_path_to_libmgba_py / "core.c",
    relative_path_to_libmgba_py / "log.c",
    relative_path_to_libmgba_py / "sio.c",
]

include_dirs = [
    path_to_libmgba_py,
    path_to_mgba_build / "include",
    path_to_mgba_root / "include",
    path_to_mgba_root / "src",
]

library_dirs = [
    path_to_libmgba_py,
]

if platform.system() == "Windows":
    include_dirs.append(path_to_mgba_build / "vcpkg" / "installed" / "x64-windows" / "include")
    library_dirs.append(path_to_mgba_build / "Release")

    os.environ["CL"] = "/DWIN32_LEAN_AND_MEAN"

    preprocessor_command = ["cl", "/P", "/DWIN32_LEAN_AND_MEAN", *(f"/I{str(path)}" for path in include_dirs)]
    subprocess.check_call(preprocessor_command + [str(path_to_libmgba_py / "_builder_cdef.h")])
    with open(path_to_libmgba_py / "_builder_cdef.i", "r") as file:
        preprocessed_header = file.read()
    os.remove(path_to_libmgba_py / "_builder_cdef.i")
else:
    if platform.system() == "Darwin":
        include_dirs.append(Path("/opt/homebrew/include"))
        include_dirs.append(Path("/usr/local/include"))
        library_dirs.append(Path("/usr/local/lib"))

    library_dirs.append(path_to_mgba_build)

    preprocessor_command = ["cc", "-E", *(f"-I{str(path)}" for path in include_dirs)]
    preprocessed_header = subprocess.check_output(
        preprocessor_command + [str(path_to_libmgba_py / "_builder_cdef.h")]).decode('utf-8')

blacklisted_lines = []
with open("_builder_blacklisted_lines.h", "r") as file:
    for line in file.readlines():
        line = line.strip()
        if line != '' and not line.startswith('//'):
            blacklisted_lines.append(line)

lines = []
last_line_was_empty = True
ignoring_lines = True

line_indicator_pattern = re.compile(r'^#(?:line)? \d+ "([^"]+)"(?: \d+)?$')

for line in preprocessed_header.splitlines():
    line = line.strip()
    line_indicator_result = line_indicator_pattern.match(line)
    if line_indicator_result:
        filename = line_indicator_result.group(1).replace('\\\\', '\\')
        ignoring_lines = (not filename.startswith(str(path_to_mgba_root))
                          and not filename.startswith(str(path_to_libmgba_py)))
        continue
    if ignoring_lines:
        continue
    if line.startswith('#') or line.startswith('__pragma') or line.startswith('__declspec('):
        continue
    if line == '':
        if last_line_was_empty:
            continue
        last_line_was_empty = True
    else:
        last_line_was_empty = False
    line = line.replace(';;', ';').replace('__declspec(dllimport)', '').replace('__declspec(noreturn)', '')
    for entry in blacklisted_lines:
        line = line.replace(entry, '')
    lines.append(line)

# with open(path_to_libmgba_py / "cdef.h", "w") as file:
#     file.write('\n'.join(lines))

ffi = cffi.FFI()
with open(path_to_libmgba_py / "_builder_source.h") as file:
    ffi.set_source("mgba._pylib", file.read(),
                   include_dirs=include_dirs,
                   libraries=["mgba"],
                   library_dirs=[str(path) for path in library_dirs],
                   sources=[str(path) for path in source_files])
ffi.cdef('\n'.join(lines))

if __name__ == "__main__":
    ffi.compile()
