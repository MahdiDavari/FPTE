"""All minimum dependencies for FPTE.
"""
import argparse

NUMPY_MIN_VERSION = "1.16.5"
PANDAS_MIN_VERSION = "0.25.3"
MATPLOTLIB_MIN_VERSION = "2.2.4"
JOBLIB_MIN_VERSION = "0.11"
PYTEST_MIN_VERSION = "5.0.1"
CYTHON_MIN_VERSION = "0.29.24"

# 'build' and 'install' is included to have structured metadata for CI.
# The values are (version_spec, comma separated tags)
dependent_packages = {
    "numpy": (NUMPY_MIN_VERSION, "build, install"),
    "pandas": (PANDAS_MIN_VERSION, "build, install, docs, examples, tests"),
    "matplotlib": (MATPLOTLIB_MIN_VERSION, "build, install, docs, examples, tests"),
    "joblib": (JOBLIB_MIN_VERSION, "install"),
    "cython": (CYTHON_MIN_VERSION, "build"),
    "subprocess32": ("3.5.4", "build, install"),
    "seaborn": ("0.9.0", "docs, examples"),
    "memory_profiler": ("0.57.0", "docs"),
    "pytest": (PYTEST_MIN_VERSION, "tests"),
    "PyHamcrest": ("2.0.3", "tests"),
    "pytest-cov": ("2.9.0", "tests"),
    "pyamg": ("4.0.0", "tests"),
    "sphinx": ("4.0.1", "docs"),
    "sphinx-gallery": ("0.7.0", "docs"),
    "Pillow": ("7.1.2", "docs"),
    "sphinx-prompt": ("1.3.0", "docs"),
    "sphinxext-opengraph": ("0.4.2", "docs"),
}

# create inverse mapping for setuptools
tag_to_packages: dict = {
    extra: [] for extra in ["build", "install", "docs", "examples", "tests"]
}
for package, (min_version, extras) in dependent_packages.items():
    for extra in extras.split(", "):
        tag_to_packages[extra].append("{}>={}".format(package, min_version))

# Used by CI to get the min dependencies
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get min dependencies for a package")

    parser.add_argument("package", choices=dependent_packages)
    args = parser.parse_args()
    min_version = dependent_packages[args.package][0]
    print(min_version)
