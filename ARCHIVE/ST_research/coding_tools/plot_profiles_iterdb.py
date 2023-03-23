#INPUT: python filepath/of/plot_profiles_iterdb.py iterdb_filename.iterdb profiles_e.dat profiles_i.dat

import numpy as np
import matplotlib.pyplot as plt
import sys

from make_profiles_iterdb import create_profiles, auto_create_profiles


#Call this function when you want to plot multiple discharges on the same plots for comparison
#INPUT: multi_profile_dict = {'DISCHARGE#1': {'filename_path': f1, 'gene_e_path': ge1, 'gene_i_path': gi1}, 
# 'DISCHARGE#2': {'filename_path': f2, 'gene_e_path': ge2, 'gene_i_path': gi2}, ... }
def multi_plot_profiles(discharge_path_dict: dict, x_start: float = 0, gene_plotting: bool = False, plot_impurity: bool = False):
    
    discharges = list(discharge_path_dict.keys())

    for discharge in discharges:
        path = discharge_path_dict[discharge]['filepath']
        profile_dict, g_plot_dict = auto_create_profiles(path)

        discharge_path_dict[discharge]['profile_dict'] = profile_dict
        discharge_path_dict[discharge]['g_plot_dict'] = g_plot_dict

    quantities = list(profile_dict.keys())
    
    for quantity in quantities:
        for discharge in discharges:
            profile_dict = discharge_path_dict[discharge]['profile_dict']

            rhot = profile_dict[quantity]['rhot']
            arr = profile_dict[quantity]['arr']
            units = profile_dict[quantity]['units']

            if x_start != 0:
                arr = arr[rhot > x_start]
                rhot = rhot[rhot > x_start]

            plt.plot(rhot, arr, label=quantity+'('+units+')' + ' - ' + discharge)
            
            plt.xlabel(r'$\rho_{tor}$',size=18)
            if x_start != 0: plt.xlim(x_start)
            plt.legend(loc='lower left')

        plt.show()
    # return multi_profile_dict



#Plotting function (called in main script)
def plot_profiles(profile_dict: dict, g_plots: dict, x_start: float = 0, gene_plotting: bool = False, plot_impurity: bool = False):
    quantities = list(profile_dict.keys())

    for quantity in quantities:
        units = profile_dict[quantity]['units']
        arr = profile_dict[quantity]['arr']
        rhot = profile_dict[quantity]['rhot']
        gprof_i = g_plots['gprof_i']
        gprof_e = g_plots['gprof_e']
        gprof_imp = g_plots['gprof_imp']

        #if a start x-value > 0 then cut off the data where rhot (x-values) exceed the x start point
        if x_start != 0:
            arr = arr[rhot > x_start]
            rhot = rhot[rhot > x_start]

        plt.plot(rhot,arr,label=quantity+'('+units+')')
        plt.xlabel(r'$\rho_{tor}$',size=18)
        plt.legend(loc='lower left')
        if x_start != 0: plt.xlim(x_start)
        plt.show()
        
        if gene_plotting and quantity=='TI':
            plt.plot(rhot,arr/1000.0,label=quantity+'('+units+')')
            plt.plot(gprof_i[:,0],gprof_i[:,2],'r.',label='$T_i$ gene')
            plt.legend(loc='lower left')
            if x_start != 0: plt.xlim(x_start)
        if gene_plotting and quantity=='NM1':
            plt.plot(rhot,arr/1.0e19,label=quantity+'('+units+')/1.0e19')
            plt.plot(gprof_i[:,0],gprof_i[:,3],'r.',label='$n_i$ gene')
            plt.legend(loc='lower left')
            if x_start != 0: plt.xlim(x_start)
        if gene_plotting and quantity=='NM2' and plot_impurity:
            plt.plot(rhot,arr/1.0e19,label=quantity+'('+units+')/1.0e19')
            plt.plot(gprof_imp[:,0],gprof_imp[:,3],'r.',label='$n_i$ gene')
            plt.legend(loc='lower left')
            if x_start != 0: plt.xlim(x_start)
        if gene_plotting and quantity=='TE':
            plt.plot(rhot,arr/1000.0,label=quantity+'('+units+')')
            plt.plot(gprof_e[:,0],gprof_e[:,2],'r.',label='$T_e$ gene')
            plt.legend(loc='lower left')
            if x_start != 0: plt.xlim(x_start)
        if gene_plotting and quantity=='NE':
            plt.plot(rhot,arr/1.0e19,label=quantity+'('+units+')/1.0e19')
            plt.plot(gprof_e[:,0],gprof_e[:,3],'r.',label='$n_e$ gene')
            plt.legend(loc='lower left')
            if x_start != 0: plt.xlim(x_start)
        plt.show()



#Only allow user input for filename and e/i profiles if the script is executed in terminal (name == "__main___")
if __name__ == "__main__":
    filename = sys.argv[1]
    gene_e = sys.argv[2]
    gene_i = sys.argv[3]

    print(filename)
    print(gene_e)
    print(gene_i)
    
    #If you want to compare with gene profile files:
    gene_plotting = True    #set to 0 for no gene plots
    plot_impurity = False

    profile_dict, g_plots = create_profiles(filename, gene_e, gene_i, gene_plotting, plot_impurity)
    plot_profiles(profile_dict, g_plots, gene_plotting, plot_impurity, 0)












