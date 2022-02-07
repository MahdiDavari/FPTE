#!/usr/bin/env python
# %!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%#
# %%% --------------------------------- FPTE_Analyze_Stress -------------------------------- %%%#
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
# python FPTE_Analyze_Stress.py
#        FPTE_Analyze_Stress
# 
# EXPLANATION:
# 
# __________________________________________________________________________________________________

import copy
import os
import os.path
import re
import shutil
import sys
import warnings

import numpy as np

from .FPTE_Ensemble_Average_AIMD import fpte_ensemle_average_aimd


def fpte_analyze():
    ###------ CHECKING THE INPUT FILES ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%
    if (os.path.exists('INCAR')):
        molecular_dynamics = False
        with open('INCAR') as file:
            for line in file:
                line = line.replace('=', ' = ')
                AIMD = re.findall(r'IBRION', line)
                if AIMD:
                    line = line.strip().split(' ')[-1]
                    if (int(line) == 0):
                        molecular_dynamics = True
                        print('Please be patient! This may take a few minutes')
        file.close()

    # %!%!%--- SUBROUTINS AND FUNCTIONS ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%
    def sortlist(lst1, lst2):
        temp = copy.copy(lst1)

        lst3 = []
        lst4 = []

        temp.sort()

        for i in range(len(lst1)):
            lst3.append(lst1[lst1.index(temp[i])])
            lst4.append(lst2[lst1.index(temp[i])])

        return lst3, lst4

    # --------------------------------------------------------------------------------------------------

    # %!%!%--- Dictionaries ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%
    Ls_Dic = { \
        '36': [1., 2., 3., 4., 5., 6.], \
        '37': [-2., 1., 4., -3., 6., -5.], \
        '38': [3., -5., -1., 6., 2., -4.], \
        '39': [-4., -6., 5., 1., -3., 2.], \
        '40': [5., 4., 6., -2., -1., -3.], \
        '41': [-6., 3., -2., 5., -4., 1.]}

    # %!%!%--- Reading the "I'NFO_FPTE" file ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%
    INFO = open('INFO_FPTE', 'r')

    l1 = INFO.readline()
    ordr = int(l1.split()[-1])

    if (ordr != 2 and ordr != 3):
        sys.exit('\n.... Oops ERROR: The order of the elastic constant is NOT clear !?!?!? \
                \n                 Something is WRONG in INFO_FPTE file.          \n')

    l2 = INFO.readline()
    mthd = l2.split()[-1]

    if (mthd != 'Stress' and mthd != 'Energy'):
        sys.exit('\n.... Oops ERROR: The method of the calculation is NOT clear !?!?!? \
                \n                 Something is WRONG in INFO_FPTE file.          \n')

    l3 = INFO.readline()
    cod = l3.split()[-1]

    if (cod != 'WIEN2k' and cod != 'exiting' and cod != 'ESPRESSO' and cod != 'VASP'):
        sys.exit('\n.... Oops ERROR: The DFT code is NOT clear !?!?!? \
                \n                 Something is WRONG in INFO_FPTE file.          \n')

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

    # %!%!%--- Calculating the Space-Group Number and classifying it ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!
    if (1 <= SGN and SGN <= 2):  # Triclinic
        LC = 'N'

    elif (3 <= SGN and SGN <= 15):  # Monoclinic
        LC = 'M'

    elif (16 <= SGN and SGN <= 74):  # Orthorhombic
        LC = 'O'

    elif (75 <= SGN and SGN <= 88):  # Tetragonal II
        LC = 'TII'

    elif (89 <= SGN and SGN <= 142):  # Tetragonal I
        LC = 'TI'

    elif (143 <= SGN and SGN <= 148):  # Rhombohedral II
        LC = 'RII'

    elif (149 <= SGN and SGN <= 167):  # Rhombohedral I
        LC = 'RI'

    elif (168 <= SGN and SGN <= 176):  # Hexagonal II
        LC = 'HII'

    elif (177 <= SGN and SGN <= 194):  # Hexagonal I
        LC = 'HI'

    elif (195 <= SGN and SGN <= 206):  # Cubic II
        LC = 'CII'

    elif (207 <= SGN and SGN <= 230):  # Cubic I
        LC = 'CI'

    else:
        sys.exit('\n.... Oops ERROR: WRONG Space-Group Number !?!?!?    \n')
    # --------------------------------------------------------------------------------------------------

    # %!%!%--- Reading the stresses ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%
    if (mthd == 'Stress'):
        if (ordr == 2):
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

        if (ordr == 3):
            if (LC == 'CI'):
                sys.exit('\n.... Oops SORRY: Not implemented yet. \n')
            if (LC == 'CII'):
                sys.exit('\n.... Oops SORRY: Not implemented yet. \n')
            if (LC == 'HI'):
                sys.exit('\n.... Oops SORRY: Not implemented yet. \n')
            if (LC == 'HII'):
                sys.exit('\n.... Oops SORRY: Not implemented yet. \n')
            if (LC == 'RI'):
                sys.exit('\n.... Oops SORRY: Not implemented yet. \n')
            if (LC == 'RII'):
                sys.exit('\n.... Oops SORRY: Not implemented yet. \n')
            if (LC == 'TI'):
                sys.exit('\n.... Oops SORRY: Not implemented yet. \n')
            if (LC == 'TII'):
                sys.exit('\n.... Oops SORRY: Not implemented yet. \n')
            if (LC == 'O'):
                sys.exit('\n.... Oops SORRY: Not implemented yet. \n')
            if (LC == 'M'):
                sys.exit('\n.... Oops SORRY: Not implemented yet. \n')
            if (LC == 'N'):
                sys.exit('\n.... Oops SORRY: Not implemented yet. \n')

    cont1 = 0
    if molecular_dynamics:
        exclude_steps = input(
            '\n>>>> In the ab initio MD, you need to exclude at least 1 ps of the ionic steps, \n' +
            '>>>> the default is 1500 steps (each step = 1fs). \n' +
            ' \n' +
            '>>>> Please press ENTER to confirm or specify a different value: ')

    for i in Lag_strain_list:
        Ls_list = Ls_Dic[i]

        cont1 = cont1 + 1
        if (cont1 < 10):
            Dstn = 'Deform0' + str(cont1)
        else:
            Dstn = 'Deform' + str(cont1)
        if (os.path.exists(Dstn)):
            os.chdir(Dstn)
        else:
            sys.exit('.... Oops ERROR: Where is the ' + Dstn + ' directory !?!?!?    \n')

        flstres = open(Dstn + '_Lagrangian-stress.dat', 'w')
        fpstres = open(Dstn + '_Physical-stress.dat', 'w')

        flstres.write(
            ' Lagrangian strain and Lagrangian stresses (LS) in Voigt notation for ' + Dstn + '. \n')
        l = ' Lag. strain          LS1              LS2              LS3              LS4              LS5              LS6 \n'
        flstres.write(l)
        fpstres.write(
            ' Lagrangian strain and physical stresses (PS) in Voigt notation for ' + Dstn + '. \n')
        fpstres.write(
            ' Lag. strain         PS1          PS2          PS3          PS4          PS5          PS6  \n')

        for j in range(1, NoP + 1):
            if (j < 10):
                Dstn_num = Dstn + '_0' + str(j)
            else:
                Dstn_num = Dstn + '_' + str(j)

            if (os.path.exists(Dstn_num)):
                os.chdir(Dstn_num)

                s = j - (NoP + 1) / 2
                r = 2 * mdr * s / (NoP - 1)
                if (s == 0): r = 0.00001

                le = np.zeros(6)
                for i in range(6):
                    le[i] = Ls_list[i]
                Lv = r * le
                # --- Lag. to phy. strain (eta = eps + 0.5*eps*esp) and making the deformation matrix --
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

                # --- Calculating the deformation matrix -----------------------------------------------
                i_matrix = np.array([[1., 0., 0.],
                                     [0., 1., 0.],
                                     [0., 0., 1.]])
                def_matrix = i_matrix + eps_matrix

                # --- Reading the physical stresses from the output files ------------------------------
                sig = np.zeros((3, 3))

                if (cod == 'VASP'):
                    if (os.path.exists('OUTCAR')):
                        if molecular_dynamics:
                            sys.stdout = open(Dstn_num + "-stress.dat", "w")
                            if exclude_steps:
                                exclude_steps = int(exclude_steps)
                                fpte_ensemle_average_aimd(exclude_steps)
                            else:
                                fpte_ensemle_average_aimd()

                            sys.stdout = open('/dev/stdout', 'w')

                        else:
                            os.system(
                                "grep -A 1 'in kB' OUTCAR  | tail -n 2 >" + Dstn_num + "-stress.dat")

                        if (os.path.getsize(Dstn_num + '-stress.dat') != 0):
                            with open(Dstn_num + '-stress.dat', 'r') as fstres:
                                l1 = fstres.readline()
                                l2 = fstres.readline()
                            pullay_stree = l2.split()[-2]
                            external_pressure = l2.split()[-7]
                            print(
                                'The external pressure is {0:.1f} kB, and the Pullay stress is {1:.1f} kB.'.format(
                                    float(external_pressure), float(pullay_stree)))
                            sig[0, 0] = str(float(l1.split()[-6]) - float(pullay_stree))
                            sig[0, 1] = l1.split()[-3]
                            sig[0, 2] = l1.split()[-1]

                            sig[1, 0] = l1.split()[-3]
                            sig[1, 1] = str(float(l1.split()[-5]) - float(pullay_stree))
                            sig[1, 2] = l1.split()[-2]

                            sig[2, 0] = l1.split()[-1]
                            sig[2, 1] = l1.split()[-2]
                            sig[2, 2] = str(float(l1.split()[-4]) - float(pullay_stree))

                        else:
                            print('\n.... Oops WARNING: No Stresses in "' + \
                                  Dstn_num + '.out" file !?!?!?\n')

                    else:
                        print('\n.... Oops WARNING: Where is the OUTCAR file !?!?!?\n')

                # --------------------------------------------------------------------------------------------------
                dm = def_matrix
                idm = np.linalg.inv(dm)
                tao = np.linalg.det(dm) * np.dot(idm, np.dot(sig, idm))

                if (r > 0):
                    strain = '+%12.10f' % r
                else:
                    strain = '%13.10f' % r
                fpstres.write(strain + '   ' + '%10.3f' % sig[0, 0] \
                              + '   ' + '%10.3f' % sig[1, 1] \
                              + '   ' + '%10.3f' % sig[2, 2] \
                              + '   ' + '%10.3f' % sig[1, 2] \
                              + '   ' + '%10.3f' % sig[0, 2] \
                              + '   ' + '%10.3f' % sig[0, 1] + '\n')

                flstres.write(strain + '   ' + '%14.8f' % tao[0, 0] \
                              + '   ' + '%14.8f' % tao[1, 1] \
                              + '   ' + '%14.8f' % tao[2, 2] \
                              + '   ' + '%14.8f' % tao[1, 2] \
                              + '   ' + '%14.8f' % tao[0, 2] \
                              + '   ' + '%14.8f' % tao[0, 1] + '\n')
                os.chdir('../src/')
        flstres.close()
        fpstres.close()
        os.chdir('../src/')
    # --------------------------------------------------------------------------------------------------

    warnings.simplefilter('ignore', np.RankWarning)

    # %!%!%--- Directory management ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%
    if (os.path.exists('Stress-vs-Strain_old')):
        shutil.rmtree('Stress-vs-Strain_old')

    if (os.path.exists('Stress-vs-Strain')):
        os.rename('Stress-vs-Strain', 'Stress-vs-Strain_old')

    os.mkdir('Stress-vs-Strain')
    os.chdir('Stress-vs-Strain')

    os.system('cp -f ../Deform??/Deform??_Lagrangian-stress.dat .')

    # %!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%#
    # %!%!% ------------ Calculating the second derivative and Cross-Validation Error ----------- %!%!%#
    # %!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%#
    if (cod == 'VASP'):
        CONV = (1 - ordr) / 10.

    # NoD = Number of Deformation
    NoD = len(Lag_strain_list)

    for i in range(1, NoD + 1):
        if (i < 10):
            Dstn = 'Deform0' + str(i)
        else:
            Dstn = 'Deform' + str(i)

        LSi_dic = {1: 'LS1', 2: 'LS2', 3: 'LS3', 4: 'LS4', 5: 'LS5', 6: 'LS6'}
        for l in range(1, 7):

            if (ordr == 2):
                fD = open(Dstn + '_' + LSi_dic[l] + '_d1S.dat', 'w')
            if (ordr == 3):
                fD = open(Dstn + '_' + LSi_dic[l] + '_d2S.dat', 'w')

            fE = open(Dstn + '_' + LSi_dic[l] + '_CVe.dat', 'w')
            fD.write('# Max. eta    SUM(Cij) \n#')
            fE.write('# Max. eta    Cross-Validation error   \n#')

            for j in range(ordr + 3, ordr - 2, -2):
                if (j == 2):
                    nth = '2nd'
                elif (j == 3):
                    nth = '3rd'
                else:
                    nth = str(j) + 'th'

                fD.write('\n# ' + nth + ' order fit.')
                fE.write('\n# ' + nth + ' order fit.')

                # --- Reading the input files ----------------------------------------------------------
                nl = 0
                ls1 = []
                ls2 = []
                ls3 = []
                ls4 = []
                ls5 = []
                ls6 = []
                strain = []

                eta_strs = open(Dstn + '_Lagrangian-stress.dat', 'r')
                eta_strs.readline()
                eta_strs.readline()

                while (nl < NoP):
                    line = eta_strs.readline()
                    if (line == ''): break
                    line = line.strip().split()

                    if (len(line) == 7):
                        nl += 1
                        eta, lsxx, lsyy, lszz, lsyz, lsxz, lsxy = line
                        strain.append(float(eta))
                        ls1.append(float(lsxx))
                        ls2.append(float(lsyy))
                        ls3.append(float(lszz))
                        ls4.append(float(lsyz))
                        ls5.append(float(lsxz))
                        ls6.append(float(lsxy))
                    elif (len(line) == 0):
                        pass
                    else:
                        sys.exit(
                            '\n.... Oops ERROR: Strain and Stresses are NOT defined correctly in "' + Dstn + \
                            '_Lagrangian-stress.dat" !?!?!?\n')

                eta_strs.close()

                if (l == 1): stress = ls1
                if (l == 2): stress = ls2
                if (l == 3): stress = ls3
                if (l == 4): stress = ls4
                if (l == 5): stress = ls5
                if (l == 6): stress = ls6
                strain, stress = sortlist(strain, stress)
                strain0 = copy.copy(strain)
                stress0 = copy.copy(stress)

                # --- first derivative coefficient calculation -----------------------------------------
                while (len(strain) > j):
                    emax = max(strain)
                    emin = min(strain)
                    emax = max(abs(emin), abs(emax))
                    coeffs = np.polyfit(strain, stress, j)
                    if (ordr == 2):
                        Cij = coeffs[j - 1] * CONV  # in GPa unit
                    if (ordr == 3):
                        Cij = coeffs[j - 2] * CONV * 0.001  # in TPa unit

                    fD.write('%13.10f' % emax + ' ' + '%18.6f' % Cij)
                    if (abs(strain[0] + emax) < 1.e-7):
                        strain.pop(0)
                        stress.pop(0)
                    if (abs(strain[len(strain) - 1] - emax) < 1.e-7):
                        strain.pop()
                        stress.pop()

                strain = copy.copy(strain0)
                stress = copy.copy(stress0)
                while (len(strain) > j + 1):
                    emax = max(strain)
                    emin = min(strain)
                    emax = max(abs(emin), abs(emax))

                    S = 0
                    for k in range(len(strain)):
                        Y = stress[k]
                        etatmp = []
                        strtmp = []
                        for q in range(len(strain)):
                            if (q == k):
                                pass
                            else:
                                etatmp.append(strain[q])
                                strtmp.append(stress[q])
                        Yfit = np.polyval(np.polyfit(etatmp, strtmp, j), strain[k])
                        S = S + (Yfit - Y) ** 2

                    CV = np.sqrt(S / len(strain))
                    fE.write('%13.10f' % emax + ' ' + '%13.10f' % CV)

                    if (abs(strain[0] + emax) < 1.e-7):
                        strain.pop(0)
                        stress.pop(0)
                    if (abs(strain[len(strain) - 1] - emax) < 1.e-7):
                        strain.pop()
                        stress.pop()
            fD.close()
            fE.close()

            # --- Plotting -----------------------------------------------------------------------------
            # if (os.path.exists('Grace.par') == False):
            #     os.system("cp -f $FPTEROOT/Grace.par .")
            #
            # Gf    = open('Grace.par', 'r')
            # Glines= Gf.readlines()
            # Gf.close()
            #
            # TMP = []
            # if (ordr == 2):
            #     for k in range(95, 122):
            #         TMP.append(Glines[k])
            #
            # if (ordr == 3):
            #     for k in range(125, 151):
            #         TMP.append(Glines[k])
            #
            # for k in range(164, 219):
            #     TMP.append(Glines[k])
            #
            # TMP.insert(82,'    s2 legend  " n = '+str(ordr-1)+'"\n')
            # TMP.insert(74,'    s1 legend  " n = '+str(ordr+1)+'"\n')
            # TMP.insert(66,'    s0 legend  " n = '+str(ordr+3)+'"\n')
            # TMP.insert(29,'    subtitle "Plot for '+ Dstn +'_'+LSi_dic[l]+' , n = Order of polynomial fit"\n')
            #
            # GdE = open(Dstn+'_'+LSi_dic[l]+'_d'+str(ordr-1)+'S.par', 'w')
            # for k in range(len(TMP)):
            #     print >>GdE, TMP[k],
            # GdE.close()
            #
            # os.system('xmgrace '+Dstn+'_'+LSi_dic[l]+'_d'+str(ordr-1)+'S.dat -param '+Dstn+'_'+LSi_dic[l]+'_d1S.par -saveall '\
            #                     +Dstn+'_'+LSi_dic[l]+'_d'+str(ordr-1)+'S.agr &')
            #
            # TMP = []
            # for k in range(154, 162):
            #     TMP.append(Glines[k])
            #
            # for k in range(164, 219):
            #     TMP.append(Glines[k])
            #
            # TMP.insert(63,'    s2 legend  " n = '+str(ordr-1)+'"\n')
            # TMP.insert(55,'    s1 legend  " n = '+str(ordr+1)+'"\n')
            # TMP.insert(47,'    s0 legend  " n = '+str(ordr+3)+'"\n')
            # TMP.insert(10,'    subtitle "Plot for '+ Dstn +'_'+LSi_dic[l]+' , n = Order of polynomial fit"\n')
            #
            # CVe = open(Dstn+'_'+LSi_dic[l]+'_CVe.par', 'w')
            # for k in range(len(TMP)):
            #     print >>CVe, TMP[k],
            # CVe.close()
            #
            # os.system('xmgrace '+Dstn+'_'+LSi_dic[l]+'_CVe.dat -param '+Dstn+'_'+LSi_dic[l]+'_CVe.par -saveall '\
            #                     +Dstn+'_'+LSi_dic[l]+'_CVe.agr &')

    os.chdir('../src/')

    # --- Writing the "FPTE_???.in" file ------------------------------------------------------------

    if (ordr == 2):
        orth = '2nd'
        fri = open('FPTE_' + orth + '.in', 'w')
        for i in range(1, NoD + 1):
            if (i < 10):
                Dstn = 'Deform0' + str(i)
            else:
                Dstn = 'Deform' + str(i)

            fri.write(Dstn + '   ' + str(mdr) + '      ' + str(mdr) + '      ' + str(
                mdr) + '      ' + str(mdr) + '      ' + str(mdr) + '       ' + str(mdr) + '  \n' \
                                                                                          '       2             2            2             2             2             2       \n')
        fri.close()

    if (ordr == 3):
        orth = '3rd'
        sys.exit('\n.... Oops SORRY: Not implemented yet. \n')

    # --------------------------------------------------------------------------------------------------
    os.system('rm -f Stress-vs-Strain/Grace.par')


if __name__ == "__main__":
    fpte_analyze()
