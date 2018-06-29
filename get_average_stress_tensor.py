#!/usr/bin/python

import os
import sys


if (os.path.exists('OSZICAR') == False or os.path.exists('OUTCAR') == False):
    sys.exit('\n.... Oops ERROR: There is NO OUTCAR or OSZICAR file !?!?!?    \n')

os.system('rm -f tmp_file')
os.system("grep T= OSZICAR  | awk 'BEGIN {T=0.} {T+=$3} END {print T , $1}'  >   tmp_file  ")

with open('tmp_file') as f:
    T, tot = f.readline().split()
    T = int(T)
    tot = int(tot)
    f.close()

num_discard = input(
    '\n >>>> How many initial ionic steps need to be discarded in order to reach equilibration? \ '
    '\n >>>> (it is recommended to discard 1 ps at least - the default is 1000 steps): ')
if (int(num_discard) > tot or int(num_discard) < 0):
    sys.exit("\n.... Oops ERROR - your discarded part is higher than the total ionic steps:  \n")
if num_discard == '':
    num_discard = 1000

equilibrated = tot - num_discard

os.system("grep 'in kB' OUTCAR | tail -"+str(equilibrated)+"  > tmp_sig")

for i in range(6):
    os.system("grep 'in kB' tmp_sig | awk 'BEGIN {sig=0.} {sig+=$"+str(i+3)+"} END {print sig/"+str(equilibrated)+"}' >> tmp_file")
os.system('rm -f tmp_sig')


with open('tmp_file') as f:
    f.readline()
    sig1 = float(f.readline())
    sig2 = float(f.readline())
    sig3 = float(f.readline())
    sig4 = float(f.readline())
    sig5 = float(f.readline())
    sig6 = float(f.readline())

    print('SigXX', '%10.3f' % sig1)
    print('SigYY', '%10.3f' % sig2)
    print('SigZZ', '%10.3f' % sig3)
    print('SigXY', '%10.3f' % sig4)
    print('SigYZ', '%10.3f' % sig5)
    print('SigZX', '%10.3f' % sig6)
    f.close()

os.system('rm -f tmp_file')
