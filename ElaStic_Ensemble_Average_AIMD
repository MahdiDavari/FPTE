#!/usr/local/bin/python3.3

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

equilibrated = tot - int(num_discard)

os.system("grep -A 1 'in kB' OUTCAR | tail -"+str(3*equilibrated)+"  > tmp_sig")

for i in range(6):
    os.system("grep 'in kB' tmp_sig | awk 'BEGIN {sig=0.} {sig+=$"+str(i+3)+"} END {print sig/"+str(equilibrated)+"}' >> tmp_file")
os.system("grep 'Pullay' tmp_sig | awk 'BEGIN {sig=0.} {sig+=$4} END {print sig/"+str(equilibrated)+"}' >> tmp_file")
os.system("grep 'Pullay' tmp_sig | awk 'BEGIN {sig=0.} {sig+=$9} END {print sig/"+str(equilibrated)+"}' >> tmp_file")
os.system('rm -f tmp_sig')


with open('tmp_file') as f:
    f.readline()
    sig1 = float(f.readline())
    sig2 = float(f.readline())
    sig3 = float(f.readline())
    sig4 = float(f.readline())
    sig5 = float(f.readline())
    sig6 = float(f.readline())
    ext_p= float(f.readline())
    pullay_s= float(f.readline())


#    print('SigXX %10.3f' % sig1)
#    print('SigYY %10.3f' % sig2)
#    print('SigZZ %10.3f' % sig3)
#    print('SigXY %10.3f' % sig4)
#    print('SigYZ %10.3f' % sig5)
#    print('SigZX %10.3f' % sig6)
#    print('external pressure %10.3f' %ext_p)
#    print('Pullay Stress %10.3f' %pullay_s)
    print(' in kB    ', str(sig1), str(sig2), str(sig3), str(sig4), str(sig5), str(sig6), sep="    ")
    print('  external pressure =      ', ext_p,' kB  Pullay stress =     ', pullay_s, ' kB')
    print('  ')
    f.close()

os.system('rm -f tmp_file')
