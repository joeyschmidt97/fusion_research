#!/usr/bin/env python3

# This code will go into all the sub-directories and extract all parameters data 
import os
from GENE_POST_param_data import parameters_to_list
from GENE_POST_omega_data import omegas_to_list


def simulations_to_data(filepath):
    simulation_list = []

    directory_list = os.listdir(filepath)
    directory_list.sort()

    for directory_name in directory_list:
        
        # Skip files that start with "X_" 
        if directory_name.startswith('X_'):
            pass

        else:
            simulation_dict = {} 
            directory_path = os.path.join(filepath, directory_name)

            if os.path.isdir(directory_path):
                parameter_list = parameters_to_list(directory_path)
                simulation_dict['parameters'] = parameter_list

                omega_list = omegas_to_list(directory_path)
                simulation_dict['omegas'] = omega_list

                simulation_dict['filepath'] = directory_path
                simulation_list.append(simulation_dict)

            else:  
                pass

    return simulation_list



if __name__ == "__main__":
    cwd = os.getcwd()
    simulation_list = simulations_to_data(cwd)

    for simulation_dict in simulation_list:
        filepath = simulation_dict['filepath']
        parameter_list = simulation_dict['parameters']
        omega_list = simulation_dict['omegas']

        print(filepath)

        for parameter in parameter_list:
            print(parameter['kymin'], parameter['filename'])

        for omega in omega_list:
            print(omega['kymin'], omega['gamma (cs/a)'], omega['omega (cs/a)'], omega['filename'])
        
