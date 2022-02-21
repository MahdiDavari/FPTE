#!/usr/bin/env python
""" This file discards the initial ionic steps in order to reach equilibration.
It is recommended to discard at least 1 ps - the default is 1000 steps.
"""
import os
import sys

__author__ = "Mahdi Davari"
__version__ = "1.2.0"
__email__ = "Mahdi.Davari@StonyBrook.edu"
__date__ = "June 20, 2018"


def fpte_ensemle_average_aimd(exclude_steps=1500):
    # parser = argparse.ArgumentParser(description='''
    # Lattice strain function |
    # Author: Mahdi Davari |
    # Last updated: June, 2018''')

    # parser.add_argument('-exclude', metavar='number', type=str, nargs=1,
    #                     help='In the Ab Initio MD, one need to exclude at least 1 ps of the ionic steps, the default is 1000 steps (1fs)')

    # args = parser.parse_args()
    # if args.exclude:
    # exc_steps = int(args.exclude[0])
    # else:
    # exc_steps = 1000

    if os.path.exists("OSZICAR") == False or os.path.exists("OUTCAR") == False:
        sys.exit("\n.... Oops ERROR: There is NO OUTCAR or OSZICAR file !?!?!?    \n")

    os.system("rm -f tmp_file")
    os.system("rm -f tmp_sig")
    os.system("rm -f tmp_pullay")

    os.system(
        "grep T= OSZICAR  | awk 'BEGIN {T=0.} {T+=$3} END {print T , $1}'  >   tmp_file  "
    )
    os.system("grep T= OSZICAR  | wc -l   >>   tmp_file  ")

    with open("tmp_file") as f:
        T, tot = f.readline().split()
        T = int(T)
        tot = int(f.readline().strip())
        f.close()

    equilibrated = tot - exclude_steps
    if exclude_steps > tot or exclude_steps < 0:
        sys.exit(
            "\n.... Oops ERROR - your discarded part is higher than the total ionic steps:  \n"
        )

    # print('>>>>>> Your ensemble average is for '+ str(equilibrated) + ' ionic steps')
    os.system("grep  'Total+kin' OUTCAR | tail -" + str(equilibrated) + "  > tmp_sig")
    os.system(
        "grep  'Pullay stress' OUTCAR | tail -" + str(equilibrated) + "  > tmp_pullay"
    )

    for i in range(6):
        os.system(
            "grep 'Total+kin' tmp_sig | awk 'BEGIN {sig=0.} {sig+=$"
            + str(i + 2)
            + "} END {print sig/"
            + str(equilibrated)
            + "}' >> tmp_file"
        )
    os.system(
        "grep 'Pullay' tmp_pullay | awk 'BEGIN {sig=0.} {sig+=$4} END {print sig/"
        + str(equilibrated)
        + "}' >> tmp_file"
    )
    os.system(
        "grep 'Pullay' tmp_pullay | awk 'BEGIN {sig=0.} {sig+=$9} END {print sig/"
        + str(equilibrated)
        + "}' >> tmp_file"
    )
    os.system("rm -f tmp_sig")

    with open("tmp_file") as f:
        f.readline()
        sig1 = float(f.readline())
        sig2 = float(f.readline())
        sig3 = float(f.readline())
        sig4 = float(f.readline())
        sig5 = float(f.readline())
        sig6 = float(f.readline())
        ext_p = float(f.readline())
        pullay_s = float(f.readline())

        print(
            " in kB   %8.3f   %8.3f  %8.3f   %8.3f   %8.3f   %8.3f"
            % (sig1, sig2, sig3, sig4, sig5, sig6)
        )
        print(
            "  external pressure =    %8.3f  " % ext_p
            + " kB  Pullay stress =   %8.2f  " % pullay_s
            + " kB"
        )
        print("  ")
        f.close()

    # os.system('rm -f tmp_file')


if __name__ == "__main__":
    fpte_ensemle_average_aimd(1500)
