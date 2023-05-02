#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from GENE_POST_all_sim_data import simulations_to_list
# from GENE_POST_omega_data import omega_to_Hz
from GENE_POST_param_data import parameters_to_list



def print_data_points(filepath):
    beta_directories = os.listdir(filepath)

    for beta_name in beta_directories:
        beta_dir = os.path.join(filepath, beta_name)

        print(beta_dir)
        simulation_list = simulations_to_list(beta_dir)
        # print(len(simulation_list))
        for simulation_dict in simulation_list:
            param_dict = simulation_dict['parameter_file']
            omega_dict = simulation_dict['omega_file']

            parameter_directory = param_dict['filepath']
            suffix = param_dict['suffix']

            print('beta:', param_dict['beta'])
            print('elec density grad (omn2):',param_dict['omn2'])
        print('')


def get_data_points(filepath):
    beta_list = []
    density_list = []
    KBM_limit_list = []

    beta_directories = os.listdir(filepath)

    for beta_name in beta_directories:
        beta_dir = os.path.join(filepath, beta_name)

        print(beta_dir)
        simulation_list = simulations_to_list(beta_dir)
        # print(len(simulation_list))
        for simulation_dict in simulation_list:
            param_dict = simulation_dict['parameter_file']
            omega_dict = simulation_dict['omega_file']

            parameter_directory = param_dict['filepath']
            suffix = param_dict['suffix']
            diff_abs_value = get_diff_abs_value(parameter_directory, suffix)

            KBM_limit_list.append(diff_abs_value)
            beta_list.append(param_dict['beta'])
            density_list.append(param_dict['omn2'])

            # print(param_dict['filename'] ,param_dict['kymin'], omega_dict['filename'], param_dict['kymin'], diff_abs_value)
        print('')

    return beta_list, density_list, KBM_limit_list


def get_diff_abs_value(filepath, suffix):
    import subprocess
    os.chdir(filepath)

    # Get the full path to the script
    script_path = os.path.abspath('/global/homes/j/joeschm/ifs_scripts/plot_mode_structures.py')
    result = subprocess.run(['python', script_path, suffix, '-e'], stdout=subprocess.PIPE)  # Run the script with the specified arguments

    # Get the stdout as a string
    output = result.stdout.decode('utf-8')

    # Find the line that contains the "diff/abs" value
    diff_abs_line = [line for line in output.split('\n') if 'diff/abs' in line][0]
    diff_abs_value = float(diff_abs_line.split()[-1])   # Extract the numerical value from the line

    return diff_abs_value

   


def ref_values(filepath):
    discharge_directory = os.path.dirname(filepath)
    ref_directory = os.path.join(discharge_directory, 'kymin_scan')
    scanfile_list = os.listdir(ref_directory)

    for scanfile in scanfile_list:
            scanfile_dir = os.path.join(ref_directory, scanfile)

            simulation_list = simulations_to_list(scanfile_dir)
            for simulation_dict in simulation_list:
                param_dict = simulation_dict['parameter_file']
                
                if param_dict['kymin'] == 0.1:
                    ref_beta = param_dict['beta']
                    ref_elec_dens = param_dict['omn2']
                    break

    return ref_beta, ref_elec_dens
            


def KBM_color_plot(filepath, color_bar = 'local', show_z_vals = False):
    beta_list, density_list, KBM_limit_list = get_data_points(filepath)


    beta_den_dict = {}
    for i in range(len(KBM_limit_list)):
        KBL_limit = KBM_limit_list[i]
        beta_den_dict[(beta_list[i], density_list[i])] = KBL_limit  # Replace 'i' with your desired z value calculation
    # Sort the dictionary by the keys (x, y) in ascending order
    beta_den_dict = dict(sorted(beta_den_dict.items()))


    # Set up the plot
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    ref_beta, ref_elec_dens = ref_values(filepath)


    if (ref_beta, ref_elec_dens) in beta_den_dict:
        # Retrieve the z value for a given (x, y) tuple
        ref_diff_abs = beta_den_dict[(ref_beta, ref_elec_dens)]    
    else:
        print(f"ref_beta {ref_beta} is not found in beta_list.")


    


    if color_bar == 'absolute':
        KBM_lower_limit = 0.2
    elif color_bar == 'local':
        KBM_lower_limit = np.min(KBM_limit_list)
    

    KBM_upper_limit = np.max(KBM_limit_list)
    if KBM_upper_limit < ref_diff_abs:
        KBM_upper_limit = ref_diff_abs

    # Plot the points with z used to color them on a scale
    scatter = ax.scatter(beta_list, density_list, c=KBM_limit_list, cmap='RdBu', s=100, vmin=KBM_lower_limit, vmax=KBM_upper_limit, edgecolor='black')
    cbar = plt.colorbar(scatter, pad=0.15)    # Add a color bar


    if show_z_vals:
        for x, y, z in zip(beta_list, density_list, KBM_limit_list):
            # print(KBM_limit_list, '// z:', z)
            label = f"{z:.5f}"  # Format the label with two decimal places
            ax.annotate(label, xy=(x, y), xytext=(-5, 10), textcoords='offset points')

    # Add reference point to plot
    ax.scatter(ref_beta, ref_elec_dens, c=ref_diff_abs, cmap='RdBu', marker='*', s=600, vmin=KBM_lower_limit, vmax=KBM_upper_limit, edgecolor='black')


    # Add percentage scales
    ax2 = ax.secondary_xaxis('top', functions=(lambda x: ((x - ref_beta) / ref_beta) * 100, lambda x: x))
    ax3 = ax.secondary_yaxis('right', functions=(lambda y: ((y - ref_elec_dens) / ref_elec_dens) * 100, lambda y: y))
    ax2.set_xlabel('Beta deviation (%)')
    ax3.set_ylabel('Elec density gradient deviation (%)')

    # Set the labels and title
    ax.set_xlabel('beta')
    ax.set_ylabel('a/Ln (elec gradient)')
    ax.set_title('KBM Limit Test')

    plt.show()



def beta_scan(filepath):
    beta_list_unsorted, density_list, KBM_limit_list_unsorted = get_data_points(filepath)

    # create a list of indices that would sort beta_list_unsorted
    idx = sorted(range(len(beta_list_unsorted)), key=lambda i: beta_list_unsorted[i])

    # sort beta_list and KBM_limit_list using the sorted indices
    beta_list = [beta_list_unsorted[i] for i in idx]
    KBM_limit_list = [KBM_limit_list_unsorted[i] for i in idx]

    # Set up the plot
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    ref_beta, ref_elec_dens = ref_values(filepath)

    if ref_beta in beta_list:
        ref_index = beta_list.index(ref_beta)
        ref_diff_abs = KBM_limit_list[ref_index]
        # print(f"KBM value at ref_beta {ref_beta} is {ref_diff_abs}.")
    else:
        print(f"ref_beta {ref_beta} is not found in beta_list.")


    # Plot the points with z used to color them on a scale
    ax.plot(beta_list, KBM_limit_list, linestyle = 'dotted', marker = 'o')
    
    # Add reference point to plot
    ax.plot(ref_beta, ref_diff_abs, linestyle = 'dotted', marker = '*', markersize=15, color='blue')
    #ax.scatter(ref_beta, ref_elec_dens, c=ref_diff_abs, cmap='RdBu', marker='*', s=200, vmin=KBM_lower_limit, vmax=KBM_upper_limit)

    # Add percentage scales
    ax2 = ax.secondary_xaxis('top', functions=(lambda x: ((x - ref_beta) / ref_beta) * 100, lambda x: x))
    ax2.set_xlabel('Beta deviation (%)')
    
    # Set the labels and title
    ax.set_xlabel('beta')
    ax.set_ylabel('diff/abs')
    ax.set_title('Beta scan')

    plt.show()



if __name__=="__main__":
    filepath = os.getcwd()
    suffix = '0002'
    # get_diff_abs_value(filepath, suffix)

    KBM_color_plot(filepath)