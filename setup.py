import numpy as np
import pathlib
import re
from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

ext = Extension(
    "chess._movegen",
    sources=[
        "src/chess/_movegen/__init__.pyx",
        "src/chess/_movegen/src/cmovegen.cpp",
    ],
    include_dirs=[np.get_include()],
    language="c++",
)

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# A file containing the __version__ variable.
VERSIONFILE = "src/chess/__init__.py"

try:
    __version__ = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", open(VERSIONFILE, "rt").read(), re.M
    ).group(1)
except Exception as exception:
    raise RuntimeError(f"Unable to find version string in {VERSIONFILE}") from exception


setup(
    name="chess",
    author="Troels Lægsgaard",
    version=__version__,
    description=("A small chess engine."),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/laegsgaardTroels/chess",
    package_dir={"": "src"},
    packages=find_packages(
        where="src",
        include=["chess*"],
    ),
    python_requires=">=3.9",
    install_requires=[
        "Cython==3.0.2",
        "numpy==1.26.0",
    ],
    extras_require={
        "dev": [
            "flake8==3.8.3",
            "jupyterlab==4.2.2",
            "pytest-cov",
            "pytest-pep8",
            "pytest==8.0.2",
            "sphinx==7.2.6",
        ]
    },
    ext_modules=cythonize([ext]),
    entry_points={
        "console_scripts": [
            "chess = chess.__main__:main",
        ]
    },
)
