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

print("--- DATA FILES ---")
print(data_files)
print("------------------")

setup(
    name="mgba",
    version=version,
    author="Jeffrey Pfau",
    author_email="jeffrey@endrift.com",
    url="http://github.com/mgba-emu/mgba/",
    packages=["mgba"],
    package_data={
        "mgba": ["*.pyd", "*.dll"],
    },
    include_package_data=True,
    setup_requires=['cffi>=1.6'],
    install_requires=['cffi>=1.6'],
    extras_require={'pil': ['Pillow>=2.3']},
    cffi_modules=["_builder.py:ffi"],
    license="MPL 2.0",
    #data_files=data_files,
    classifiers=[
        "Programming Language :: C",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Topic :: Games/Entertainment",
        "Topic :: System :: Emulators"
    ]
)
