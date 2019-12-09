#!/usr/bin/env python

import os

def fpte_clean():
    inp = input('>>>> All result files/folders will be deleted, are you sure??')
    if inp:
        os.system('rm -rf ./Deform0* ./Distorted_Parameters ./INFO_FPTE')


if __name__ == "__main__":
    fpte_clean()