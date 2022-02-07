# coding: utf-8
# Distributed under the terms of the MIT License.
"""The FPTE package is a collection of tools for finite pressure temperature elastic constants'
calculation. Features include, but are not limited to stress-strain method for getting second
order elastic tensors using DFT package VASP as well as, ab initio molecular dynamic method for
temperature dependent elastic constants. The package is free and ...
"""

__author__ = "Mahdi Davari"
__email__ = "Mahdi.Davari@iCloud.com"
__version__ = "1.2.0"


from .FPTE_Analyze_Stress import fpte_analyze
from .FPTE_RMSD import fpte_rmsd
from .FPTE_Result_Stress_2nd import fpte_results
from .FPTE_Setup_VASP import fpte_setup
from .FPTE_clean import fpte_clean


__all__ = [_file for _file in dir() if not _file.startswith("_")]