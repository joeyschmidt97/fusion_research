#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt
import numpy as np

from GENE_POST_simulation_data import simulation_sorter
from GENE_POST_omega_data import omega_to_sim_dict
from GENE_POST_param_data import parameter_to_sim_dict



def compare_str_for_plots(filepath, compare_str):
    directory_list = os.listdir(filepath)
    directory_list.sort()

    for directory_name in directory_list:
        # Skip files that start with "X_" 
        if directory_name.startswith('X_'):
            pass

        else:
            directory_path = os.path.join(filepath, directory_name)

            if os.path.isdir(directory_path):
                sort_simulation_list = simulation_sorter(filepath)
        
                for i in range(len(sort_simulation_list)-1):
                    sim_1_dict = sort_simulation_list[i]
                    parameter_to_sim_dict(sim_1_dict)
                    sim_2_dict = sort_simulation_list[i+1]
                    parameter_to_sim_dict(sim_2_dict)
                    # if parameter_list[i][compare_str] != parameter_list[i+1][compare_str]:
                    if sim_1_dict['parameters'][compare_str] != sim_2_dict['parameters'][compare_str]:
                        print('There is a mismatching value in', directory_path, 'for the comparison value:', compare_str)
                        break
                else:
                    compare_value = sim_2_dict['parameters'][compare_str]

    return compare_value



def compare_growth_rates(filepath_list, compare_str='nz0', plot_type = 'kymin'):
    import itertools

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    colors = itertools.cycle(['blue', 'red', 'green', 'orange', 'purple'])
    markers = itertools.cycle(['o', 's', '^', 'd', 'v'])

    for (filepath, color, marker) in zip(filepath_list, colors, markers):
        print('filepath:', filepath)
        
        compare_value = compare_str_for_plots(filepath, compare_str)
        label_str = f"{compare_str} = {compare_value}"
        
        growth_data_dict = collect_growth_rates(filepath)

        if plot_type == 'global':
            log_plot(growth_data_dict, 'n0_global', 'gamma (kHz)', ax1, color=color, linestyle='dotted', marker=marker, label = label_str)
            log_plot(growth_data_dict, 'n0_global', 'omega (kHz)', ax2, color=color, linestyle='dotted', marker=marker, label = label_str)
        elif plot_type == 'kymin':
            log_plot(growth_data_dict, 'kymin', 'gamma (cs/a)', ax1, color=color, linestyle='dotted', marker=marker, label = label_str)
            log_plot(growth_data_dict, 'kymin', 'omega (cs/a)', ax2, color=color, linestyle='dotted', marker=marker, label = label_str)

    ax1.legend(loc='best', fontsize=10)
    ax2.legend(loc='best', fontsize=10)
    fig.suptitle(f"Comparison of growth rates for {len(filepath_list)} files", fontsize=12)
    plt.tight_layout()
    plt.show()



def collect_growth_rates(filepath):
    keys = ['kymin', 'n0_global', 'omega (kHz)', 'gamma (kHz)', 'omega (cs/a)', 'gamma (cs/a)']
    growth_data_dict = {}

    for key in keys:
        growth_data_dict[key] = []
    

    sort_simulation_list = simulation_sorter(filepath)

    for simulation_dict in sort_simulation_list:
        parameter_to_sim_dict(simulation_dict)
        omega_to_sim_dict(simulation_dict)
        param_dict = simulation_dict['parameters']
        omega_dict = simulation_dict['omega']
        
        for key in keys:
            growth_data_dict[key].append(omega_dict[key])
        
    return growth_data_dict



def log_plot(plotting_dict, x_name, y_name, ax=None, label=None, **kwargs):
    x = np.array(plotting_dict[x_name])
    y = np.array(plotting_dict[y_name])

    # get the indices that would sort x in ascending order
    idx = np.argsort(x)

    # use the indices to rearrange both x and y
    x_sorted = x[idx]
    y_sorted = y[idx]

    # # print out values of x and y
    x_print = [float(i) for i in x_sorted]
    print('x:', x_print)
    # print('y:', y_sorted)
    
    ax = ax or plt.gca()
    ax.set_xscale('log')
    
    ax.set_xlabel(x_name, fontsize=15)
    ax.set_ylabel(y_name, fontsize=15)
    
    return ax.plot(x_sorted, y_sorted, label=label, **kwargs)



def plot_growth_rates(filepath, plot_type = 'kymin'):
    growth_data_dict = collect_growth_rates(filepath)

    print('filepath:', filepath)

    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10, 4))
    if plot_type == 'global':
        log_plot(growth_data_dict, 'n0_global', 'gamma (kHz)', ax1, color='blue', linestyle = 'dotted', marker = 'o')
        log_plot(growth_data_dict, 'n0_global', 'omega (kHz)', ax2, color='red', linestyle = 'dotted', marker = 'o')
    elif plot_type == 'kymin':
        log_plot(growth_data_dict, 'kymin', 'gamma (cs/a)', ax1, color='blue', linestyle = 'dotted', marker = 'o')
        log_plot(growth_data_dict, 'kymin', 'omega (cs/a)', ax2, color='red', linestyle = 'dotted', marker = 'o')
    
    fig.suptitle(filepath, fontsize=12)
    plt.tight_layout()
    plt.show()


if __name__=="__main__":
    filepath = os.getcwd()
    plot_growth_rates(filepath)