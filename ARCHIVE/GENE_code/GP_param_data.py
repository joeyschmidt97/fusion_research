#!/usr/bin/env python3

# This code will go extract all parameters data from the current directory or sub-directories
import os
import sys
import pandas as pd
from GP_simulation_data import simulation_sorter, simulation_to_dict
from GP_file_checks import file_check, suffix_from_filename
sys.path.append('/global/homes/j/joeschm/ifs_scripts')
from genetools import Parameters



# def parameter_to_sim_dict(simulation_list):
def parameter_to_sim_dict(simulation_dict):
    simulation_files = simulation_dict['simulation files']

    for filepath in simulation_files:
        check_param = file_check(filepath, 'parameters')

        # check if file is parameter file
        if check_param:
            parameter_dict = param_filepath_to_dict(filepath)
            simulation_dict['parameters'] = parameter_dict
    
    return simulation_dict



def print_parameter(filepath, key_list = 'filepath'):

    #Check if filepath is for the entire simulation or a single parameter
    if 'parameter' in os.path.basename(filepath):
        filename = os.path.basename(filepath)
        suffix = suffix_from_filename(filename)
        parameter_directory = os.path.dirname(filepath)

        simulation_dict = simulation_to_dict(parameter_directory, suffix)
        sort_simulation_list = [simulation_dict]
    else:    
        sort_simulation_list = simulation_sorter(filepath)
    
    # print(filepath)

    # If key_list is an empty list then make it display filepath
    if not key_list:
        key_list = 'filepath'

    spacer = '~~~~~~~~~~~~~~~~'
    if isinstance(key_list, str):
        key = key_list
        for simulation_dict in sort_simulation_list:
            parameter_to_sim_dict(simulation_dict)
            parameter_dict = simulation_dict['parameters']

            print(os.path.basename(parameter_dict['filepath']), '///', parameter_dict['filename'])
            print(key,':', parameter_dict[key])
            print(spacer)

    elif isinstance(key_list, list):
        for simulation_dict in sort_simulation_list:
            parameter_to_sim_dict(simulation_dict)
            parameter_dict = simulation_dict['parameters']

            print(os.path.basename(parameter_dict['filepath']), '///', parameter_dict['filename'])
            for key in key_list:
                print(key,':', parameter_dict[key])
            print(spacer)



# ~~~AUXILLARY FUNCTIONS~~~

def param_filepath_to_dict(parameter_filepath):
    #get parameter filename and directory path
    parameter_file = os.path.basename(parameter_filepath)
    parameter_directory = os.path.dirname(parameter_filepath)
    suffix = suffix_from_filename(parameter_file)
    
    os.chdir(parameter_directory)   #go into parameter directory

    #create parameter dictionary
    par = Parameters()
    par.Read_Pars(parameter_file)  #read parameter file
    parameter_dict = par.pardict 


    #Add filename and filepath (can be different than diagdir) to dict
    parameter_dict['filename'] = parameter_file
    parameter_dict['filepath'] = parameter_directory
    parameter_dict['suffix'] = suffix

    return parameter_dict



def filepath_to_param_df(filepath, keys_to_include=['kymin']):

    #Check if filepath is for the entire simulation or a single parameter
    if 'parameter' in os.path.basename(filepath):
        filename = os.path.basename(filepath)
        suffix = suffix_from_filename(filename)
        parameter_directory = os.path.dirname(filepath)

        simulation_dict = simulation_to_dict(parameter_directory, suffix)
        sort_simulation_list = [simulation_dict]
    else:    
        sort_simulation_list = simulation_sorter(filepath)


    param_list = []
    
    for simulation_dict in sort_simulation_list:
        parameter_to_sim_dict(simulation_dict)
        param_dict = simulation_dict['parameters']
        param_list.append(param_dict)
    
    param_df = pd.DataFrame(param_list, columns=['filepath', 'suffix'] + keys_to_include)
    
    return param_df



# ~~~RUNNING IN TERMINAL~~~


if __name__=="__main__":
    filepath = os.getcwd()

    print(filepath)
    
    # key_list = ['kymin', 'nz0', 'filepath', 'filename', 'x0']
    # print_parameter(filepath, key_list)

    param_dict = param_filepath_to_dict(filepath)
    param_dict_to_df(param_dict)


