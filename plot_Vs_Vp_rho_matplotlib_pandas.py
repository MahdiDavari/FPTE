import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def exponential_fit(x, a, b, c):
    return a*np.exp(-b*x) + c


# plt.style.use('seaborn-paper')

##
params = {
   'axes.labelsize':  12,
   'legend.fontsize': 10,
   'xtick.labelsize': 12,
   'ytick.labelsize': 12,
   'lines.linewidth' : 2.5,
   'lines.markersize' : 9,
   'boxplot.flierprops.linewidth': 2.0,
   'boxplot.boxprops.color': 'r',


   # 'boxplot.boxprops.linewidth': 9.0,
   'legend.loc': 'upper right',
   'text.usetex': False,
   # 'figure.figsize': [8, 6]
   }
plt.rcParams.update(params)

import matplotlib.gridspec as gridspec
gs1 = gridspec.GridSpec(3, 1)
gs1.update(wspace=0.01, hspace=0.01) # set the spacing between axes.



# pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier
# plt.rcParams['figure.figsize'] = (15, 5)

broken_df = pd.ExcelFile('/Users/MSG/Downloads/Fe_hcp/Fe-Si-S_Cij.xlsx')

df = broken_df.parse('Fe-S', na_values=['None'])



ax1 = plt.subplot(311)
######
x_min = min(df['Structure'])
x_max = max(df['Structure'])                               #min/max values for x axis
x_fit = np.linspace(x_min, x_max, 100)   #range of x values used for the fit function
# plt.plot(x, y, 'o', label='data')
# plt.axis([x_min, x_max, 6, 7])

df.plot('Structure', 'Vs', linestyle='', marker='*', markersize='9', label='', color='red')
fitting_parameters, covariance = curve_fit(exponential_fit, df['Structure'], df['Vs'],maxfev=2000)
a, b, c = fitting_parameters
plt.plot(x_fit, exponential_fit(x_fit, *fitting_parameters), color='red', linewidth=2.5, linestyle='-', label='Voigt')


df.plot('Structure', 'Vs_H', 'r+', linestyle='', marker='*', markersize='9',  color='red', label='')
fitting_parameters_VsH, covariance = curve_fit(exponential_fit, df['Structure'], df['Vs_H'],maxfev=2000)
a, b, c = fitting_parameters_VsH
plt.plot(x_fit, exponential_fit(x_fit, *fitting_parameters_VsH), linewidth=2.5, color='red', label='Voigt-Reuss-Hill', linestyle=':' )



plt.ylabel(r'V$_s$ (km s$^{-1}$)')
plt.xlabel('')

plt.setp(ax1.get_xticklabels(), visible=False)
plt.legend(fontsize='medium')
plt.grid(False)

ax2 = plt.subplot(312, sharex=ax1)
df.plot('Structure', 'Vp (km s-1)', linestyle='', marker='*', markersize='9',  color='blue', label='')
fitting_parameters_Vp, covariance = curve_fit(exponential_fit, df['Structure'], df['Vp (km s-1)'], maxfev=2000)
a, b, c = fitting_parameters_Vp
plt.plot(x_fit, exponential_fit(x_fit, *fitting_parameters_Vp), linewidth=2.5, color='blue', label='Voigt', linestyle='-' )



df.plot('Structure', 'Vp (km s-1)_H', linestyle='', marker='*', markersize='9',  color='blue', label='')
fitting_parameters_VpH, covariance = curve_fit(exponential_fit, df['Structure'], df['Vp (km s-1)_H'], maxfev=2000)
a, b, c = fitting_parameters_VpH
plt.plot(x_fit, exponential_fit(x_fit, *fitting_parameters_VpH), linewidth=2.5, color='blue', label='Voigt-Reuss-Hill', linestyle=':' )
# plt.ytick.major.width = 0.5


plt.ylabel(r'V$_p$ (km s$^{-1}$)')
plt.xlabel('')


plt.setp(ax2.get_xticklabels(), visible=False)
plt.legend(fontsize='medium')
plt.grid(False)

ax3 = plt.subplot(313, sharex=ax1)
df.plot('Structure', 'rho (Kg m-3)', color='black', marker='*', markersize='9', linewidth=2.5, linestyle='-', label='density')
plt.ylabel(r'$\rho$ (g m$^{-3}$)')


plt.xlabel(r'Fe$_{1-x}$S$_{x}$')
plt.grid(False)

# plt.show()
plt.savefig('/Users/MSG/Downloads/Fe_hcp/Fe-S_Oct.pdf')



