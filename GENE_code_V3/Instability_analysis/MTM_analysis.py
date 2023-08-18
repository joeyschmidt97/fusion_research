#!/usr/bin/env python3

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import sys
sys.path.insert(1, '/global/u1/j/joeschm/fusion_research/GENE_code_V3')
from GP_simulation_data_V3 import filepath_to_simulation_dict_list, species_value_from_simulation


def MTM_plots(filepath_list:list, criteria_list:list = [], plot_type:str = '3D', debug:bool = False):

    #MIGHT HAVE TO LOAD IN NRG FILES HERE FOR RATIOS
    # simulation_dict_list = filepath_to_simulation_dict_list(filepath_list, criteria_list, load_files='nrg')
    # TODO: BELOW CODE IS FOR TESTING PURPOSE REMOVE WHEN STARTING TO DO Q ratios
    simulation_dict_list = filepath_to_simulation_dict_list(filepath_list, criteria_list, load_files='nrg')

    if plot_type == '3D':
        MTM_3D_plots(simulation_dict_list, debug=debug)
    elif plot_type == '2D':
        # TODO: add 2D plotting
        pass
    else:
        print('Please specify "plot_type" as either "2D" or "3D" for plotting.')

    return


def MTM_3D_plots(simulation_dict_list:list, debug:bool = False):

    kymin_list = collect_kymin_list(simulation_dict_list)

    for kymin in kymin_list:
        kymin_simulation_dict_list = []

        for simulation_dict in simulation_dict_list:        
            if kymin == simulation_dict['parameters_dict']['kymin']:
                kymin_simulation_dict_list.append(simulation_dict)

        single_3D_plot(kymin, kymin_simulation_dict_list, debug=debug)
    

    return None


def single_3D_plot(kymin:float, kymin_simulation_dict_list:list, species:str = 'e', debug:bool = False):

    coll_list = []
    beta_list = []
    omt_list = []

    point_list = []

    for kymin_simulation_dict in kymin_simulation_dict_list:
        coll = kymin_simulation_dict['parameters_dict']['coll']
        beta = kymin_simulation_dict['parameters_dict']['beta']

        omt_name = species_value_from_simulation(kymin_simulation_dict, 'omt', species)
        omt = kymin_simulation_dict['parameters_dict'][omt_name]

        Q_EM_name = species_value_from_simulation(kymin_simulation_dict, 'Q_EM', species)
        Q_ES_name = species_value_from_simulation(kymin_simulation_dict, 'Q_ES', species)
        Q_EM = kymin_simulation_dict['nrg_dict'][Q_EM_name][-1]
        Q_ES = kymin_simulation_dict['nrg_dict'][Q_ES_name][-1]

        points = ((coll, beta, omt), Q_EM/Q_ES)
        # points = ((coll, beta, omt), Q_ES/Q_EM)   #CHECK RATIO
        point_list.append(points)



    # Extracting coordinates and values
    coordinates, values = zip(*point_list)
    x, y, z = zip(*coordinates)
    values = np.array(values)

    # Calculating sizes and colors based on values
    max_value = max(values)
    min_value = min(values)

    # Defining a size range for the dots (you can adjust as necessary)
    min_size = 10
    max_size = 100
    sizes = ((values - min_value) / (max_value - min_value)) * (max_size - min_size) + min_size

    # Defining colors for the dots
    colors = plt.cm.RdYlGn_r((values - min_value) / (max_value - min_value))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    sc = ax.scatter(x, y, z, c=colors, s=sizes, edgecolors='black', linewidth=0.5, depthshade=False)

    # Add color bar on the right side of the graph
    cbar = fig.colorbar(sc, ax=ax, orientation='vertical', fraction=0.05, pad=0.1)
    cbar.set_label('Q_EM/Q_ES')

    ax.set_xlabel('coll')
    ax.set_ylabel('beta')
    ax.set_zlabel('omt')

    plt.show()



    return


#------------------------------------------------------------------------------------------------
# Function to collect unique kymin values from simulations---------------------------------------
#------------------------------------------------------------------------------------------------

def collect_kymin_list(simulation_dict_list):
    kymin_list = []

    for simulation_dict in simulation_dict_list:
        kymin = simulation_dict['parameters_dict']['kymin']

        if kymin not in kymin_list:
            kymin_list.append(kymin)

    kymin_list.sort()

    return kymin_list

