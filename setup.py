import setuptools
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='FPTE',  
     version='1.1.0a3',
     scripts=['FPTE'] ,
     author="Mahdi Davari",
     author_email="Mahdi.Davari@icloud.com",
     description="The FPTE package is a collection of tools for finite pressure temperature elastic constants calculation. Features include, but are not limited to stress-strain method for getting second order elastic tensors using DFT package VASP as well as, ab initio molecular dynamic method for temperature dependent elastic constatns. The package is free and ...",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/MahdiDavari/FPTE",
     packages=setuptools.find_packages(where='src'),
     package_dir={'': 'src'},
     include_package_data=True,
     install_requires=['matplotlib', 'numpy', 'pandas'],

     classifiers=[
         "Development Status :: 3 - Alpha",
         "Programming Language :: Python :: 2",
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
    project_urls={
        'Bug Reports': 'https://github.com/MahdiDavari/FPTE/issues',
        'Source': 'https://github.com/MahdiDavari/FPTE/src',
    },
)
