import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from instability_analysis.src.basic_analysis_tools.growth_rate.growth_rate_df_builder import growth_freq_dataframe





def gamma_omega_plot(filepath, criteria_list = ['gamma', 'omega'], plot_mode='kymin', label_key='nz0', verbose = False):

    if isinstance(filepath, str): filepath = [filepath]

    gr_sim_df = growth_freq_dataframe(filepath, criteria_list) 
    
    converged = gr_sim_df['status'] == 'CONVERGED'
    gr_sim_df = gr_sim_df[converged]

    if label_key == 'theta_0':
        gr_sim_df['kx_center'].fillna(0, inplace=True)
        gr_sim_df['theta_0'] = gr_sim_df['kx_center']/(gr_sim_df['shat']*gr_sim_df['kymin'])
        gr_sim_df['theta_0'] = gr_sim_df['theta_0'].round(3)

    if label_key.strip() == 'theta_0(deg)':
        gr_sim_df['kx_center'].fillna(0, inplace=True)
        gr_sim_df['theta_0'] = gr_sim_df['kx_center']/(gr_sim_df['shat']*gr_sim_df['kymin'])
        gr_sim_df['theta_0(deg)'] = gr_sim_df['theta_0']*(180/np.pi)
        gr_sim_df['theta_0(deg)'] = gr_sim_df['theta_0(deg)'].round(3)



    gr_sim_df = gr_sim_df.sort_values(by='kymin')


    # if isinstance(filepath_list, str): filepath_list = [filepath_list]
    # if plot_mode == 'global':
    #     x_name = 'n0_global'
    #     y_gamma_name = f"gamma (kHz)"
    #     y_omega_name = f"omega (kHz)"
    # elif plot_mode == 'kymin':
    #     x_name = 'kymin'
    #     y_gamma_name = f"gamma (cs/a)"
    #     y_omega_name = f"omega (cs/a)"

    
    if len(filepath) == 1:
        fig, (gamma_ax, omega_ax) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
    elif len(filepath) > 1:
        fig, ((gamma_ax, omega_ax), (gamma_diff, omega_diff)) = plt.subplots(nrows=2, ncols=2, 
                                                                             gridspec_kw={'height_ratios': [2, 1]}, 
                                                                             figsize=(10, 6))


    # Assuming gr_sim_df[label_key] is a categorical variable with unique values
    unique_values = gr_sim_df[label_key].unique()
    unique_values = np.sort(unique_values)

    # Create a colormap with a color for each unique value
    colors = plt.cm.brg(np.linspace(0, 1, len(unique_values)))
    # colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_values)))


    # Iterate over unique values and plot with different colors
    for i, unique_value in enumerate(unique_values):
        subset_df = gr_sim_df[gr_sim_df[label_key] == unique_value]

        plot_label = f"{label_key} = {unique_value}"

        gamma_ax.set_xscale('log')
        gamma_ax.set_xlabel('kymin', fontsize=15)
        gamma_ax.set_ylabel('gamma (cs/a)', fontsize=15)
        gamma_ax.plot(subset_df['kymin'], subset_df['gamma'], label=plot_label, marker='o', markersize=5, linestyle='dotted', color=colors[i])
        gamma_ax.legend()

        omega_ax.set_xscale('log')
        omega_ax.set_xlabel('kymin', fontsize=15)
        omega_ax.set_ylabel('omega (cs/a)', fontsize=15)
        omega_ax.plot(subset_df['kymin'], subset_df['omega'], label=plot_label, marker='o', markersize=5, linestyle='dotted', color=colors[i])
        omega_ax.legend()



        if verbose:
            print('x-values for filepath:', subset_df['filepath'].unique())
            x_decimal_list = [float(f"{value:.1f}") for value in subset_df['kymin']]
            print(x_decimal_list)


            for _, (x_val, y_val) in enumerate(zip(subset_df['kymin'], subset_df['gamma'])):
                label = f"{x_val:.1f}"  # Format the label with two decimal places
                gamma_ax.annotate(label, xy=(x_val, y_val), xytext=(-5, 10), textcoords='offset points')



    # Show the plot
    plt.tight_layout()
    plt.show()





def log_plotting(fig, ax, gr_sim_df, x_name, y_name, verbose):
    
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






