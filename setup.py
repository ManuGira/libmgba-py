import platform
import subprocess

from setuptools import setup

from _config import path_to_mgba_root, path_to_mgba_build


def get_version_var(piece):
    env = None
    if platform.system() == "Windows":
        env = {"PWD": path_to_mgba_build.as_posix()}
    return subprocess.check_output(
        [
            'cmake',
            '-DPRINT_STRING={}'.format(piece),
            '-P',
            (path_to_mgba_root / 'version.cmake').as_posix()
        ],
        env=env
    ).decode('utf-8').strip()


version = '.'.join([
    get_version_var('LIB_VERSION_MAJOR'),
    get_version_var('LIB_VERSION_MINOR'),
    get_version_var('LIB_VERSION_PATCH')
])

data_files = None
if platform.system() == "Windows":
    data_files = {"mgba": []}
    for file in (path_to_mgba_build / "Release").glob("*.dll"):
        # Chemin relatif à setup.py, destination dans le dossier mgba du package
        rel_path = str(("mgba-src/build/Release/" + file.name).replace("\\", "/"))
        data_files["mgba"].append(rel_path)


setup(
    version=version,
    packages=["mgba"],
    package_data={
        "mgba": ["*.pyd", "*.dll"],
    },
    include_package_data=True,
    cffi_modules=["_builder.py:ffi"],
)
