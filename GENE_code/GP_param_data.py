#!/usr/bin/env python3

# This code will go extract all parameters data from the current directory or sub-directories
import os
import sys
from GENE_POST_simulation_data import simulation_sorter
from GENE_POST_file_checks import file_check, suffix_from_filename
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



def print_parameter(filepath, key_list):
    sort_simulation_list = simulation_sorter(filepath)
    
    print(filepath)

    if not key_list:
        key_list = 'filepath'

    spacer = '~~~~~'
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



if __name__=="__main__":
    filepath = os.getcwd()

    print(filepath)
    
    key_list = ['kymin', 'nz0', 'filepath', 'filename', 'x0']
    print_parameter(filepath, key_list)


