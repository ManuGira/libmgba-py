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

setup(
    version=version,
    packages=["mgba"],
    package_data={
        "mgba": ["*.pyd", "*.dll"],
    },
    include_package_data=True,
    cffi_modules=["_builder.py:ffi"],
)
