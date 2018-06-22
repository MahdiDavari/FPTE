#!/usr/bin/python3

import numpy as np
import argparse
import sys

__author__  =   "Mahdi Davari"
__version__ =   "1.0.0"
__email__   =   "Mahdi.Davari@StonyBrook.edu"
__date__    =   "June 20, 2018"


parser = argparse.ArgumentParser(description='''
Lattice strain function |
Author: Mahdi Davari |
Last updated: June, 2018''')


parser.add_argument('-i', metavar='files', type=str, nargs=1,
                    help='Structure Input file , e.g. -f POSCAR. the default is "POSCAR"')
parser.add_argument('-lat', metavar='nodes', type=str, nargs=1,
                    help='Define the type of lattice. For each crystal lattice, we have different deformation matrices. You can use  --lat HEX. Required')
parser.add_argument('-delta', metavar='delta', type=str, nargs=1,
                    help='strain delta value , e.g. -delta 0.02. the default is "0.01"')
parser.add_argument('-o', metavar='result', type=str, nargs=1,
                    help='Strained strctures Output files, e.g. -o HEX_POSCAR. Default: POSCAR-#')


args = parser.parse_args()
if args.lat:
    lat_type = args.lat[0]
    if args.i:
        files_name = args.i[0]
    else:
        files_name = "POSCAR"
    if args.o:
        output = args.o[0]
    else:
        output = "POSCAR"
    if args.delta:
        e = float(args.delta[0])
    else:
        e = 0.01
else:
    sys.stderr.write('You should provide lattice type, i.e., -lat. For more information, use -h')
    sys.exit(1)


def clean_lines(string_list, remove_empty_lines=True):
    """
    Strips whitespace, carriage returns and empty lines from a list of strings.
    Args:
        string_list: List of strings
        remove_empty_lines: Set to True to skip lines which are empty after
            stripping.
    Returns:
        List of clean strings with no whitespaces.
    """

    for s in string_list:
        clean_s = s
        if '#' in s:
            ind = s.index('#')
            clean_s = s[:ind]
        clean_s = clean_s.strip()
        if (not remove_empty_lines) or clean_s != '':
            yield clean_s


def new_lattice(deformation, old_lattice):
    """this function converts the lattice to distorted lattices"""
    new_lat = np.zeros(shape=(3, 3))
    for i in range(3):
        new_lat[i] = np.matmul(deformation, old_lattice[i])
    return new_lat


with open(files_name, 'r') as f:
    texx_file = f.readlines()
    first_line = texx_file[0].strip(' ')
    scale=float(texx_file[1])
    lattice= np.array([[float(item) for item in line.split()] for line in texx_file[2:5]])
    species = texx_file[5].split(' ')
    species_num = texx_file[6].split(' ')
    coordinate_type = texx_file[7] ## will fix it later! right now only works for "Direct"
    try:
        symbols = texx_file[5].split()
        natoms = [int(i) for i in texx_file[6].split()]
    except ValueError:
        print('check your POSCAR')
    positions = np.array([[float(i) for i in line.split()] for line in texx_file[8:8+sum(natoms)]])
    f.close()


for strain_sing in [e, -e]:
    e = strain_sing   ###### fix it later

    if lat_type in ["CUBIC", "cubic", "CUB"]:
        d1 = np.array([[1 + e, 0.00, 0.0],
                       [0.0,   1.00, 0.0],
                       [0.0,   0.00, 1.0]])

        d2 = np.array([[1.0,    e,   0.0],
                      [e,     1.0,  0.0],
                      [0.0,   0.0,  1.0]])

        deformations = [d1, d2]

    elif lat_type in ["HEX", "hexagonal", "hex"]:
        unity = np.array([[1.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0],
                          [0.0, 0.0, 1.0]])

        d1 = np.array([[1 + e, 0.0, 0.0],
                       [0.0, 1 + e, 0.0],
                       [0.0, 0.0, 1.0]])

        d2 = np.array([[np.sqrt((1 + e) / (1 - e)), 0.000000000000000000, 0.00000000000000],
                       [0.000000000000000000, np.sqrt((1 - e) / (1 + e)), 0.00000000000000],
                       [0.000000000000000000, 0.000000000000000000, 1.00000000000000]])

        d3 = np.array([[1.0, 0.0, 0.0],
                       [0.0, 1.0, 0.0],
                       [0.0, 0.0, 1.0 + e]])

        d4 = np.array([[1.0, 0.0, e],
                       [0.0, 1.0, 0.0],
                       [e, 0.0, 1.0]])

        d5 = np.array([[(1 + e) ** (-1 / 3), 0.0000000000, 0.00000000000],
                       [0.0000000000, (1 + e) ** (-1 / 3), 0.00000000000],
                       [0.0000000000, 0.0000000000, (1 + e) ** (2 / 3)]])
        deformations = [d1, d2, d3, d4, d5]


    elif lat_type in ["orthorhombic", "ORTH", "ORTHORHOMBIC"]:
        d1 = np.array([[1.0 + e, 0.0, 0.0],
                       [0.0,     1.0, 0.0],
                       [0.0,     0.0, 1.0]])

        d2 = np.array([[1.0, 0.0,     0.0],
                       [0.0, 1.0 + e, 0.0],
                       [0.0, 0.0,     1.0]])

        d3 = np.array([[1.0, 0.0, 0.0],
                       [0.0, 1.0, 0.0],
                       [0.0, 0.0, 1.0 + e]])

        d4 = np.array([[1 / ((1 - e ** 2) ** (1 / 3)), 0.000000000000000000000000000, 0.000000000000000000000000000],
                       [0.000000000000000000000000000, 1 / ((1 - e ** 2) ** (1 / 3)), e / ((1 - e ** 2) ** (1 / 3))],
                       [0.000000000000000000000000000, e / ((1 - e ** 2) ** (1 / 3)), 1 / ((1 - e ** 2) ** (1 / 3))]])

        d5 = np.array([[1 / ((1 - e ** 2) ** (1 / 3)), 0.00000000000000000,           e / ((1 - e ** 2) ** (1 / 3))],
                       [0.00000000000000000,           1 / ((1 - e ** 2) ** (1 / 3)), 0.000000000000000000000000000],
                       [e / ((1 - e ** 2) ** (1 / 3)), 0.00000000000000000,           1 / ((1 - e ** 2) ** (1 / 3))]])

        d6 = np.array([[1 / ((1 - e ** 2) ** (1 / 3)), e / ((1 - e ** 2) ** (1 / 3)), 0.0000000000000000000000000000],
                       [e / ((1 - e ** 2) ** (1 / 3)), 1 / ((1 - e ** 2) ** (1 / 3)), 0.0000000000000000000000000000],
                       [0.000000000000000000000000000, 0.000000000000000000000000000, 1 / ((1 - e ** 2) ** (1 / 3))]])

        d7 = np.array([[(1 + e) / ((1 - e ** 2) ** (1 / 3)), 0.000000000000000000000, 0.00000000000000000],
              [0.000000000000000000000, (1 - e) / ((1 - e ** 2) ** (1 / 3)), 0.00000000000000000],
              [0.000000000000000000000, 0.000000000000000000000, 1 / ((1 - e ** 2) ** (1 / 3))]])

        d8 = np.array([[(1 + e) / ((1 - e ** 2) ** (1 / 3)), 0.00000000000000000, 0.000000000000000000000],
              [0.000000000000000000000, 1 / ((1 - e ** 2) ** (1 / 3)), 0.000000000000000000000],
              [0.000000000000000000000, 0.00000000000000000, (1 - e) / ((1 - e ** 2) ** (1 / 3))]])

        d9 = np.array([[1 / ((1 - e ** 2) ** (1 / 3)), 0.000000000000000000000, 0.000000000000000000000],
              [0.00000000000000000, (1 + e) / ((1 + e ** 2) ** (1 / 3)), 0.000000000000000000000],
              [0.00000000000000000, 0.000000000000000000000, (1 - e) / ((1 - e ** 2) ** (1 / 3))]])

        shear_distortion = [[1.000, e / 2.0, e / 2.0],
                            [e / 2.0, 1.000, e / 2.0],
                            [e / 2.0, e / 2.0, 1.000]]
        deformations = [d1, d2, d3, d4, d5, d6, d7, d8, d9]

    else:
        print('Deformation matrices for this crystal class is not implemented yet')
        exit()


    index = 0
    for i in deformations:
        index += 1
        new_latt_conv = new_lattice(i, lattice)
        output_file_name = output+str(int(np.sign(strain_sing)))+'--'+str(index)
        with open(output_file_name, 'a+') as f:
            f.write(str(first_line))
            f.write(str(scale)+'\n')
            f.write('%40s' % ('\n'.join(' '.join(str(cell) for cell in row) for row in new_latt_conv)+'\n'))
            f.write(' '.join(str(symbols) for symbols in species))#+'\n')
            f.write(' '.join(str(atom_num) for atom_num in species_num))#+'\n')
            f.write(coordinate_type)
            f.write('\n'.join(' '.join(str(coor) for coor in line) for line in positions))
        f.close()

