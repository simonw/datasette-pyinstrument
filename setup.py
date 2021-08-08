from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-pyinstrument",
    description="Use pyinstrument to analyze Datasette page performance",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-pyinstrument",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-pyinstrument/issues",
        "CI": "https://github.com/simonw/datasette-pyinstrument/actions",
        "Changelog": "https://github.com/simonw/datasette-pyinstrument/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_pyinstrument"],
    entry_points={"datasette": ["pyinstrument = datasette_pyinstrument"]},
    install_requires=["datasette", "pyinstrument"],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
    tests_require=["datasette-pyinstrument[test]"],
    python_requires=">=3.7",
)
