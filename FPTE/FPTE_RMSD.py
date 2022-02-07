#!/usr/bin/env python
import sys, os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def fpte_rmsd():
 
    if (not os.path.exists('CONTCAR')) or (not os.path.exists('OUTCAR')) or (not os.path.exists('OSZICAR')):
        sys.exit('\n.... Oops ERROR: There is NO CONTCAR, OUTCAR or OSZICAR file !?!?!?    \n')

    os.system('grep -B 1 Direct CONTCAR > tmp')
    with open('tmp', 'r') as f:
        a = f.readline().strip().split()
        total_atoms = sum(list(map(int, a)))


    #os.system("grep T= OSZICAR  | tail -1 | cut -d' ' -f1 > tmp")
    os.system("grep T= OSZICAR  | tail -1  > tmp")
    with open('tmp', 'r')as f:
        total_steps = int(f.readline().strip().split()[0])


    os.system("sed -n '/POSITION/,/total drift:/{//!p;}' OUTCAR | grep -v '\-\-\-\-' > tmp")
    df = pd.read_csv('tmp', delim_whitespace=True, header=None, usecols=[0,1,2], dtype=np.float32)

    rmsd_list = []
    for i in range(total_steps):
        df_RMSD = []
        df_RMSD = df.iloc[0:total_atoms] - df.iloc[(total_atoms)*i:(total_atoms*(i+1))].reset_index(drop=True)


        df_RMSD[0] = df_RMSD[0].apply(lambda x: abs(x)-6.98279 if abs(x) > 5.0 else x)
        df_RMSD[1] = df_RMSD[1].apply(lambda x: abs(x)-6.93810 if abs(x) > 5.0 else x)
        df_RMSD[2] = df_RMSD[2].apply(lambda x: abs(x)-9.19443 if abs(x) > 7.3 else x)

        newwww = np.power(df_RMSD,2)
        rmsd_list.append(np.sqrt(sum(newwww.apply(np.sum))/total_atoms))

    os.system('rm ./tmp')
    print('The Maximum RMSD is: {:2.2}'.format(max(rmsd_list)))
    print('The Minimum RMSD is: {:2.2}'.format(min(rmsd_list)))
    print('Total number of Structures {:1}'.format(len(rmsd_list)))
    print('Total number of atoms {:1}'.format(total_atoms))
    plt.plot(rmsd_list)
    plt.savefig('RMSD.pdf', format='pdf', dpi=600)
    plt.show()
    
if __name__ == '__main__':
    fpte_rmsd()