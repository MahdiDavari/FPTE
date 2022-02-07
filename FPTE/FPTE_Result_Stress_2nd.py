#!/usr/bin/env python 
# %!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%#
# %!%!% ----------------------------- FPTE_Result_Stress_2nd ----------------------------- %!%!%#
# %!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%#
#
# AUTHORs:
# Mahdi Davari
# Mahdi.Davari@stonybrook.edu
#
# Rostam Golesorkhtabar
# r.golesorkhtabar@gmail.com
#
# DATE:
# July 01 00:00:00 2018
#
# SYNTAX:
# python FPTE_Result_Stress_2nd.py
#        FPTE_Result_Stress_2nd
#
# EXPLANATION:
#
# __________________________________________________________________________________________________

import os
import os.path
import sys
import time

import numpy as np


def fpte_results():
    # %!%!%--- Dictionaries ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%
    head = { \
        'CI': '\
        for, space group-number between 207 and 230, Cubic I structure.        \n\n\
                C11     C12     C12      0       0       0                  \n\
                C12     C11     C12      0       0       0                  \n\
                C12     C12     C11      0       0       0                  \n\
                 0       0       0      C44      0       0                  \n\
                 0       0       0       0      C44      0                  \n\
                 0       0       0       0       0      C44                 \n', \
        'CII': '\
        for, space group-number between 195 and 206, Cubic II structure.       \n\n\
                C11     C12     C12      0       0       0                  \n\
                C12     C11     C12      0       0       0                  \n\
                C12     C12     C11      0       0       0                  \n\
                 0       0       0      C44      0       0                  \n\
                 0       0       0       0      C44      0                  \n\
                 0       0       0       0       0      C44                 \n', \
        'HI': '\
        for, space group-number between 177 and 194, Hexagonal I structure.    \n\n\
                C11     C12     C13      0       0       0                  \n\
                C12     C11     C13      0       0       0                  \n\
                C13     C13     C33      0       0       0                  \n\
                 0       0       0      C44      0       0                  \n\
                 0       0       0       0      C44      0                  \n\
                 0       0       0       0       0   (C11-C12)/2            \n', \
        'HII': '\
        for, space group-number between 168 and 176, Hexagonal II structure.   \n\n\
                C11     C12     C13      0       0       0                  \n\
                C12     C11     C13      0       0       0                  \n\
                C13     C13     C33      0       0       0                  \n\
                 0       0       0      C44      0       0                  \n\
                 0       0       0       0      C44      0                  \n\
                 0       0       0       0       0   (C11-C12)/2            \n', \
        'RI': '\
        for, space group-number between 149 and 167, Rhombohedral I structure. \n\n\
                C11     C12     C13     C14      0       0                  \n\
                C12     C11     C13    -C14      0       0                  \n\
                C13     C13     C33      0       0       0                  \n\
                C14    -C14      0      C44      0       0                  \n\
                 0       0       0       0      C44     C14                 \n\
                 0       0       0       0      C14  (C11-C12)/2            \n', \
        'RII': '\
        for, space group-number between 143 and 148, Rhombohedral II structure.\n\n\
                C11     C12     C13     C14     C15      0                  \n\
                C12     C11     C13    -C14    -C15      0                  \n\
                C13     C13     C33      0       0       0                  \n\
                C14    -C14      0      C44      0     -C15                 \n\
                C15    -C15      0       0      C44     C14                 \n\
                 0       0       0     -C15     C14  (C11-C12)/2            \n', \
        'TI': '\
        for, space group-number between 89 and 142, Tetragonal I structure.    \n\n\
                C11     C12     C13      0       0       0                  \n\
                C12     C11     C13      0       0       0                  \n\
                C13     C13     C33      0       0       0                  \n\
                 0       0       0      C44      0       0                  \n\
                 0       0       0       0      C44      0                  \n\
                 0       0       0       0       0      C66                 \n', \
        'TII': '\
        for, space group-number between 75 and 88, Tetragonal II structure.    \n\n\
                C11     C12     C13      0       0      C16                 \n\
                C12     C11     C13      0       0     -C16                 \n\
                C13     C13     C33      0       0       0                  \n\
                 0       0       0      C44      0       0                  \n\
                 0       0       0       0      C44      0                  \n\
                C16    -C16      0       0       0      C66                 \n', \
        'O': '\
        for, space group-number between 16 and 74, Orthorhombic structure.     \n\n\
                C11     C12     C13      0       0       0                  \n\
                C12     C22     C23      0       0       0                  \n\
                C13     C23     C33      0       0       0                  \n\
                 0       0       0      C44      0       0                  \n\
                 0       0       0       0      C55      0                  \n\
                 0       0       0       0       0      C66                 \n', \
        'M': '\
        for, space group-number between 3 and 15, Monoclinic structure.        \n\n\
                C11     C12     C13      0       0      C16                 \n\
                C12     C22     C23      0       0      C26                 \n\
                C13     C23     C33      0       0      C36                 \n\
                 0       0       0      C44     C45      0                  \n\
                 0       0       0      C45     C55      0                  \n\
                C16     C26     C36      0       0      C66                 \n', \
        'N': '\
        for, space group-number between 1 and 2, Triclinic structure.          \n\n\
                C11     C12     C13     C14      C15    C16                 \n\
                C12     C22     C23     C24      C25    C26                 \n\
                C13     C23     C33     C34      C35    C36                 \n\
                C14     C24     C34     C44      C45    C46                 \n\
                C15     C25     C35     C45      C55    C56                 \n\
                C16     C26     C36     C46      C56    C66                 \n'}
    # --------------------------------------------------------------------------------------------------

    # %!%!%--- Reading the "INFO_FPTE" file ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!
    INFO = open('INFO_FPTE', 'r')

    l1 = INFO.readline()
    ordr = int(l1.split()[-1])

    if (ordr != 2 and ordr != 3):
        sys.exit('\n.... Oops ERROR: The order of the elastic constant is NOT clear !?!?!?' \
                 '\n                 Something is WRONG in the "INFO_FPTE" file.\n')

    l2 = INFO.readline()
    mthd = l2.split()[-1]

    if (mthd != 'Stress' and mthd != 'Energy'):
        sys.exit('\n.... Oops ERROR: The method of the calculation is NOT clear !?!?!?' \
                 '\n                 Something is WRONG in the "INFO_FPTE" file.\n')

    l3 = INFO.readline()
    cod = l3.split()[-1]

    if (cod != 'WIEN2k' and cod != 'exciting' and cod != 'ESPRESSO' and cod != 'VASP'):
        sys.exit('\n.... Oops ERROR: The DFT code is NOT clear !?!?!?' \
                 '\n                 Something is WRONG in the "INFO_FPTE" file.\n')

    # l5  = INFO.readline()
    # V0  = float(l5.split()[-2])

    l6 = INFO.readline()
    mdr = float(l6.split()[-1])

    l7 = INFO.readline()
    NoP = int(l7.split()[-1])

    l4 = INFO.readline()
    SGN = int(l4.split()[-1])

    INFO.close()
    # --------------------------------------------------------------------------------------------------
    # %%%--- Calculating the Space-Group Number and classifying it ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!
    # NoD = Number of Deformation
    if (1 <= SGN and SGN <= 2):  # Triclinic
        LC = 'N'
        NoD = 6

    elif (3 <= SGN and SGN <= 15):  # Monoclinic
        LC = 'M'
        NoD = 5

    elif (16 <= SGN and SGN <= 74):  # Orthorhombic
        LC = 'O'
        NoD = 3

    elif (75 <= SGN and SGN <= 88):  # Tetragonal II
        LC = 'TII'
        NoD = 2

    elif (89 <= SGN and SGN <= 142):  # Tetragonal I
        LC = 'TI'
        NoD = 2

    elif (143 <= SGN and SGN <= 148):  # Rhombohedral II
        LC = 'RII'
        NoD = 2

    elif (149 <= SGN and SGN <= 167):  # Rhombohedral I
        LC = 'RI'
        NoD = 2

    elif (168 <= SGN and SGN <= 176):  # Hexagonal II
        LC = 'HII'
        NoD = 2

    elif (177 <= SGN and SGN <= 194):  # Hexagonal I
        LC = 'HI'
        NoD = 2

    elif (195 <= SGN and SGN <= 206):  # Cubic II
        LC = 'CII'
        NoD = 1

    elif (207 <= SGN and SGN <= 230):  # Cubic I
        LC = 'CI'
        NoD = 1

    else:
        sys.exit('\n.... Oops ERROR: WRONG Space-Group Number !?!?!?    \n')
    # --------------------------------------------------------------------------------------------------

    lineseparator = ' '
    for i in range(0, 79):
        lineseparator = lineseparator + '%'

    # %%%--- Making the Matrix  ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%
    if (LC == 'CI' or \
            LC == 'CII'):
        Matrix = np.mat([[1.0, 5.0, 0.0],
                         [2.0, 4.0, 0.0],
                         [3.0, 3.0, 0.0],
                         [0.0, 0.0, 4.0],
                         [0.0, 0.0, 5.0],
                         [0.0, 0.0, 6.0]])

    if (LC == 'HI' or \
            LC == 'HII'):
        Matrix = np.mat([[1, 2, 3, 0, 0],
                         [2, 1, 3, 0, 0],
                         [0, 0, 3, 3, 0],
                         [0, 0, 0, 0, 4],
                         [0, 0, 0, 0, 5],
                         [3, -3, 0, 0, 0],
                         [3, -5, -1, 0, 0],
                         [-5, 3, -1, 0, 0],
                         [0, 0, -2, -1, 0],
                         [0, 0, 0, 0, 6],
                         [0, 0, 0, 0, 2],
                         [-2, 2, 0, 0, 0]])

    if (LC == 'RI'):
        Matrix = np.mat([[1, 2, 3, 4, 0, 0],
                         [2, 1, 3, -4, 0, 0],
                         [0, 0, 3, 0, 3, 0],
                         [0, 0, 0, -1, 0, 4],
                         [0, 0, 0, 6, 0, 5],
                         [3, -3, 0, 5, 0, 0],
                         [3, -5, -1, 6, 0, 0],
                         [-5, 3, -1, -6, 0, 0],
                         [0, 0, -2, 0, -1, 0],
                         [0, 0, 0, 8, 0, 6],
                         [0, 0, 0, -4, 0, 2],
                         [-2, 2, 0, 2, 0, 0]])

    if (LC == 'RII'):
        Matrix = np.mat([[1, 2, 3, 4, 5, 0, 0],
                         [2, 1, 3, -4, -5, 0, 0],
                         [0, 0, 3, 0, 0, 3, 0],
                         [0, 0, 0, -1, -6, 0, 4],
                         [0, 0, 0, 6, -1, 0, 5],
                         [3, -3, 0, 5, -4, 0, 0],
                         [3, -5, -1, 6, 2, 0, 0],
                         [-5, 3, -1, -6, -2, 0, 0],
                         [0, 0, -2, 0, 0, -1, 0],
                         [0, 0, 0, 8, 4, 0, 6],
                         [0, 0, 0, -4, 8, 0, 2],
                         [-2, 2, 0, 2, -6, 0, 0]])

    if (LC == 'TI'):
        Matrix = np.mat([[1, 2, 3, 0, 0, 0],
                         [2, 1, 3, 0, 0, 0],
                         [0, 0, 3, 3, 0, 0],
                         [0, 0, 0, 0, 4, 0],
                         [0, 0, 0, 0, 5, 0],
                         [0, 0, 0, 0, 0, 6],
                         [3, -5, -1, 0, 0, 0],
                         [-5, 3, -1, 0, 0, 0],
                         [0, 0, -2, -1, 0, 0],
                         [0, 0, 0, 0, 6, 0],
                         [0, 0, 0, 0, 2, 0],
                         [0, 0, 0, 0, 0, -4]])

    if (LC == 'TII'):
        Matrix = np.mat([[1, 2, 3, 6, 0, 0, 0],
                         [2, 1, 3, -6, 0, 0, 0],
                         [0, 0, 3, 0, 3, 0, 0],
                         [0, 0, 0, 0, 0, 4, 0],
                         [0, 0, 0, 0, 0, 5, 0],
                         [0, 0, 0, -1, 0, 0, 6],
                         [3, -5, -1, -4, 0, 0, 0],
                         [-5, 3, -1, 4, 0, 0, 0],
                         [0, 0, -2, 0, -1, 0, 0],
                         [0, 0, 0, 0, 0, 6, 0],
                         [0, 0, 0, 0, 0, 2, 0],
                         [0, 0, 0, 8, 0, 0, -4]])

    if (LC == 'O'):
        Matrix = np.mat([[1, 2, 3, 0, 0, 0, 0, 0, 0],
                         [0, 1, 0, 2, 3, 0, 0, 0, 0],
                         [0, 0, 1, 0, 2, 3, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 4, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 5, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 6],
                         [3, -5, -1, 0, 0, 0, 0, 0, 0],
                         [0, 3, 0, -5, -1, 0, 0, 0, 0],
                         [0, 0, 3, 0, -5, -1, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 6, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 2, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, -4],
                         [5, 4, 6, 0, 0, 0, 0, 0, 0],
                         [0, 5, 0, 4, 6, 0, 0, 0, 0],
                         [0, 0, 5, 0, 4, 6, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, -2, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, -1, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, -3]])

    if (LC == 'M'):
        Matrix = np.mat([[1, 2, 3, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 1, 0, 0, 2, 3, 6, 0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0, 2, 0, 3, 6, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 5, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 5, 0],
                         [0, 0, 0, 1, 0, 0, 2, 0, 3, 0, 0, 0, 6],
                         [-2, 1, 4, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, -2, 0, 0, 1, 4, -5, 0, 0, 0, 0, 0, 0],
                         [0, 0, -2, 0, 0, 1, 0, 4, -5, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 6, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 6, 0],
                         [0, 0, 0, -2, 0, 0, 1, 0, 4, 0, 0, -5, 0],
                         [3, -5, -1, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 3, 0, 0, -5, -1, -4, 0, 0, 0, 0, 0, 0],
                         [0, 0, 3, 0, 0, -5, 0, -1, -4, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2, 0],
                         [0, 0, 0, 3, 0, 0, -5, 0, -1, 0, 0, -4, 0],
                         [-4, -6, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, -4, 0, 0, -6, 5, 2, 0, 0, 0, 0, 0, 0],
                         [0, 0, -4, 0, 0, -6, 0, 5, 2, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -3, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -3, 0],
                         [0, 0, 0, -4, 0, 0, -6, 0, 5, 0, 0, 2, 0],
                         [5, 4, 6, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 5, 0, 0, 4, 6, -3, 0, 0, 0, 0, 0, 0],
                         [0, 0, 5, 0, 0, 4, 0, 6, -3, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, -2, -1, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, -1, 0],
                         [0, 0, 0, 5, 0, 0, 4, 0, 6, 0, 0, -3, 0]])

    if (LC == 'N'):
        Matrix = np.mat([[1, 2, 3, 4, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 1, 0, 0, 0, 0, 2, 3, 4, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 3, 4, 5, 6, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 4, 5, 6, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 4, 0, 5, 6, 0],
                         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 4, 0, 5, 6],
                         [-2, 1, 4, -3, 6, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, -2, 0, 0, 0, 0, 1, 4, -3, 6, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, -2, 0, 0, 0, 0, 1, 0, 0, 0, 4, -3, 6, -5, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, -2, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, -3, 6, -5, 0, 0, 0],
                         [0, 0, 0, 0, -2, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, -3, 0, 6, -5, 0],
                         [0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, -3, 0, 6, -5],
                         [3, -5, -1, 6, 2, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 3, 0, 0, 0, 0, -5, -1, 6, 2, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 3, 0, 0, 0, 0, -5, 0, 0, 0, -1, 6, 2, -4, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 3, 0, 0, 0, 0, -5, 0, 0, 0, -1, 0, 0, 6, 2, -4, 0, 0, 0],
                         [0, 0, 0, 0, 3, 0, 0, 0, 0, -5, 0, 0, 0, -1, 0, 0, 6, 0, 2, -4, 0],
                         [0, 0, 0, 0, 0, 3, 0, 0, 0, 0, -5, 0, 0, 0, -1, 0, 0, 6, 0, 2, -4],
                         [-4, -6, 5, 1, -3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, -4, 0, 0, 0, 0, -6, 5, 1, -3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, -4, 0, 0, 0, 0, -6, 0, 0, 0, 5, 1, -3, 2, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, -4, 0, 0, 0, 0, -6, 0, 0, 0, 5, 0, 0, 1, -3, 2, 0, 0, 0],
                         [0, 0, 0, 0, -4, 0, 0, 0, 0, -6, 0, 0, 0, 5, 0, 0, 1, 0, -3, 2, 0],
                         [0, 0, 0, 0, 0, -4, 0, 0, 0, 0, -6, 0, 0, 0, 5, 0, 0, 1, 0, -3, 2],
                         [5, 4, 6, -2, -1, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 5, 0, 0, 0, 0, 4, 6, -2, -1, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 5, 0, 0, 0, 0, 4, 0, 0, 0, 6, -2, -1, -3, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 5, 0, 0, 0, 0, 4, 0, 0, 0, 6, 0, 0, -2, -1, -3, 0, 0, 0],
                         [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0, 0, 0, 6, 0, 0, -2, 0, -1, -3, 0],
                         [0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0, 0, 0, 6, 0, 0, -2, 0, -1, -3],
                         [-6, 3, -2, 5, -4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, -6, 0, 0, 0, 0, 3, -2, 5, -4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, -6, 0, 0, 0, 0, 3, 0, 0, 0, -2, 5, -4, 1, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, -6, 0, 0, 0, 0, 3, 0, 0, 0, -2, 0, 0, 5, -4, 1, 0, 0, 0],
                         [0, 0, 0, 0, -6, 0, 0, 0, 0, 3, 0, 0, 0, -2, 0, 0, 5, 0, -4, 1, 0],
                         [0, 0, 0, 0, 0, -6, 0, 0, 0, 0, 3, 0, 0, 0, -2, 0, 0, 5, 0, -4, 1]])

    # %!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%#
    # %!%!% ------------ Calculating the second derivative and Cross-Validation Error ----------- %!%!%#
    # %!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%#
    OBJ = open('FPTE_2nd.in', 'r')

    # RoD = Range of Deformation
    RoD = OBJ.read().strip().split()

    if (len(RoD) != 13 * NoD):
        sys.exit('\n.... Oops ERROR: Something is WRONG in the "FPTE_2nd.in" file !?!?!?\n')

    os.chdir('Stress-vs-Strain')

    sigma = []
    for i in range(1, NoD + 1):
        if (i < 10):
            Dstn = 'Deform0' + str(i)
        else:
            Dstn = 'Deform' + str(i)

        for j in range(0, 13 * NoD - 1, 13):
            if (RoD[j] == Dstn):
                mdr1 = abs(float(RoD[j + 1]))
                mdr2 = abs(float(RoD[j + 2]))
                mdr3 = abs(float(RoD[j + 3]))
                mdr4 = abs(float(RoD[j + 4]))
                mdr5 = abs(float(RoD[j + 5]))
                mdr6 = abs(float(RoD[j + 6]))
                ordr1 = abs(int(float(RoD[j + 7])))
                ordr2 = abs(int(float(RoD[j + 8])))
                ordr3 = abs(int(float(RoD[j + 9])))
                ordr4 = abs(int(float(RoD[j + 10])))
                ordr5 = abs(int(float(RoD[j + 11])))
                ordr6 = abs(int(float(RoD[j + 12])))

            if (os.path.exists(Dstn + '_Lagrangian-stress.dat') == False):
                sys.exit(
                    '\n.... Oops ERROR: Where is the "' + Dstn + '_Lagrangian-stress.dat" !?!?!?\n')

            eta_strs = open(Dstn + '_Lagrangian-stress.dat', 'r')
            eta_strs.readline()
            eta_strs.readline()

            str1 = []
            str2 = []
            str3 = []
            str4 = []
            str5 = []
            str6 = []

            ls1 = []
            ls2 = []
            ls3 = []
            ls4 = []
            ls5 = []
            ls6 = []

            while True:
                line = eta_strs.readline()
                line = line.strip()
                if (len(line) == 0): break

                eta, lsxx, lsyy, lszz, lsyz, lsxz, lsxy = line.split()
                if (-mdr1 <= float(eta) and float(eta) <= mdr1):
                    str1.append(float(eta))
                    ls1.append(float(lsxx))
                if (-mdr2 <= float(eta) and float(eta) <= mdr2):
                    str2.append(float(eta))
                    ls2.append(float(lsyy))
                if (-mdr3 <= float(eta) and float(eta) <= mdr3):
                    str3.append(float(eta))
                    ls3.append(float(lszz))
                if (-mdr4 <= float(eta) and float(eta) <= mdr4):
                    str4.append(float(eta))
                    ls4.append(float(lsyz))
                if (-mdr5 <= float(eta) and float(eta) <= mdr5):
                    str5.append(float(eta))
                    ls5.append(float(lsxz))
                if (-mdr6 <= float(eta) and float(eta) <= mdr6):
                    str6.append(float(eta))
                    ls6.append(float(lsxy))

            num_eta1 = len(str1)
            if (num_eta1 < ordr1 + 1):
                sys.exit(
                    '\n.... Oops ERROR: NOT enough stress points in "' + Dstn + '_Lagrangian-stress.dat"' \
                                                                                '\n                 for ' + str(
                        ordr1) + ' order polynomial fit.\n')

            num_eta2 = len(str2)
            if (num_eta2 < ordr2 + 1):
                sys.exit(
                    '\n.... Oops ERROR: NOT enough stress points in "' + Dstn + '_Lagrangian-stress.dat"' \
                                                                                '\n                 for ' + str(
                        ordr2) + ' order polynomial fit.\n')

            num_eta3 = len(str3)
            if (num_eta3 < ordr3 + 1):
                sys.exit(
                    '\n.... Oops ERROR: NOT enough stress points in "' + Dstn + '_Lagrangian-stress.dat"' \
                                                                                '\n                 for ' + str(
                        ordr3) + ' order polynomial fit.\n')

            num_eta4 = len(str4)
            if (num_eta4 < ordr4 + 1):
                sys.exit(
                    '\n.... Oops ERROR: NOT enough stress points in "' + Dstn + '_Lagrangian-stress.dat"' \
                                                                                '\n                 for ' + str(
                        ordr4) + ' order polynomial fit.\n')

            num_eta5 = len(str5)
            if (num_eta5 < ordr5 + 1):
                sys.exit(
                    '\n.... Oops ERROR: NOT enough stress points in "' + Dstn + '_Lagrangian-stress.dat"' \
                                                                                '\n                 for ' + str(
                        ordr5) + ' order polynomial fit.\n')

            num_eta6 = len(str6)
            if (num_eta6 < ordr6 + 1):
                sys.exit(
                    '\n.... Oops ERROR: NOT enough stress points in "' + Dstn + '_Lagrangian-stress.dat"' \
                                                                                '\n                 for ' + str(
                        ordr6) + ' order polynomial fit.\n')

        coeff1 = []
        coeff1 = np.polyfit(str1, ls1, ordr1)
        sigma.append(float(coeff1[ordr1 - 1]))

        coeff2 = []
        coeff2 = np.polyfit(str2, ls2, ordr2)
        sigma.append(float(coeff2[ordr2 - 1]))

        coeff3 = []
        coeff3 = np.polyfit(str3, ls3, ordr3)
        sigma.append(float(coeff3[ordr3 - 1]))

        coeff4 = []
        coeff4 = np.polyfit(str4, ls4, ordr4)
        sigma.append(float(coeff4[ordr4 - 1]))

        coeff5 = []
        coeff5 = np.polyfit(str5, ls5, ordr5)
        sigma.append(float(coeff5[ordr5 - 1]))

        coeff6 = []
        coeff6 = np.polyfit(str6, ls6, ordr6)
        sigma.append(float(coeff6[ordr6 - 1]))

    # %%%--- Calculating the elastic constant and writing the output file ---%!%!%!%!%!%!%!%!%!%!%!%!%!%
    if (len(sigma) != 6 * NoD):
        sys.exit('\n.... Oops ERROR: Something is WRONG in the "FPTE_2nd.in" file !?!?!?\n')

    sigma = np.array(sigma)
    ci = np.linalg.lstsq(Matrix, sigma)
    C = np.zeros((6, 6))

    # -- Cubic structures ------------------------------------------------------------------------------
    if (LC == 'CI' or \
            LC == 'CII'):
        C[0, 0] = ci[0][0]
        C[0, 1] = ci[0][1]
        C[3, 3] = ci[0][2]
        C[1, 1] = C[0, 0]
        C[2, 2] = C[0, 0]
        C[0, 2] = C[0, 1]
        C[1, 2] = C[0, 1]
        C[4, 4] = C[3, 3]
        C[5, 5] = C[3, 3]

    # -- Hexagonal Structures --------------------------------------------------------------------------
    if (LC == 'HI' or \
            LC == 'HII'):
        C[0, 0] = ci[0][0]
        C[0, 1] = ci[0][1]
        C[0, 2] = ci[0][2]
        C[2, 2] = ci[0][3]
        C[3, 3] = ci[0][4]
        C[1, 1] = C[0, 0]
        C[1, 2] = C[0, 2]
        C[4, 4] = C[3, 3]
        C[5, 5] = 0.5 * (C[0, 0] - C[0, 1])

    # -- Rhombohedral I Structures ---------------------------------------------------------------------
    if (LC == 'RI'):
        C[0, 0] = ci[0][0]
        C[0, 1] = ci[0][1]
        C[0, 2] = ci[0][2]
        C[0, 3] = ci[0][3]
        C[2, 2] = ci[0][4]
        C[3, 3] = ci[0][5]
        C[1, 1] = C[0, 0]
        C[1, 2] = C[0, 2]
        C[1, 3] = -C[0, 3]
        C[4, 5] = C[0, 3]
        C[4, 4] = C[3, 3]
        C[5, 5] = 0.5 * (C[0, 0] - C[0, 1])

    # -- Rhombohedral II Structures --------------------------------------------------------------------
    if (LC == 'RII'):
        C[0, 0] = ci[0][0]
        C[0, 1] = ci[0][1]
        C[0, 2] = ci[0][2]
        C[0, 3] = ci[0][3]
        C[0, 4] = ci[0][4]
        C[2, 2] = ci[0][5]
        C[3, 3] = ci[0][6]
        C[1, 1] = C[0, 0]
        C[1, 2] = C[0, 2]
        C[1, 3] = -C[0, 3]
        C[4, 5] = C[0, 3]
        C[1, 4] = -C[0, 4]
        C[3, 5] = -C[0, 4]
        C[4, 4] = C[3, 3]
        C[5, 5] = 0.5 * (C[0, 0] - C[0, 1])

    # -- Tetragonal I Structures -----------------------------------------------------------------------
    if (LC == 'TI'):
        C[0, 0] = ci[0][0]
        C[0, 1] = ci[0][1]
        C[0, 2] = ci[0][2]
        C[2, 2] = ci[0][3]
        C[3, 3] = ci[0][4]
        C[5, 5] = ci[0][5]
        C[1, 1] = C[0, 0]
        C[1, 2] = C[0, 2]
        C[4, 4] = C[3, 3]

    # -- Tetragonal II Structures ----------------------------------------------------------------------
    if (LC == 'TII'):
        C[0, 0] = ci[0][0]
        C[0, 1] = ci[0][1]
        C[0, 2] = ci[0][2]
        C[0, 5] = ci[0][3]
        C[2, 2] = ci[0][4]
        C[3, 3] = ci[0][5]
        C[5, 5] = ci[0][6]
        C[1, 1] = C[0, 0]
        C[1, 2] = C[0, 2]
        C[1, 5] = -C[0, 5]
        C[4, 4] = C[3, 3]

    # -- Orthorhombic Structures -----------------------------------------------------------------------
    if (LC == 'O'):
        C[0, 0] = ci[0][0]
        C[0, 1] = ci[0][1]
        C[0, 2] = ci[0][2]
        C[1, 1] = ci[0][3]
        C[1, 2] = ci[0][4]
        C[2, 2] = ci[0][5]
        C[3, 3] = ci[0][6]
        C[4, 4] = ci[0][7]
        C[5, 5] = ci[0][8]

    # -- Monoclinic Structures -------------------------------------------------------------------------
    if (LC == 'M'):
        C[0, 0] = ci[0][0]
        C[0, 1] = ci[0][1]
        C[0, 2] = ci[0][2]
        C[0, 5] = ci[0][3]
        C[1, 1] = ci[0][4]
        C[1, 2] = ci[0][5]
        C[1, 5] = ci[0][6]
        C[2, 2] = ci[0][7]
        C[2, 5] = ci[0][8]
        C[3, 3] = ci[0][9]
        C[3, 4] = ci[0][10]
        C[4, 4] = ci[0][11]
        C[5, 5] = ci[0][12]

    # -- Triclinic Structures --------------------------------------------------------------------------
    if (LC == 'N'):
        C[0, 0] = ci[0][0]
        C[0, 1] = ci[0][1]
        C[0, 2] = ci[0][2]
        C[0, 3] = ci[0][3]
        C[0, 4] = ci[0][4]
        C[0, 5] = ci[0][5]
        C[1, 1] = ci[0][6]
        C[1, 2] = ci[0][7]
        C[1, 3] = ci[0][8]
        C[1, 4] = ci[0][9]
        C[1, 5] = ci[0][10]
        C[2, 2] = ci[0][11]
        C[2, 3] = ci[0][12]
        C[2, 4] = ci[0][13]
        C[2, 5] = ci[0][14]
        C[3, 3] = ci[0][15]
        C[3, 4] = ci[0][16]
        C[3, 5] = ci[0][17]
        C[4, 4] = ci[0][18]
        C[4, 5] = ci[0][19]
        C[5, 5] = ci[0][20]
    # --------------------------------------------------------------------------------------------------

    # %%%--- Calculating the elastic moduli ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%
    if (cod == 'WIEN2k'):
        CONV = 1.
    if (cod == 'exciting'):
        CONV = 1.
    if (cod == 'ESPRESSO'):
        CONV = -1. / 10.
    if (cod == 'VASP'):
        CONV = -1. / 10.

    for i in range(5):
        for j in range(i + 1, 6):
            C[j, i] = C[i, j]

    C = C * CONV
    BV = (C[0, 0] + C[1, 1] + C[2, 2] + 2 * (C[0, 1] + C[0, 2] + C[1, 2])) / 9
    GV = ((C[0, 0] + C[1, 1] + C[2, 2]) - (C[0, 1] + C[0, 2] + C[1, 2]) + 3 * (
            C[3, 3] + C[4, 4] + C[5, 5])) / 15
    EV = (9 * BV * GV) / (3 * BV + GV)
    nuV = (1.5 * BV - GV) / (3 * BV + GV)
    S = np.linalg.inv(C)
    BR = 1 / (S[0, 0] + S[1, 1] + S[2, 2] + 2 * (S[0, 1] + S[0, 2] + S[1, 2]))
    GR = 15 / (4 * (S[0, 0] + S[1, 1] + S[2, 2]) - 4 * (S[0, 1] + S[0, 2] + S[1, 2]) + 3 * (
            S[3, 3] + S[4, 4] + S[5, 5]))
    ER = (9 * BR * GR) / (3 * BR + GR)
    nuR = (1.5 * BR - GR) / (3 * BR + GR)
    BH = 0.50 * (BV + BR)
    GH = 0.50 * (GV + GR)
    EH = (9. * BH * GH) / (3. * BH + GH)
    nuH = (1.5 * BH - GH) / (3. * BH + GH)
    AVR = 100. * (GV - GR) / (GV + GR)
    # --------------------------------------------------------------------------------------------------

    # %%%--- Writing the output file ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!
    fo = open('FPTE_2nd.out', 'w')
    fo.write('    The output of FPTE code                                              \n' \
             '    Today is ' + time.asctime() + '\n' \
                                                '\n' \
                                                '    Symmetry of the second-order elastic constant matrix in Voigt notation. \n' \
             + head[LC] + '\n' \
                          '    Elastic constant (stiffness) matrix in GPa:                             \n')

    for i in range(0, 6):
        for j in range(0, 6):
            fo.write('%11.1f' % (C[i, j]))
        fo.write(' \n')

    fo.write('\n\n    Elastic compliance matrix in 1/GPa: \n')

    for i in range(0, 6):
        for j in range(0, 6):
            fo.write('%11.5f' % (S[i, j]))
        fo.write('\n')

    fo.write('\n' + lineseparator + '\n')

    fo.write('    Voigt bulk  modulus, B_V = {0}  GPa'.format('%8.2f' % (BV)) + '\n')
    fo.write('    Voigt shear modulus, G_V = {0}  GPa'.format('%8.2f' % (GV)) + '\n')

    fo.write('    Reuss bulk  modulus, B_R = {0}  GPa'.format('%8.2f' % (BR)) + '\n')
    fo.write('    Reuss shear modulus, G_R = {0}  GPa'.format('%8.2f' % (GR)) + '\n')

    fo.write('    Hill bulk  modulus,  B_H = {0}  GPa'.format('%8.2f' % (BH)) + '\n')
    fo.write('    Hill shear modulus,  G_H = {0}  GPa'.format('%8.2f' % (GH)) + '\n')

    fo.write('\n' + lineseparator + '\n')

    fo.write('    Voigt Young modulus,  E_V = {0}  GPa'.format('%8.2f' % (EV)) + '\n')
    fo.write('    Voigt Poisson ratio, nu_V = {0}'.format('%8.2f' % (nuV)) + '\n')

    fo.write('    Reuss Young modulus,  E_R = {0}  GPa'.format('%8.2f' % (ER)) + '\n')
    fo.write('    Reuss Poisson ratio, nu_R = {0}'.format('%8.2f' % (nuR)) + '\n')

    fo.write('    Hill Young modulus,   E_H = {0}  GPa'.format('%8.2f' % (EH)) + '\n')
    fo.write('    Hill Poisson ratio,  nu_H = {0}'.format('%8.2f' % (nuH)) + '\n')

    fo.write('\n' + lineseparator + '\n')

    fo.write(
        '    Elastic Anisotropy in polycrystalline, AVR = {0} %'.format('%8.3f' % (AVR)) + '\n')

    fo.write('\n' + lineseparator + '\n')

    fo.write('    Eigenvalues of elastic constant (stiffness) matrix:   \n')

    eigval = np.linalg.eig(C)
    for i in range(6):
        fo.write('%16.1f' % float(eigval[0][i]))

    fo.write(
        '\n    ... Have a G00D Day, Week, Month, Year, and Century (if you are lucky) ...    ' \
        '\n               Bye-Bye! Tschuess! Ciao! Poka! Zia Jian! KhodaHafez!             \n')
    fo.close()

    # %%%--- Writing Cij in stdout ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!
    print('                                                  \n' \
          '    Symmetry of the second-order elastic constant matrix in Voigt notation. \n' \
          + head[LC] + '\n' \
                       '    Elastic constant (stiffness) matrix in GPa:                             \n')

    for i in range(0, 6):
        print('%13.3f' % C[i][0] + '%13.3f' % C[i][1] + '%13.3f' % C[i][2] + '%13.3f' % C[i][
            3] + '%13.3f' % C[i][4] + '%13.3f' % C[i][5])
    print('\n')
    print('For more information see the FPTE_2nd.out file.')
    # --------------------------------------------------------------------------------------------------
    os.chdir('../src/')
    os.system('cp -f Stress-vs-Strain/FPTE_2nd.out .')


if __name__ == "__main__":
    fpte_results()
