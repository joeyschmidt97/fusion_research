#!/usr/bin/env python3
import json
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from MTM_data import extract_data_points, dist_3D_from_reference_point
sys.path.insert(1, '/global/u1/j/joeschm/fusion_research/GENE_code_V3')
from GP_simulation_data_V3 import filepath_to_simulation_dict_list
from GP_file_functions_V3 import rescale_list

#------------------------------------------------------------------------------------------------
# Function to plot MTM plots in 3D---------------------------------------------------------------
#------------------------------------------------------------------------------------------------

def MTM_plots(filepath, criteria_list:list = [], plot_type:str = '3D', debug:bool = False, cutoff_value=None, write_data:bool=False):

    os.chdir(filepath)
    MTM_data_filename = 'MTM_kymin_dict_data_CUTOFF_VAL_' + str(cutoff_value)
    MTM_file_exists = os.path.exists(MTM_data_filename)

    if (not MTM_file_exists) or write_data:
        print('Writing data to:', os.getcwd(), '\n')
        simulation_dict_list = filepath_to_simulation_dict_list(filepath, criteria_list, load_files='nrg')
        all_kymin_data_points_dict = extract_data_points(simulation_dict_list, species='e', cutoff_value=cutoff_value)

        os.chdir(filepath)
        write_MTM_dict_data(all_kymin_data_points_dict, MTM_data_filename)

    elif MTM_file_exists:
        print('Reading data from:', os.getcwd(), '\n')
        all_kymin_data_points_dict = read_MTM_dict_data(MTM_data_filename)
        
    if plot_type == '3D':
        MTM_3D_plots(all_kymin_data_points_dict, cutoff_value=cutoff_value, debug=debug)
    elif plot_type == '3D kymin':
        MTM_3D_kymin_plots(all_kymin_data_points_dict, cutoff_value=cutoff_value, debug=debug)
    else:
        print('Please specify "plot_type" as either "3D" or "3D kymin" for plotting.')

    return


#------------------------------------------------------------------------------------------------
# Functions to create dict and load dict data ---------------------------------------------------
#------------------------------------------------------------------------------------------------


def write_MTM_dict_data(save_dict, filename):    
    with open(filename, 'w') as f:
        json.dump(save_dict, f)


def read_MTM_dict_data(filename):

    def to_float(value):
        try:
            return float(value)
        except ValueError:
            return value

    def deep_float_convert(d):
        new_dict = {}
        for key, value in d.items():
            new_key = to_float(key)
            if isinstance(value, dict):
                new_dict[new_key] = deep_float_convert(value)
            elif isinstance(value, list):
                new_dict[new_key] = [to_float(item) for item in value]
            else:
                new_dict[new_key] = to_float(value)
        return new_dict

    with open(filename, 'r') as f:  
        all_kymin_data_points_dict = deep_float_convert(json.load(f))
        return all_kymin_data_points_dict



#------------------------------------------------------------------------------------------------
# Functions to plot 3D cube of sensitivity analysis for MTM detection----------------------------
#------------------------------------------------------------------------------------------------

def MTM_3D_plots(all_kymin_data_points_dict: dict, cutoff_value = None, debug: bool = False):
    """
    Creates two 3D scatter plots side by side for each key in the input dictionary.
    - The left plot displays the actual values of 'coll', 'beta', and 'omt'.
    - The right plot displays the percent differences from a reference point.

    Parameters:
    - kymin_data_points_dict (dict): A dictionary with kymin values as keys. Each key has a dictionary
                                    value containing lists of 'coll', 'beta', 'omt', 'Q_EM/Q_ES', and
                                    a 'reference_point' which is itself a dictionary with 'coll', 'beta',
                                    and 'omt' values.
    - debug (bool): If True, prints the kymin value for which the plot is generated.

    Returns:
    - None, but displays the 3D scatter plots.
    """
    
    kymin_list = all_kymin_data_points_dict.keys()
    
    for kymin in kymin_list:
        data_point_dict = all_kymin_data_points_dict[kymin]
        
        # Extracting data points from the dictionary
        coll_list = data_point_dict['coll']
        beta_list = data_point_dict['beta']
        omt_list = data_point_dict['omt']
        ratio_Q_EM_Q_ES = data_point_dict['Q_EM/Q_ES']
        reference_point = data_point_dict['reference_point']
        
        # Scaling marker sizes based on the ratio of Q_EM/Q_ES values
        max_marker_size = 600
        min_marker_size = 80

        resized_Q_ratio_list = rescale_list(ratio_Q_EM_Q_ES, max_marker_size, min_marker_size)
        
        # Extracting reference point values
        ref_coll, ref_beta, ref_omt = reference_point['coll'], reference_point['beta'], reference_point['omt']
        
        # Calculating percent differences from the reference point
        coll_diff = [((val - ref_coll) / ref_coll) * 100 for val in coll_list]
        beta_diff = [((val - ref_beta) / ref_beta) * 100 for val in beta_list]
        omt_diff = [((val - ref_omt) / ref_omt) * 100 for val in omt_list]
        
        # Create figure and two 3D subplots
        fig = plt.figure(figsize=(12, 6))
        ax1 = fig.add_subplot(121, projection='3d')  # Actual values plot
        ax2 = fig.add_subplot(122, projection='3d')  # Percent difference plot
        
        norm = Normalize(vmin=min(ratio_Q_EM_Q_ES), vmax=max(ratio_Q_EM_Q_ES))
        
        # Plotting the data points for the actual values and perc diff values
        sc1 = ax1.scatter(coll_list, beta_list, omt_list, s=resized_Q_ratio_list, c=ratio_Q_EM_Q_ES, cmap='plasma', edgecolor='black', norm=norm, zorder=1)
        sc2 = ax2.scatter(coll_diff, beta_diff, omt_diff, s=resized_Q_ratio_list, c=ratio_Q_EM_Q_ES, cmap='plasma', edgecolor='black', norm=norm, zorder=1)
        
        # Highlight the reference data point
        reference_label = 'Reference Sim.'
        for idx, (coll, beta, omt) in enumerate(zip(coll_list, beta_list, omt_list)):
            if (coll == ref_coll) and (beta == ref_beta) and (omt == ref_omt):
                ax1.scatter(coll, beta, omt, s=resized_Q_ratio_list[idx]*1.3, edgecolor='red', facecolors='none', linewidth=3)
                ax2.scatter(coll_diff[idx], beta_diff[idx], omt_diff[idx], s=resized_Q_ratio_list[idx]*1.3, edgecolor='red', label=reference_label, facecolors='none', linewidth=3)
                reference_label = "_nolegend_"  # ensures label is only added once
                
                
        if cutoff_value is not None:
            meets_cutoff_value = [val == cutoff_value for val in ratio_Q_EM_Q_ES]
            if any(meets_cutoff_value):
                ax1.scatter([coll for coll, cond in zip(coll_list, meets_cutoff_value) if cond],
                           [beta for beta, cond in zip(beta_list, meets_cutoff_value) if cond],
                           [omt for omt, cond in zip(omt_list, meets_cutoff_value) if cond],
                           c='r', s=300, marker='x', linewidth=3,
                           label=f'Q_EM/Q_ES > {cutoff_value}')
                ax2.scatter([coll for coll, cond in zip(coll_diff, meets_cutoff_value) if cond],
                           [beta for beta, cond in zip(beta_diff, meets_cutoff_value) if cond],
                           [omt for omt, cond in zip(omt_diff, meets_cutoff_value) if cond],
                           c='r', s=300, marker='x', linewidth=3)

                
        # Adding figure legend label for reference simulation
        legend = fig.legend(loc=(0.32, 0.78), markerscale=2, fontsize=12)
        
        for handle in legend.legendHandles:
            handle._sizes = [300]  # set legend marker size to 100, you can adjust this value

        # Add colorbar
        cbar_ax = fig.add_axes([0.93, 0.15, 0.02, 0.6])  # positioning the colorbar
        cbar = fig.colorbar(sc1, cax=cbar_ax)
        cbar.set_label(r'$Q_{EM}/Q_{ES}$', fontsize=14)
        
        # Set titles and labels for both plots
        ax1.set_title('Kymin = ' + str(kymin))
        ax1.set_xlabel('Coll', labelpad=20, size=15)
        ax1.set_ylabel('Beta', labelpad=25, size=15)
        ax1.set_zlabel('Omt (elec)', labelpad=10, size=15)
        # Adjusting x and y axis label angles
        ax1.tick_params(axis='x', labelrotation=30)
        ax1.tick_params(axis='y', labelrotation=-45)

        ax2.set_title('Kymin = ' + str(kymin) + ' (Percent Difference)')
        ax2.set_xlabel('Coll (perc diff)', size=15)
        ax2.set_ylabel('Beta (perc diff)', size=15)
        ax2.set_zlabel('Omt (elec) (perc diff)', size=15)

        # Debugging output
        if debug:
            print(f"Plot generated for kymin = {kymin}")
            print('coll points: \n', data_point_dict['coll'], '\n')
            print('beta points: \n', data_point_dict['beta'], '\n')
            print('omt points: \n', data_point_dict['omt'], '\n')
            print('Q_EM/Q_ES points: \n', data_point_dict['Q_EM/Q_ES'], '\n')
            print('reference point point: \n', data_point_dict['reference_point'], '\n')

        plt.subplots_adjust(right=0.85)  # Adjust layout
        plt.show()




def MTM_3D_kymin_plots(all_kymin_data_points_dict: dict, cutoff_value=None, debug: bool=False):
    """
    Generate 3D plots of kymin, distance from reference simulation, and Q_EM/Q_ES ratio.

    Parameters:
    all_kymin_data_points_dict : dict
        Dictionary containing kymin as keys and data points containing distances and ratio_Q values as values.
    cutoff_value : float, optional
        The cutoff value for Q_EM/Q_ES to highlight in the plot.
    debug : bool, optional
        Flag for debug mode. Not used in current implementation.

    Returns:
    None
    """
    
    # Extract the keys (kymin values) from the input dictionary.
    kymin_list = list(all_kymin_data_points_dict.keys())
    
    # Calculate the global min and max of Q_EM/Q_ES ratio for color normalization.
    all_Q_vals = [val for sublist in [list(dist_3D_from_reference_point(data)['Q_EM/Q_ES']) for data in all_kymin_data_points_dict.values()] for val in sublist]
    global_min_Q, global_max_Q = min(all_Q_vals), max(all_Q_vals)

    # Set up color normalization based on global min and max values or cutoff value.
    if cutoff_value is not None and cutoff_value > global_max_Q:
        norm_Q_vals = plt.Normalize(global_min_Q, cutoff_value)
    else:
        norm_Q_vals = plt.Normalize(global_min_Q, global_max_Q)

    # Set colormap and plot properties.
    colormap = plt.cm.jet
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    # Variable to track if legend for cutoff values has been displayed.
    legend_displayed = False
    
    # Loop through each kymin to plot the data.
    for kymin in kymin_list:
        # Get data points for this kymin.
        data_points_dict = dist_3D_from_reference_point(all_kymin_data_points_dict[kymin])
        dist_vals = data_points_dict['3D_distances']
        ratio_Q_vals = data_points_dict['Q_EM/Q_ES']
        kymin_vals = [kymin + i * 0.1e-10 + 1e-10 for i in range(len(dist_vals))]

        # Create 3D surface plot and scatter plot.
        ax.plot_trisurf(kymin_vals, dist_vals, ratio_Q_vals, color=colormap(norm_Q_vals(kymin)), alpha=0.2)
        scatter = ax.scatter(kymin_vals, dist_vals, ratio_Q_vals, c=ratio_Q_vals, cmap='RdYlGn_r', norm=norm_Q_vals, s=200, edgecolor='black')

        # Highlight points that meet the cutoff value condition.
        if cutoff_value is not None:
            meets_cutoff_value = [val == cutoff_value for val in ratio_Q_vals]
            if any(meets_cutoff_value):
                ax.scatter([ky for ky, cond in zip(kymin_vals, meets_cutoff_value) if cond],
                           [dist for dist, cond in zip(dist_vals, meets_cutoff_value) if cond],
                           [Q for Q, cond in zip(ratio_Q_vals, meets_cutoff_value) if cond],
                           c='r',
                           s=300,
                           marker='x',
                           label=f'Q_EM/Q_ES > {cutoff_value}' if not legend_displayed else "",
                           linewidth=3)

                # Add legend for cutoff values, but only once.
                if not legend_displayed:
                    ax.legend(loc=(0.65, 0.88))
                    legend_displayed = True

    # Add colorbar and axis labels.
    cbar = fig.colorbar(scatter, ax=ax, orientation='vertical', pad=0.1)
    cbar.set_label(r'$Q_{EM}/Q_{ES}$', fontsize=15)
    ax.set_xlabel('kymin', labelpad=10, size=15)
    ax.set_ylabel('Dist. from ref sim', labelpad=10, size=15)
    ax.set_zlabel('$Q_{EM}/Q_{ES}$', labelpad=10, size=15)
    
    # Set the 3D view angle.
    ax.view_init(azim=-80)
    
    # Display the plot.
    plt.show()
