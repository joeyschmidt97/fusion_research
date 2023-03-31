#!/usr/bin/env python3

# This code will go into all the sub-directories and extract all parameters data 

import os
from GENE_POST_param_2_dict import param_list


def sim_data():
    simulation_dict = {} 

    cwd = os.getcwd()
    directory_list = os.listdir(cwd)
    directory_list.sort()

    for directory_name in directory_list:
        directory_path = os.path.join(cwd, directory_name)

        if os.path.isdir(directory_path):   
            parameter_list = param_list(directory_path)


            simulation_dict['parameters'] = parameter_list

        else:  
            pass

    return simulation_dict

if __name__ == "__main__":
    simulation_dict = sim_data()

    parameter_list = simulation_dict['parameters']

    for parameter in parameter_list:
        print(parameter['kymin'], parameter['diagdir'])
    





