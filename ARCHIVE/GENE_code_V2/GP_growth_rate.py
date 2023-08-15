#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt
import numpy as np

from GP_simulation_data import simulation_sorter
from GP_omega_data import omega_to_sim_dict
from fusion_research.GENE_code_V2.GP_parameter_data import parameter_to_sim_dict



def sort_and_reorder_dict(data_dict, sort_key):
    # Get the values associated with the 'kymin' key
    x = data_dict[sort_key]

    # Get the indices that would sort x in ascending order
    idx = np.argsort(x)

    # Create a new dictionary with sorted and reordered keys
    sorted_dict = {}
    for k, v in data_dict.items():
        sorted_dict[k] = [v[i] for i in idx]

    return sorted_dict


def collect_growth_rates(filepath_list, label_key = 'nz0'):
    keys = ['kymin', 'n0_global', 'omega (kHz)', 'gamma (kHz)', 'omega (cs/a)', 'gamma (cs/a)']
    growth_data_list = []
    
    if isinstance(filepath_list, str):
        filepath_list = [filepath_list]
    if isinstance(filepath_list, list):
        pass

    for filepath in filepath_list:
        if os.path.exists(filepath):
            pass
        else:
            print(filepath, 'is not a valid filepath. Please give a valid filepath.')
        
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
            
        sorted_dict = sort_and_reorder_dict(growth_data_dict,sort_key = 'kymin')    
        sorted_dict['filepath'] = filepath
        sorted_dict['label'] = f"{label_key} = {param_dict[label_key]}"
        
        growth_data_list.append(sorted_dict)
            
    return growth_data_list



def percent_difference(ref_x_list, ref_y_list, x_list, y_list):
    
    combined_x_list = list(set(ref_x_list).union(set(x_list)))
    combined_x_list.sort()
    
    diff_list = []
    x_vals = []
    
    for x in combined_x_list:
        if np.isin(x, ref_x_list) and np.isin(x, x_list):
            ref_x_index = np.where(ref_x_list == x)[0][0]
            x_index = np.where(x_list == x)[0][0]

            y_ref = ref_y_list[ref_x_index]
            y_value = y_list[x_index]
            
        elif np.isin(x, ref_x_list):
            ref_x_index = np.where(ref_x_list == x)[0][0]
            y_ref = ref_y_list[ref_x_index]
            
            #interpolate y_value
            y_value = np.interp(x, x_list, y_list)
            
        elif np.isin(x, x_list):
            x_index = np.where(x_list == x)[0][0]
            y_value = y_list[x_index]
            
            #interpolate y_ref
            y_ref = np.interp(x, ref_x_list, ref_y_list)
        
        if y_ref == 0:
            pass
        else:
            diff = y_ref - y_value
            perc_diff = diff/y_ref
            diff_list.append(perc_diff)
            x_vals.append(x)

    return x_vals, diff_list


#################################
# PLOTTING FUNCTIONS
#################################

def log_plotting(fig, ax, plot_dict_list, x_name, y_name, verbose):
    ref_x = np.array(plot_dict_list[0][x_name])
    ref_y = np.array(plot_dict_list[0][y_name])

    colors = ['blue', 'red', 'green', 'orange', 'purple']  # Default list of colors
    markers = ['o', 'd', 's', '>', '^']
    
    for i, plot_dict in enumerate(plot_dict_list):
        x = np.array(plot_dict[x_name])
        y = np.array(plot_dict[y_name])
        color = colors[i % len(colors)]  # Cycles through colors
        marker = markers[i % len(markers)]

        ax.set_xscale('log')
        ax.set_xlabel(x_name, fontsize=15)
        ax.set_ylabel(y_name, fontsize=15)
        ax.plot(x, y, label=plot_dict['label'], color=color, marker=marker, markersize=8, linestyle='dotted')
        ax.legend()
    
        if verbose:
            print('x-values for filepath:', plot_dict['filepath'])
            x_decimal_list = [float(f"{value:.1f}") for value in x]
            print(x_decimal_list)


            if i==0:
                for i, (x_val, y_val) in enumerate(zip(x, y)):
                    # print(i)
                    label = f"{x_val:.1f}"  # Format the label with two decimal places
                    ax.annotate(label, xy=(x_val, y_val), xytext=(-5, 10), textcoords='offset points')
    print('\n')

    return fig



# def diff_plotting(fig, ax_diff, plot_dict_list, x_name, y_name, verbose):
#     ref_x = np.array(plot_dict_list[0][x_name])
#     ref_y = np.array(plot_dict_list[0][y_name])

#     colors = ['blue', 'red', 'green', 'orange', 'purple']  # Default list of colors
#     markers = ['o', 'd', '*', '>', '^']
    
#     for i, plot_dict in enumerate(plot_dict_list):
#         x = np.array(plot_dict[x_name])
#         y = np.array(plot_dict[y_name])
#         color = colors[i % len(colors)]  # Cycles through colors
#         marker = markers[i % len(markers)]

#         x_vals, perc_diff = percent_difference(ref_x, ref_y, x, y)

#         ax_diff.set_xscale('log')
#         ax_diff.set_ylabel('% Diff', fontsize=15)
#         if i > 0:
#             ax_diff.plot(x_vals, perc_diff, color=color, linestyle='dotted', marker=marker)

#             if verbose:
#                 for i, (x_val, y_val) in enumerate(zip(x_vals, perc_diff)):
#                     label = f"{x_val:.1f}"  # Format the label with two decimal places
#                     ax_diff.annotate(label, xy=(x_val, y_val), xytext=(-5, 10), textcoords='offset points')
    
#     return fig


def diff_plotting(fig, ax_diff, plot_dict_list, x_name, y_name, verbose):
    ref_x = np.array(plot_dict_list[0][x_name])
    ref_y = np.array(plot_dict_list[0][y_name])

    colors = ['blue', 'red', 'green', 'orange', 'purple']  # Default list of colors
    markers = ['o', 'd', '*', '>', '^']
    
    for i, plot_dict in enumerate(plot_dict_list):
        x = np.array(plot_dict[x_name])
        y = np.array(plot_dict[y_name])
        color = colors[i % len(colors)]  # Cycles through colors
        marker = markers[i % len(markers)]

        print(ref_x, x)

        x_combined = np.concatenate((ref_x, x))
        x_combined = np.unique(x_combined)
        x_combined = np.sort(x_combined)
        
        MOD_ref_y = interpolate_points(x_combined, ref_x, ref_y)
        MOD_y = interpolate_points(x_combined, x, y)


        percent_diff_values = []
        for val_ref, val in zip(MOD_ref_y, MOD_y):
            
            # low_bound = 1
            
            percent_diff = 100*abs(val_ref - val)/ abs(val_ref)

            # if (val_ref < 0) or (val < 0):
            #     percent_diff = 100*(val_ref - val / abs(val_ref))
            
            # else:
            #     percent_diff = 100*abs(val_ref - val) / ((val_ref + val)/2)
            
            percent_diff_values.append(percent_diff)

        
        ax_diff.set_xscale('log')
        ax_diff.set_ylabel('% Diff', fontsize=15)
        if i > 0:
            ax_diff.plot(x_combined, percent_diff_values, color=color, linestyle='dotted', marker=marker)

            if verbose:
                for i, (x_val, y_val) in enumerate(zip(x_combined, percent_diff_values)):
                    label = f"{x_val:.1f}"  # Format the label with two decimal places
                    ax_diff.annotate(label, xy=(x_val, y_val), xytext=(-5, 10), textcoords='offset points')
    
    return fig





def interpolate_points(X_MERGE, x_list, y_list):
    Y_MERGE = []

    for X in X_MERGE:
        closest_x_i = np.argmin(np.abs(x_list - X))
        closest_x = x_list[closest_x_i]
        delta_x = X - closest_x
        
        in_between = True
        
        if (X == closest_x):
            in_between = False
            Y_int = y_list[closest_x_i]
        
        elif (X < x_list[0]):
            in_between = False
            x_back = x_list[0]
            y_back = y_list[0]
            x_front = x_list[1]
            y_front = y_list[1]
            
            m = (y_front - y_back) / (x_front - x_back)
            Y_int = m * delta_x + y_back
            
        elif (X > x_list[-1]):
            in_between = False
            x_back = x_list[-2]
            y_back = y_list[-2]
            x_front = x_list[-1]
            y_front = y_list[-1]
            
            m = (y_front - y_back) / (x_front - x_back)
            Y_int = m * delta_x + y_front
            
        elif (delta_x < 0) and in_between:       
            x_back = x_list[closest_x_i - 1]
            y_back = y_list[closest_x_i - 1]
            x_front = x_list[closest_x_i]
            y_front = y_list[closest_x_i]
            
            m = (y_front - y_back) / (x_front - x_back)
            Y_int = m * delta_x + y_front
            
        elif (delta_x > 0) and in_between:
            x_back = x_list[closest_x_i]
            y_back = y_list[closest_x_i]
            x_front = x_list[closest_x_i + 1]
            y_front = y_list[closest_x_i + 1]
            
            m = (y_front - y_back) / (x_front - x_back)
            Y_int = m * delta_x + y_back
        
        Y_MERGE.append(Y_int)
    
    return np.array(Y_MERGE)






#################################
# SINGLE AND DOUBLE PLOTS
#################################

def single_plot(filepath_list, plot_mode='kymin', label_key='nz0', plot_type = 'gamma', verbose = False):
    if isinstance(filepath_list, str): filepath_list = [filepath_list]
    if plot_mode == 'global':
        x_name= 'n0_global'
        y_name=f"{plot_type} (kHz)"
    elif plot_mode == 'kymin':
        x_name= 'kymin'
        y_name=f"{plot_type} (cs/a)"
          
    plot_dict_list = collect_growth_rates(filepath_list, label_key)

    if len(filepath_list) == 1:
        fig, ax = plt.subplots(figsize=(5, 4))
    elif len(filepath_list) > 1:
        fig, (ax, ax_diff) = plt.subplots(nrows=2, gridspec_kw={'height_ratios': [2, 1]}, figsize=(5, 6))

    log_plotting(fig, ax, plot_dict_list, x_name, y_name, verbose = verbose)
    
    if len(filepath_list) > 1:
        diff_plotting(fig, ax_diff, plot_dict_list, x_name, y_name, verbose = verbose)

    plt.tight_layout()
    plt.show()



def gamma_omega_plot(filepath_list, plot_mode='kymin', label_key='nz0', verbose = False):
    if isinstance(filepath_list, str): filepath_list = [filepath_list]
    if plot_mode == 'global':
        x_name = 'n0_global'
        y_gamma_name = f"gamma (kHz)"
        y_omega_name = f"omega (kHz)"
    elif plot_mode == 'kymin':
        x_name = 'kymin'
        y_gamma_name = f"gamma (cs/a)"
        y_omega_name = f"omega (cs/a)"
    
    plot_dict_list = collect_growth_rates(filepath_list, label_key)
    
    if len(filepath_list) == 1:
        fig, (gamma_ax, omega_ax) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
    elif len(filepath_list) > 1:
        fig, ((gamma_ax, omega_ax), (gamma_diff, omega_diff)) = plt.subplots(nrows=2, ncols=2, 
                                                                             gridspec_kw={'height_ratios': [2, 1]}, 
                                                                             figsize=(10, 6))
    
    log_plotting(fig, gamma_ax, plot_dict_list, x_name, y_gamma_name, verbose = verbose)
    log_plotting(fig, omega_ax, plot_dict_list, x_name, y_omega_name, verbose = verbose)
    
    if len(filepath_list) > 1:
        diff_plotting(fig, gamma_diff, plot_dict_list, x_name, y_gamma_name, verbose = verbose)
        diff_plotting(fig, omega_diff, plot_dict_list, x_name, y_omega_name, verbose = verbose)

    plt.tight_layout()
    plt.show()

