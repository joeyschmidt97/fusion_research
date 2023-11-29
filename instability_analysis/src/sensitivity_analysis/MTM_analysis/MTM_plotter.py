#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from .MTM_df_builder import MTM_dataframe

from instability_analysis.src.utils.plotting_sphere_disk import cartesian_to_disk

# from instability_analysis.src.utils.plotting_tools.plotting_sphere_disk import sphere_to_disk
 
















#------------------------------------------------------------------------------------------------
# Function to plot MTM plots in 3D---------------------------------------------------------------
#------------------------------------------------------------------------------------------------

def MTM_plots(filepath, criteria_list:list = [], plot_type:str = '3D', override:bool = False):

    csv_filepath = os.path.join(filepath, 'simulation_data.csv')

    if os.path.exists(csv_filepath) and not override:
        # print('reading csv')
        MTM_sim_df = pd.read_csv(csv_filepath)
    else:
        # print('writing csv')
        MTM_sim_df = MTM_dataframe(filepath)
        MTM_sim_df.to_csv(csv_filepath, index=False)


    plot_types = {'3D': '3D',
                  '3D kymin': '3D kymin',
                  'Disk': 'Disk',
                  'Disk w dist': 'Disk w dist'}
        
    if plot_type == plot_types['3D']:
        MTM_3D_plots(MTM_sim_df)
    elif plot_type == plot_types['3D kymin']:
        MTM_3D_kymin_plots(MTM_sim_df)
    elif plot_type == plot_types['Disk']:
        MTM_disk_plot(MTM_sim_df, dist_opacity_origin = False)

    elif plot_type == plot_types['Disk w dist']:
        MTM_disk_plot(MTM_sim_df, dist_opacity_origin = True)

    else:
        print(f'Please specify "plot_type" as one of the following for plotting: \n {list(plot_types.keys())}')

    return




#------------------------------------------------------------------------------------------------
# Functions to plot 3D cube of sensitivity analysis for MTM detection----------------------------
#------------------------------------------------------------------------------------------------

def MTM_3D_plots(MTM_sim_df):
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
    kymin_list = MTM_sim_df['kymin'].unique()


    
    norm_Q_ratio = MTM_sim_df['norm_Q_ratio']
    norm_Q_ratio_rescaled = (norm_Q_ratio - norm_Q_ratio.min()) / (norm_Q_ratio.max() - norm_Q_ratio.min())
    
    max_marker_size = 600
    min_marker_size = 80
    MTM_sim_df['resized_Q_ratio'] = (min_marker_size + (max_marker_size - min_marker_size) * norm_Q_ratio_rescaled)
    

    for kymin in kymin_list:

        kymin_df = MTM_sim_df[MTM_sim_df['kymin'] == kymin]

        # Create figure and two 3D subplots
        fig = plt.figure(figsize=(12, 6))
        ax1 = fig.add_subplot(121, projection='3d')  # Actual values plot
        ax2 = fig.add_subplot(122, projection='3d')  # Percent difference plot

        norm_Q_ratio = kymin_df['norm_Q_ratio']
        resized_Q_ratio = kymin_df['resized_Q_ratio']

        ref_coll = kymin_df['ref_coll']
        ref_beta = kymin_df['ref_beta']
        ref_omt2 = kymin_df['ref_omt2']

        coll_array = kymin_df['coll']
        beta_array = kymin_df['beta']
        omt2_array = kymin_df['omt2']

        pd_coll_array = kymin_df['pd_coll']
        pd_beta_array = kymin_df['pd_beta']
        pd_omt2_array = kymin_df['pd_omt2']

        norm = Normalize(vmin=0, vmax=1)
        
        # Plotting the data points for the actual values and perc diff values
        sc1 = ax1.scatter(coll_array, beta_array, omt2_array, 
                          s=resized_Q_ratio, c=norm_Q_ratio, cmap='plasma', edgecolor='black', norm=norm, zorder=1)
        sc2 = ax2.scatter(pd_coll_array, pd_beta_array, pd_omt2_array, 
                          s=resized_Q_ratio, c=norm_Q_ratio, cmap='plasma', edgecolor='black', norm=norm, zorder=1)
        
        # plot points where Q_ES <= Q_EM 
        red_x_indices = norm_Q_ratio > 0.5
        ax1.scatter(coll_array[red_x_indices], beta_array[red_x_indices], omt2_array[red_x_indices],
                    s=resized_Q_ratio[red_x_indices]*0.5, marker='x', color='red', zorder=2, linewidth=2,
                    label=f'Q_ratio > 0.5')
        ax2.scatter(pd_coll_array[red_x_indices], pd_beta_array[red_x_indices], pd_omt2_array[red_x_indices],
                    s=resized_Q_ratio[red_x_indices]*0.5, marker='x', color='red', zorder=2, linewidth=2)
        
        # Highlight the reference data point
        reference_label = 'Reference Sim'
        ref_point_loc = kymin_df[(kymin_df['coll'] == ref_coll) & (kymin_df['beta'] == ref_beta) & (kymin_df['omt2'] == ref_omt2)].index
        if ref_point_loc.any():
            ax1.scatter(coll_array[ref_point_loc], beta_array[ref_point_loc], omt2_array[ref_point_loc], 
                        s=resized_Q_ratio[ref_point_loc]*1.3, edgecolor='red', facecolors='none', linewidth=2,
                        label=reference_label)
            ax2.scatter(pd_coll_array[ref_point_loc], pd_beta_array[ref_point_loc], pd_omt2_array[ref_point_loc], 
                        s=resized_Q_ratio[ref_point_loc]*1.3, edgecolor='red', facecolors='none', linewidth=2)
                
        
        # Adding figure legend label for reference simulation
        legend = fig.legend(loc=(0.32, 0.78), markerscale=2, fontsize=12)
        
        for handle in legend.legendHandles:
            handle._sizes = [300]  # set legend marker size to 100, you can adjust this value

        # Add colorbar
        cbar_ax = fig.add_axes([0.93, 0.15, 0.02, 0.6])  # positioning the colorbar
        cbar = fig.colorbar(sc1, cax=cbar_ax)
        cbar.set_label(r'$Q_{EM}/(Q_{ES} - Q_{EM})$', fontsize=14)
        
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

        plt.subplots_adjust(right=0.85)  # Adjust layout
        plt.show()

























def MTM_disk_plot(MTM_sim_df, dist_opacity_origin:bool):

    # MTM_sim_df = MTM_sim_df[MTM_sim_df['omt2'] > 11.7]

    # MTM_sim_df = MTM_sim_df[MTM_sim_df['coll'] < 0.02028]

    # MTM_sim_df = MTM_sim_df[MTM_sim_df['beta'] > 0.0058 ]


    kymin_list = MTM_sim_df['kymin'].unique()



    norm_Q_ratio = MTM_sim_df['norm_Q_ratio']
    norm_Q_ratio_rescaled = (norm_Q_ratio - norm_Q_ratio.min()) / (norm_Q_ratio.max() - norm_Q_ratio.min())
    
    max_marker_size = 600
    min_marker_size = 80
    MTM_sim_df['resized_Q_ratio'] = (min_marker_size + (max_marker_size - min_marker_size) * norm_Q_ratio_rescaled)
    

    for kymin in kymin_list:

        kymin_df = MTM_sim_df[MTM_sim_df['kymin'] == kymin]

        # Create figure and two 3D subplots
        fig = plt.figure(figsize=(12, 6))
        ax1 = fig.add_subplot(121)  # Actual values plot
        ax2 = fig.add_subplot(122, projection='3d')  # Percent difference plot

        norm_Q_ratio = kymin_df['norm_Q_ratio']
        resized_Q_ratio = kymin_df['resized_Q_ratio']

        ref_coll = kymin_df['ref_coll']
        ref_beta = kymin_df['ref_beta']
        ref_omt2 = kymin_df['ref_omt2']

        coll_array = kymin_df['coll']
        beta_array = kymin_df['beta']
        omt2_array = kymin_df['omt2']

        pd_coll_array = kymin_df['pd_coll']
        pd_beta_array = kymin_df['pd_beta']
        pd_omt2_array = kymin_df['pd_omt2']

        del_coll = kymin_df['dist_coll']
        del_beta = kymin_df['dist_beta']
        del_omt2 = kymin_df['dist_omt2']


        r = np.sqrt(del_coll**2 + del_beta**2 + del_omt2**2)

        if dist_opacity_origin:    

            # Define the desired range for scaled r
            opac_min = 0.4
            opac_max = 0.8
            min_r = np.min(r)
            max_r = np.max(r)

            # Scale the values of r to the desired range
            opac_r = ((r - min_r) / (max_r - min_r)) * (opac_max - opac_min) + opac_min

        else:
            max_r = np.max(r)
            opac_r = 0.5


        # norm = Normalize(vmin=0, vmax=1)


        point_colors = (norm_Q_ratio - norm_Q_ratio.min()) / (norm_Q_ratio.max() - norm_Q_ratio.min())
        norm = Normalize(vmin=point_colors.min(), vmax=point_colors.max()) 

        x_disk, y_disk = cartesian_to_disk(del_coll, del_beta, del_omt2)

        #offset points slightly
        x_offset = np.random.rand() * 0.1
        y_offset = np.random.rand() * 0.1
  
        ax1.scatter(x_disk + x_offset, y_disk + y_offset, alpha=opac_r, c=norm_Q_ratio, s=resized_Q_ratio/2, cmap='plasma', edgecolor='black', norm=norm)

        x_units = 'coll'
        y_units = 'beta'
        z_units = 'omt2'

        ref_points = [(max_r,0,0, "+" + x_units), (-max_r,0,0, "-" + x_units), 
                (0,max_r,0, "+" + y_units), (0,-max_r,0, "-" + y_units),
                (0,0,max_r, "+" + z_units), (0,0,-max_r, "-" + z_units)]


        for (x_axis, y_axis, z_axis, axis_label) in ref_points:
            xd_ref, yd_ref = cartesian_to_disk(x_axis, y_axis, z_axis)
            ax1.scatter(xd_ref, yd_ref, alpha=1, marker='o', edgecolors='black', facecolors='none')
            ax1.text(xd_ref, yd_ref, axis_label, color='black', fontsize=10, ha='left', va='bottom')


        outer_theta_disk = np.linspace(0, 2*np.pi, 100)
        x_disk_circle = np.cos(outer_theta_disk)*np.pi
        y_disk_circle = np.sin(outer_theta_disk)*np.pi
        ax1.plot(x_disk_circle, y_disk_circle, color='black', linestyle='-', alpha=0.5)
        ax1.plot(x_disk_circle/2, y_disk_circle/2, color='black', linestyle=':')
        ax1.set_title('Sphere-Disk Projection')

        





        sc2 = ax2.scatter(pd_coll_array, pd_beta_array, pd_omt2_array, 
                          s=resized_Q_ratio, c=norm_Q_ratio, cmap='plasma', edgecolor='black', norm=norm, zorder=1)
        
        # plot points where Q_ES <= Q_EM 
        red_x_indices = norm_Q_ratio > 0.5
        ax2.scatter(pd_coll_array[red_x_indices], pd_beta_array[red_x_indices], pd_omt2_array[red_x_indices],
                    s=resized_Q_ratio[red_x_indices]*0.5, marker='x', color='red', zorder=2, linewidth=2)



        cross_x_disk, cross_y_disk = cartesian_to_disk(del_coll[red_x_indices], del_beta[red_x_indices], del_omt2[red_x_indices])
        ax1.scatter(cross_x_disk + x_offset, cross_y_disk + y_offset, s=resized_Q_ratio[red_x_indices]/3, marker='x', color='red', zorder=2, linewidth=2)
        
        # Highlight the reference data point
        reference_label = 'Reference Sim'
        ref_point_loc = kymin_df[(kymin_df['coll'] == ref_coll) & (kymin_df['beta'] == ref_beta) & (kymin_df['omt2'] == ref_omt2)].index
        if ref_point_loc.any():
            ax2.scatter(pd_coll_array[ref_point_loc], pd_beta_array[ref_point_loc], pd_omt2_array[ref_point_loc], 
                        s=resized_Q_ratio[ref_point_loc]*1.3, edgecolor='red', facecolors='none', linewidth=2)
                
        
        # Adding figure legend label for reference simulation
        legend = fig.legend(loc=(0.32, 0.78), markerscale=2, fontsize=12)
        
        for handle in legend.legendHandles:
            handle._sizes = [300]  # set legend marker size to 100, you can adjust this value

        
        cbar_ax = fig.add_axes([0.93, 0.15, 0.02, 0.6])  # positioning the colorbar
        cbar = fig.colorbar(sc2, cax=cbar_ax)
        cbar.set_label(r'$Q_{EM}/(Q_{ES} - Q_{EM})$', fontsize=14)
        


        # Set titles and labels for both plots
        
        ax2.set_title('Kymin = ' + str(kymin) + ' (Percent Difference)')
        ax2.set_xlabel('Coll (perc diff)', size=15)
        ax2.set_ylabel('Beta (perc diff)', size=15)
        ax2.set_zlabel('Omt (elec) (perc diff)', size=15)

        plt.subplots_adjust(right=0.85)  # Adjust layout
        plt.show()





def garbage():

    r = np.sqrt(del_x**2 + del_y**2 + del_z**2)

    if dist_opacity_origin:    

        # Define the desired range for scaled r
        opac_min = 0.4
        opac_max = 0.8
        min_r = np.min(r)
        max_r = np.max(r)

        # Scale the values of r to the desired range
        opac_r = ((r - min_r) / (max_r - min_r)) * (opac_max - opac_min) + opac_min

    else:
        max_r = np.max(r)
        opac_r = 0.5


    x_units = units[0]
    y_units = units[1]
    z_units = units[2]

    ref_points = [(max_r,0,0, "+" + x_units), (-max_r,0,0, "-" + x_units), 
                  (0,max_r,0, "+" + y_units), (0,-max_r,0, "-" + y_units),
                  (0,0,max_r, "+" + z_units), (0,0,-max_r, "-" + z_units)]



    if color_values is None:        
        point_colors = np.ones_like(del_x)
        norm = Normalize(vmin=0, vmax=1)
    else:
        point_colors = (color_values - color_values.min()) / (color_values.max() - color_values.min())
        norm = Normalize(vmin=color_values.min(), vmax=color_values.max()) 

    if plot_3D:
        fig = plt.figure(figsize=(12, 5))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122, projection='3d')  # Set projection to 3D

        sc2 = ax2.scatter(x,y,z, c=point_colors, cmap='plasma', edgecolor='black', norm=norm)
        ax2.scatter(x0,y0,z0, c='red', s=100, marker='*')
        ax2.set_title('3D Projection')
        ax2.set_xlabel(x_units)
        ax2.set_ylabel(y_units)
        ax2.set_zlabel(z_units)

    else:
        fig = plt.figure(figsize=(12, 5))
        ax1 = fig.add_subplot(121)


    x_disk, y_disk = cart_to_disk(del_x, del_y, del_z)
    ax1.scatter(x_disk, y_disk, alpha=opac_r, c=point_colors, cmap='plasma', edgecolor='black', norm=norm)


    for (x_axis, y_axis, z_axis, axis_label) in ref_points:
        xd_ref, yd_ref = cart_to_disk(x_axis, y_axis, z_axis)
        ax1.scatter(xd_ref, yd_ref, alpha=1, marker='o', edgecolors='black', facecolors='none')
        ax1.text(xd_ref, yd_ref, axis_label, color='black', fontsize=10, ha='left', va='bottom')


    outer_theta_disk = np.linspace(0, 2*np.pi, 100)
    x_disk_circle = np.cos(outer_theta_disk)*np.pi
    y_disk_circle = np.sin(outer_theta_disk)*np.pi
    ax1.plot(x_disk_circle, y_disk_circle, color='black', linestyle='-', alpha=0.5)
    ax1.plot(x_disk_circle/2, y_disk_circle/2, color='black', linestyle=':')
    ax1.set_title('Sphere-Disk Projection')

    
    cbar_ax = fig.add_axes([0.93, 0.15, 0.02, 0.6])  # positioning the colorbar
    cbar = fig.colorbar(sc2, cax=cbar_ax)
    cbar.set_label(r'$Q_{EM}/(Q_{ES} - Q_{EM})$', fontsize=14)
    






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






