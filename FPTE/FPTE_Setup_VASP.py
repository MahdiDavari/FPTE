#!/usr/bin/env python
# %!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%#
# %!%!% ------------------------------ FPTE_Setup_VASP---- ------------------------------- %!%!%#
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
# python FPTE_Setup_VASP.py
#        FPTE_Setup_VASP
#
# EXPLANATION:
#
# __________________________________________________________________________________________________

import glob
import os
import os.path
import re
import shutil
import sys

import numpy as np

from .exceptions import FolderNotClean


# class FPTE_Setup_VASP:

def fpte_setup():
    """[summary]

    Returns:
        [type]: [description]
    """
    # %!%!%--- DICTIONARIS ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!
    Ls_Dic = { \
        '01': [1., 1., 1., 0., 0., 0.], \
        '02': [1., 0., 0., 0., 0., 0.], \
        '03': [0., 1., 0., 0., 0., 0.], \
        '04': [0., 0., 1., 0., 0., 0.], \
        '05': [0., 0., 0., 2., 0., 0.], \
        '06': [0., 0., 0., 0., 2., 0.], \
        '07': [0., 0., 0., 0., 0., 2.], \
        '08': [1., 1., 0., 0., 0., 0.], \
        '09': [1., 0., 1., 0., 0., 0.], \
        '10': [1., 0., 0., 2., 0., 0.], \
        '11': [1., 0., 0., 0., 2., 0.], \
        '12': [1., 0., 0., 0., 0., 2.], \
        '13': [0., 1., 1., 0., 0., 0.], \
        '14': [0., 1., 0., 2., 0., 0.], \
        '15': [0., 1., 0., 0., 2., 0.], \
        '16': [0., 1., 0., 0., 0., 2.], \
        '17': [0., 0., 1., 2., 0., 0.], \
        '18': [0., 0., 1., 0., 2., 0.], \
        '19': [0., 0., 1., 0., 0., 2.], \
        '20': [0., 0., 0., 2., 2., 0.], \
        '21': [0., 0., 0., 2., 0., 2.], \
        '22': [0., 0., 0., 0., 2., 2.], \
        '23': [0., 0., 0., 2., 2., 2.], \
        '24': [-1., .5, .5, 0., 0., 0.], \
        '25': [.5, -1., .5, 0., 0., 0.], \
        '26': [.5, .5, -1., 0., 0., 0.], \
        '27': [1., -1., 0., 0., 0., 0.], \
        '28': [1., -1., 0., 0., 0., 2.], \
        '29': [0., 1., -1., 0., 0., 2.], \
        '30': [.5, .5, -1., 0., 0., 2.], \
        '31': [1., 0., 0., 2., 2., 0.], \
        '32': [1., 1., -1., 0., 0., 0.], \
        '33': [1., 1., 1., -2., -2., -2.], \
        '34': [.5, .5, -1., 2., 2., 2.], \
        '35': [0., 0., 0., 2., 2., 4.], \
        '36': [1., 2., 3., 4., 5., 6.], \
        '37': [-2., 1., 4., -3., 6., -5.], \
        '38': [3., -5., -1., 6., 2., -4.], \
        '39': [-4., -6., 5., 1., -3., 2.], \
        '40': [5., 4., 6., -2., -1., -3.], \
        '41': [-6., 3., -2., 5., -4., 1.]}

    Ls_str = {
        '01': '(  eta,  eta,  eta,  0.0,  0.0,  0.0)',
        '02': '(  eta,  0.0,  0.0,  0.0,  0.0,  0.0)',
        '03': '(  0.0,  eta,  0.0,  0.0,  0.0,  0.0)',
        '04': '(  0.0,  0.0,  eta,  0.0,  0.0,  0.0)',
        '05': '(  0.0,  0.0,  0.0, 2eta,  0.0,  0.0)',
        '06': '(  0.0,  0.0,  0.0,  0.0, 2eta,  0.0)',
        '07': '(  0.0,  0.0,  0.0,  0.0,  0.0, 2eta)',
        '08': '(  eta,  eta,  0.0,  0.0,  0.0,  0.0)',
        '09': '(  eta,  0.0,  eta,  0.0,  0.0,  0.0)',
        '10': '(  eta,  0.0,  0.0, 2eta,  0.0,  0.0)',
        '11': '(  eta,  0.0,  0.0,  0.0, 2eta,  0.0)',
        '12': '(  eta,  0.0,  0.0,  0.0,  0.0, 2eta)',
        '13': '(  0.0,  eta,  eta,  0.0,  0.0,  0.0)',
        '14': '(  0.0,  eta,  0.0, 2eta,  0.0,  0.0)',
        '15': '(  0.0,  eta,  0.0,  0.0, 2eta,  0.0)',
        '16': '(  0.0,  eta,  0.0,  0.0,  0.0, 2eta)',
        '17': '(  0.0,  0.0,  eta, 2eta,  0.0,  0.0)',
        '18': '(  0.0,  0.0,  eta,  0.0, 2eta,  0.0)',
        '19': '(  0.0,  0.0,  eta,  0.0,  0.0, 2eta)',
        '20': '(  0.0,  0.0,  0.0, 2eta, 2eta,  0.0)',
        '21': '(  0.0,  0.0,  0.0, 2eta,  0.0, 2eta)',
        '22': '(  0.0,  0.0,  0.0,  0.0, 2eta, 2eta)',
        '23': '(  0.0,  0.0,  0.0, 2eta, 2eta, 2eta)',
        '24': '( -eta,.5eta,.5eta,  0.0,  0.0,  0.0)',
        '25': '(.5eta, -eta,.5eta,  0.0,  0.0,  0.0)',
        '26': '(.5eta,.5eta, -eta,  0.0,  0.0,  0.0)',
        '27': '(  eta, -eta,  0.0,  0.0,  0.0,  0.0)',
        '28': '(  eta, -eta,  0.0,  0.0,  0.0, 2eta)',
        '29': '(  0.0,  eta, -eta,  0.0,  0.0, 2eta)',
        '30': '(.5eta,.5eta, -eta,  0.0,  0.0, 2eta)',
        '31': '(  eta,  0.0,  0.0, 2eta, 2eta,  0.0)',
        '32': '(  eta,  eta, -eta,  0.0,  0.0,  0.0)',
        '33': '(  eta,  eta,  eta,-2eta,-2eta,-2eta)',
        '34': '(.5eta,.5eta, -eta, 2eta, 2eta, 2eta)',
        '35': '(  0.0,  0.0,  0.0, 2eta, 2eta, 4eta)',
        '36': '( 1eta, 2eta, 3eta, 4eta, 5eta, 6eta)',
        '37': '(-2eta, 1eta, 4eta,-3eta, 6eta,-5eta)',
        '38': '( 3eta,-5eta,-1eta, 6eta, 2eta,-4eta)',
        '39': '(-4eta,-6eta, 5eta, 1eta,-3eta, 2eta)',
        '40': '( 5eta, 4eta, 6eta,-2eta,-1eta,-3eta)',
        '41': '(-6eta, 3eta,-2eta, 5eta,-4eta, 1eta)'}

    LC_Dic = { \
        'CI': 'Cubic I', \
        'CII': 'Cubic II', \
        'HI': 'Hexagonal I', \
        'HII': 'Hexagonal II', \
        'RI': 'Rhombohedral I', \
        'RII': 'Rhombohedral II', \
        'TI': 'Tetragonal I', \
        'TII': 'Tetragonal II', \
        'O': 'Orthorhombic', \
        'M': 'Monoclinic', \
        'N': 'Triclinic'}

    LT_Dic = { \
        'CI': 'Cubic', \
        'CII': 'Cubic', \
        'HI': 'Hexagonal', \
        'HII': 'Hexagonal', \
        'RI': 'Rhombohedral', \
        'RII': 'Rhombohedral', \
        'TI': 'Tetragonal', \
        'TII': 'Tetragonal', \
        'O': 'Orthorhombic', \
        'M': 'Monoclinic', \
        'N': 'Triclinic'}

    ibravDic = { \
        '1': 'Cubic', \
        '2': 'Cubic', \
        '3': 'Cubic', \
        '4': 'Hexagonal', \
        '5': 'Rhombohedral', \
        '6': 'Tetragonal', \
        '7': 'Tetragonal', \
        '8': 'Orthorhombic', \
        '9': 'Orthorhombic', \
        '10': 'Orthorhombic', \
        '11': 'Orthorhombic', \
        '12': 'Monoclinic', \
        '13': 'Monoclinic', \
        '14': 'Triclinic'}
    # --------------------------------------------------------------------------------------------------

    print(
        '\n     This implemetation uses stress-starin metod to calculate second order elastic constants ')

    num = 2
    mthd = 'Stress'
    ordr = 2
    order = 'second'

    # --------------------------------------------------------------------------------------------------

    # %!%!%--- Checking the input file exist ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!
    if (os.path.exists('POSCAR')):
        print(
            '\n.... Oops NOTICE: FPTE found "POSCAR". It will be used as input structure file to make strained structures.')
        INF = 'POSCAR'
    else:
        INF = input('\n>>>> Please enter the name of structure file: (e.g. POSCAR) ')
        if (os.path.exists(INF) == False):
            sys.exit('\n.... Oops ERROR: There is NO ' + INF + ' file !?!?!?    \n')

    # --------------------------------------------------------------------------------------------------
    def new_lattice(deformation, old_lattice):
        """this function converts the lattice to distorted lattices"""
        new_lat = np.zeros(shape=(3, 3))
        for i in range(3):
            new_lat[i] = np.dot(deformation, old_lattice[i])
        return new_lat

    # %!%!%--- Checking the "INPUT" files ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%
    if (os.path.exists('INCAR')):
        molecular_dynamics = False
        ISIF_value = []
        with open('INCAR') as file:
            for line in file:
                line = line.replace('=', ' = ')
                ISIF_p = re.findall(r'ISIF', line)
                ISYM_p = re.findall(r'ISYM', line)
                AIMD = re.findall(r'IBRION', line)
                if (ISIF_p and ISIF_p != -1):
                    ISIF_value = line.strip().split(' ')[-1]
                    if (int(ISIF_value) != 2):
                        sys.exit(
                            '\n Ooops ISIF = 3 can not be used for elastic constant calculations \n')
                if AIMD:
                    line = line.strip().split(' ')[-1]
                    if (int(line) == 0):
                        molecular_dynamics = True
                if (ISYM_p and ISYM_p != -1):
                    line = line.strip().split(' ')[-1]
                    if (int(line) != 0):
                        sys.exit('\n It is recommended to use ISYM = 0 \n')
            if len(ISIF_value) == 0:
                sys.exit('\n Ooops ISIF is missing \n')
        file.close()

    with open(INF, 'r') as f:
        texx_file = f.readlines()
        first_line = texx_file[0].strip(' ')
        scale = float(texx_file[1])
        lattice = np.array([[float(item) for item in line.split()] for line in texx_file[2:5]])
        lattice *= scale

        vasp5_symbols = False
        try:
            species_num = [int(i) for i in texx_file[5].strip().split()]
            ipos = 6
        except ValueError:
            vasp5_symbols = True
            species = texx_file[5].strip().split()
            species_num = [int(i) for i in texx_file[6].strip().split()]
            ipos = 7

        coordinate_type = texx_file[
            ipos]  ## will fix it later! right now only works for "Direct"
        positions = np.array([[float(i) for i in line.split()] for line in
                              texx_file[ipos + 1: ipos + 1 + sum(species_num)]])
    f.close()

    #
    # with open('POSCAR', 'r') as f:
    # c1, c2, c3 = f.readline()[3].split()
    #
    #
    # a1 = celldm1 * sqrt(CP[0,0]**2 + CP[0,1]**2 + CP[0,2]**2)
    # a2 = celldm1 * sqrt(CP[1,0]**2 + CP[1,1]**2 + CP[1,2]**2)
    # a3 = celldm1 * sqrt(CP[2,0]**2 + CP[2,1]**2 + CP[2,2]**2)
    # alpha = degrees(math.acos((CP[1,0]*CP[2,0]+CP[1,1]*CP[2,1]+CP[1,2]*CP[2,2])*celldm1**2/(a2*a3)))
    # beta  = degrees(math.acos((CP[0,0]*CP[2,0]+CP[0,1]*CP[2,1]+CP[0,2]*CP[2,2])*celldm1**2/(a1*a3)))
    # gamma = degrees(math.acos((CP[0,0]*CP[1,0]+CP[0,1]*CP[1,1]+CP[0,2]*CP[1,2])*celldm1**2/(a1*a2)))
    #
    # si = open('sgroup.in','w')
    # print >>si,'P'
    # print >>si,a1, a2, a3, alpha, beta, gamma
    # print >>si
    # print >>si, nat
    # for i in range(nat-1,-1,-1):
    #     print >>si, '%15.10f'%(float(OATPO[i][1])), \
    #                 '%15.10f'%(float(OATPO[i][2])), \
    #                 '%15.10f'%(float(OATPO[i][3]))
    #     print >>si, str(OATPO[i][0])
    # si.close()
    # --------------------------------------------------------------------------------------------------

    # %!%!%--- Calculating the Space-Group Number and classifying it ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!
    # os.system('sgroup sgroup.in 1>sgroup.out 2>sgroup.err; rm -f sgroup.in')
    #
    # if (os.path.getsize('sgroup.err') != 0):
    #     fer  = open('sgroup.err', 'r')
    #     lines= fer.readlines()
    #     print '\n.... Oops '+ lines[0]
    #     for i in range(1, len(lines)):
    #         print '                 '+ lines[i]
    #     fer.close()
    #     sys.exit()
    # else: os.system('rm -f sgroup.err')
    #
    # SGf   = open('sgroup.out', 'r')
    # SGlins= SGf.readlines()
    # SGf.close()
    #
    # for i in range(len(SGlins)):
    #     if (SGlins[i].find('Number and name of space group:') >= 0):
    #         SGN = int(float(SGlins[i].split()[6]))
    #         SGN_explanation = SGlins[i].strip()
    #         break
    #
    SGN = input('>>>> Please enter the Space Group number of the structure: ')
    SGN = int(SGN)

    if (1 <= SGN and SGN <= 2):  # Triclinic
        LC = 'N'
        ECs = 21

    elif (3 <= SGN and SGN <= 15):  # Monoclinic
        LC = 'M'
        ECs = 13

    elif (16 <= SGN and SGN <= 74):  # Orthorhombic
        LC = 'O'
        ECs = 9

    elif (75 <= SGN and SGN <= 88):  # Tetragonal II
        LC = 'TII'
        ECs = 7

    elif (89 <= SGN and SGN <= 142):  # Tetragonal I
        LC = 'TI'
        ECs = 6

    elif (143 <= SGN and SGN <= 148):  # Rhombohedral II
        LC = 'RII'
        ECs = 7

    elif (149 <= SGN and SGN <= 167):  # Rhombohedral I
        LC = 'RI'
        ECs = 6

    elif (168 <= SGN and SGN <= 176):  # Hexagonal II
        LC = 'HII'
        ECs = 5

    elif (177 <= SGN and SGN <= 194):  # Hexagonal I
        LC = 'HI'
        ECs = 5

    elif (195 <= SGN and SGN <= 206):  # Cubic II
        LC = 'CII'
        ECs = 3

    elif (207 <= SGN and SGN <= 230):  # Cubic I
        LC = 'CI'
        ECs = 3

    else:
        sys.exit('\n.... Oops ERROR: WRONG Space-Group Number !?!?!?\n')

    #####addd fix
    SGN_explanation = 'SG#'

    print('\n     ' + SGN_explanation + '\
        \n     ' + LC_Dic[LC] + ' structure in the Laue classification.\
        \n     This structure has ' + str(
        ECs) + ' independent ' + order + '-order elastic constants.')

    # if (ibrav != 0):
    #     if (ibrav == 4 and 143 <= SGN and SGN <= 167): ibrav = 5
    #
    #     if (ibravDic[str(ibrav)] != LT_Dic[LC]):
    #         sys.exit('\n.... Oops ERROR: ibrav = '+ str(ibrav) +', It means "'+ibravDic[str(ibrav)]+'" structure.'\
    #                  '\n                 But this structure can be represented by "'+LT_Dic[LC]+'" system.'\
    #                  '\n                 THEY ARE NOT COMPATIBLE. Please Look at sgroup.out\n')
    # --------------------------------------------------------------------------------------------------

    # %!%!%--- Reading the maximum Lagrangian strain ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!

    mdr = float(input('\n>>>> Please enter the maximum Lagrangian strain ' \
                      '\n     The suggested value is between 0.0010 and 0.0050: '))

    if (1 < mdr or mdr < 0):
        sys.exit(
            '\n.... Oops ERROR: The maximum Lagrangian strain is out of range !!!!!!    \n')

    mdr = round(mdr, 3)
    print('     The maximum Lagrangian strain is ' + str(mdr) + '\n')
    # --------------------------------------------------------------------------------------------------

    # %!%!%--- Reading the number of the distorted structures ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%
    NoP = input('>>>> Please enter the number of the distorted structures >= 2]: ')
    NoP = int(NoP)

    if (NoP < 1):
        sys.exit('\n.... Oops ERROR: The NUMBER of the distorted structures < 2 !!!!!!    \n')
    if (99 < NoP):
        sys.exit('\n.... Oops ERROR: The NUMBER of the distorted structures > 99 !!!!!!   \n')

    if (NoP % 2 == 0):
        NoP += 1
    print('     The number of the distorted structures is ' + str(NoP) + '\n')

    ptn = int((NoP - 1) / 2)

    if (mthd == 'Energy'): interval = 0.0001
    if (mthd == 'Stress'): interval = 0.00001

    if (mdr / ptn <= interval):
        sys.exit('.... Oops ERROR: The interval of the strain values is < ' + str(interval) + \
                 '\n                 Choose a larger maximum Lagrangian strain' \
                 '\n                 or a less number of distorted structures.\n')
    # --------------------------------------------------------------------------------------------------

    # %!%!%--- Writing the "INFO_FPTE" file ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!
    # D   = np.linalg.det(CP)
    # V0  = abs(celldm1**3*D)
    # INFO= open('INFO_FPTE','w')
    print('Order of elastic constants      =', ordr, \
          '\nMethod of calculation           =', mthd, \
          '\nDFT code name                   = VASP   ', \
          '\nMaximum Lagrangian strain       =', mdr, \
          '\nNumber of distorted structures  =', NoP, \
          '\nSpace-group number              =', SGN, file=open("INFO_FPTE", "a"))

    # '\nVolume of equilibrium unit cell =', V0, '[a.u^3]'  ,\
    # INFO.close()
    # --------------------------------------------------------------------------------------------------

    # %!%!%--- Directory Management ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%
    OLDlist = glob.glob('Dst??_old')
    for Dstn_old in OLDlist:
        shutil.rmtree(Dstn_old)

    Dstlist = glob.glob('Dst??')
    for Dstn in Dstlist:
        os.rename(Dstn, Dstn + '_old')

    if (os.path.exists('Structures_VASP_old')):
        shutil.rmtree('Structures_VASP_old')

    if (os.path.exists('Structures_VASP')):
        os.rename('Structures_VASP', 'Structures_VASP_old')
    # --------------------------------------------------------------------------------------------------

    if (LC == 'CI' or \
            LC == 'CII'):
        Lag_strain_list = ['36']
    if (LC == 'HI' or \
            LC == 'HII'):
        Lag_strain_list = ['36', '38']
    if (LC == 'RI' or \
            LC == 'RII'):
        Lag_strain_list = ['36', '38']
    if (LC == 'TI' or \
            LC == 'TII'):
        Lag_strain_list = ['36', '38']
    if (LC == 'O'):
        Lag_strain_list = ['36', '38', '40']
    if (LC == 'M'):
        Lag_strain_list = ['36', '37', '38', '39', '40']
    if (LC == 'N'):
        Lag_strain_list = ['36', '37', '38', '39', '40', '41']

    # %!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%#
    # %!% ----------------------------------- Structures maker ----------------------------------- %!%!#
    # %!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%#
    # M_old= CP ! fix

    M_old = lattice
    # fdis = open('Distorted_Parameters','w')
    cont1 = 0
    for i in Lag_strain_list:
        Ls_list = Ls_Dic[i]

        cont1 = cont1 + 1
        if (cont1 < 10):
            Dstn = 'Deform0' + str(cont1)
        else:
            Dstn = 'Deform' + str(cont1)

        try:
            os.mkdir(Dstn)
            os.chdir(Dstn)
        except FileExistsError as err:
            raise FolderNotClean(Dstn) from err

        print(Dstn + ', Lagrangian strain = ' + Ls_str[i],
              file=open("Distorted_Parameters", "a"))

        cont2 = 0
        for s in range(-ptn, ptn + 1):
            r = mdr * s / ptn
            if (s == 0):
                if (mthd == 'Energy'): r = 0.0001
                if (mthd == 'Stress'): r = 0.00001

            Ls = np.zeros(6)
            for i in range(6):
                Ls[i] = Ls_list[i]
            Lv = r * Ls

            # --- Lagrangian strain to physical strain (eta = eps + 0.5*eps*esp) -----------------------
            eta_matrix = np.zeros((3, 3))

            eta_matrix[0, 0] = Lv[0]
            eta_matrix[0, 1] = Lv[5] / 2.
            eta_matrix[0, 2] = Lv[4] / 2.

            eta_matrix[1, 0] = Lv[5] / 2.
            eta_matrix[1, 1] = Lv[1]
            eta_matrix[1, 2] = Lv[3] / 2.

            eta_matrix[2, 0] = Lv[4] / 2.
            eta_matrix[2, 1] = Lv[3] / 2.
            eta_matrix[2, 2] = Lv[2]

            norm = 1.0
            eps_matrix = eta_matrix
            if (np.linalg.norm(eta_matrix) > 0.7):
                sys.exit('\n.... Oops ERROR: Too large deformation!\n')

            while (norm > 1.e-10):
                x = eta_matrix - np.dot(eps_matrix, eps_matrix) / 2.
                norm = np.linalg.norm(x - eps_matrix)
                eps_matrix = x

            # --- Calculating the M_new matrix ---------------------------------------------------------
            i_matrix = np.array([[1., 0., 0.],
                                 [0., 1., 0.],
                                 [0., 0., 1.]])
            def_matrix = i_matrix + eps_matrix
            #    M_new      = dot(M_old, def_matrix)
            M_new = new_lattice(def_matrix, lattice)
            # ------------------------------------------------------------------------------------------
            cont2 = cont2 + 1
            if (cont2 < 10):
                Dstn_cont2 = Dstn + '_0' + str(cont2)
            else:
                Dstn_cont2 = Dstn + '_' + str(cont2)

            print(Dstn_cont2 + ',  eta = ' + str(r), file=open("Distorted_Parameters", "a"))
            for j in range(3):
                print('V' + str(j + 1) + ' --=>', '%15.10f' % (M_new[j, 0]),
                      '%15.10f' % (M_new[j, 1]), '%15.10f' % (M_new[j, 2]),
                      file=open("Distorted_Parameters", "a"))
            print(" ", file=open("Distorted_Parameters", "a"))

            # --- Writing the structure file -----------------------------------------------------------
            os.mkdir(Dstn_cont2)
            os.chdir(Dstn_cont2)
            #
            # fo = open(Dstn_cont2 +'.in', 'w')
            # print >>fo, Dstn_cont2
            # print >>fo, TMP
            # for j in range(3):
            #     print >>fo, '%15.10f'%(M_new[j,0]), '%15.10f'%(M_new[j,1]), '%15.10f'%(M_new[j,2])
            # fo.close()

            new_latt_conv = new_lattice(def_matrix, lattice)
            with open('POSCAR', 'w') as f:
                f.write('this structure has been generated with applied strains' + '\n')
                f.write(str(scale) + '\n')
                f.write('\n'.join(
                    '   '.join("%.10f" % cell for cell in row) for row in new_latt_conv) + '\n')
                if vasp5_symbols:
                    f.write('  '.join("%4s" % symbols for symbols in species) + '\n')
                f.write('  '.join("%4s" % atom_num for atom_num in species_num) + '\n')
                f.write(coordinate_type)
                f.write(
                    '\n'.join('  '.join("%.10f" % coor for coor in line) for line in positions))
            f.close()
            ####
            if (os.path.exists('../../INCAR') == False or os.path.exists(
                    '../../POTCAR') == False):
                sys.exit('\n.... Oops ERROR: There is NO INCAR or POTCAR file !?!?!?    \n')
            os.system('cp ../../INCAR ./INCAR')
            if os.path.exists('../../KPOINTS'):
                os.system('cp ../../KPOINTS ./KPOINTS')
            os.system('cp ../../POTCAR ./POTCAR')
            ### This part is only for bsub system! one need to modify it for any other submission system
            submit_job_file = open('Submit_Job', 'w')
            if molecular_dynamics:
                submit_job_file.write('cat /dev/null                \n ')
                submit_job_file.write('#!/bin/sh"                   \n ')
                submit_job_file.write('# BSUB -sp 100               \n ')
                submit_job_file.write('# BSUB -q  intel             \n ')
                submit_job_file.write('# BSUB -a  intelmpi          \n ')
                submit_job_file.write('# BSUB -o  output            \n ')
                submit_job_file.write('# BSUB -R  16                \n ')
                submit_job_file.write('# BSUB -W  1000:00           \n ')
                submit_job_file.write('# BSUB -n  16                \n ')
                submit_job_file.write('# BSUB -J  FPTE' + Dstn_cont2 + '\n')
                submit_job_file.write('mpirun.lsf vasp-aimd > log   \n ')
            else:
                submit_job_file.write('cat /dev/null                \n ')
                submit_job_file.write('#!/bin/sh"                   \n ')
                submit_job_file.write('# BSUB -sp 100               \n ')
                submit_job_file.write('# BSUB -q  intel             \n ')
                submit_job_file.write('# BSUB -a  intelmpi          \n ')
                submit_job_file.write('# BSUB -o  output            \n ')
                submit_job_file.write('# BSUB -R  8                 \n ')
                submit_job_file.write('# BSUB -W  1000:00           \n ')
                submit_job_file.write('# BSUB -n  8                 \n ')
                submit_job_file.write('# BSUB -J  FPTE' + Dstn_cont2 + '\n')
                submit_job_file.write('mpirun.lsf vasp-vdw > log    \n ')
            submit_job_file.close()
            os.system('bsub < Submit_Job')

            # --------------------------------------------------------------------------------------------------
            os.chdir('../')
        os.chdir('../')
    # fdis.close()
    # os.system('mkdir Structures_VASP; cp Dst??/Dst??_??/POSCAR Structures_VASP/')
    # --------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    fpte_setup()
