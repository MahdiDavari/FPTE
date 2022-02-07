"""setup file for FPTE pkg
"""
import sys

from setuptools import setup, find_packages

from .src import FPTE
from .src.FPTE import _min_dependencies as min_deps  # noqa

DISTNAME = "FPTE",
VERSION = FPTE.__version__
SCRIPTS = ["FPTE"]
AUTHOR = "Mahdi Davari"
AUTHOR_EMAIL = "Mahdi.Davari@iCloud.com"
DESCRIPTION = "The FPTE package is a collection of tools for finite pressure temperature " \
              "elastic constants calculation. Features include, but are not limited to " \
              "stress-strain method for getting second order elastic tensors using DFT " \
              "package VASP as well as, ab initio molecular dynamic method for temperature" \
              "dependent elastic constants."

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

LONG_DESCRIPTION_CONTENT = "text/markdown"
URL = "https://github.com/MahdiDavari/FPTE"
LICENSE = ""
PROJECT_URLS = {
    "Documentation": "https://github.com/MahdiDavari/FPTE/blob/master/README.md",
    "Source Code": "https://github.com/MahdiDavari/FPTE",
    "Bug Reports": "https://github.com/MahdiDavari/FPTE/issues",
}

DOWNLOAD_URL = "https://pypi.org/project/FPTE/#files"

SETUPTOOLS_COMMANDS = {
    "develop",
    "release",
    "bdist_egg",
    "bdist_rpm",
    "bdist_wininst",
    "install_egg_info",
    "build_sphinx",
    "egg_info",
    "easy_install",
    "upload",
    "bdist_wheel",
    "--single-version-externally-managed",
}
if SETUPTOOLS_COMMANDS.intersection(sys.argv):
    extra_setuptools_args = dict(
        zip_safe=False,
        include_package_data=True,
        extras_require={
            key: min_deps.tag_to_packages[key]
            for key in ["examples", "docs", "tests"]
        },
    )
else:
    extra_setuptools_args = dict()


def setup_package():
    """main function for metadata and instalation
    """
    metadata = dict(
        name=DISTNAME,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        scripts=SCRIPTS,
        download_url=DOWNLOAD_URL,
        project_urls=PROJECT_URLS,
        version=VERSION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESCRIPTION_CONTENT,
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        include_package_data=True,
        install_requires=min_deps.tag_to_packages["install"],
        classifiers=[
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Topic :: Software Development",
            "Topic :: Scientific/Engineering",
            "Development Status :: 3 - Stable",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Operating System :: MacOS",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: Implementation :: CPython",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],

        python_requires=">=3.7",
        package_data={"": ["*.json", "*.yaml"]},
        **extra_setuptools_args,
    )
    setup(**metadata)


if __name__ == "__main__":
    setup_package()
