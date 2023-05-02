#!/usr/bin/env python3

import os
from GENE_POST_param_data import parameters_filepaths


def simulations_to_list(filepath):
    # function to collect simulation data in current directory or child directories
    simulation_list = []

    #get parameter filepaths and check how many there are
    param_filepath_list = parameters_filepaths(filepath)
    param_count = len(param_filepath_list)

    if param_count == 0:
        #if there are no parameter files check sub-directories for parameter files
        directory_list = os.listdir(filepath)
        directory_list.sort()

        for directory_name in directory_list:
            # Skip files that start with "X_" 
            if directory_name.startswith('X_'):
                pass
            else:
                directory_path = os.path.join(filepath, directory_name)
                # print(directory_path)
                #if the directory is actually a directory check for any parameters files
                if os.path.isdir(directory_path):
                    param_filepath_list = parameters_filepaths(directory_path)
                    
                    for param_filepath in param_filepath_list:
                        sim_filepath = os.path.dirname(param_filepath)
                        param_file = os.path.basename(param_filepath)
                        suffix = suffix_from_filename(param_file)

                        sim_dict = simulation_to_dict(sim_filepath, suffix)
                        simulation_list.append(sim_dict)
                        
        # pass
    else:
        #if there are any parameter file in the current directory convert them to a dict and add it to the list      
        for param_filepath in param_filepath_list:
            sim_filepath = os.path.dirname(param_filepath)
            param_file = os.path.basename(param_filepath)
            suffix = suffix_from_filename(param_file)

            sim_dict = simulation_to_dict(sim_filepath, suffix)
            simulation_list.append(sim_dict)

    #if there are no parameters files in current or sub-directories throw an error message
    if len(simulation_list) == 0:
        print("Neither the current directory nor any of its child directories contain a file starting with 'parameters', or all child directories start with 'X_'.")

    return simulation_list


def simulation_sorter(filepath, sort_type = 'CONVERGED'):
    sorted_sim_list = []

    all_sim_list = simulations_to_list(filepath)

    for sim_dict in all_sim_list:
        
        if sort_type == sim_dict['status']:
            sorted_sim_list.append(sim_dict)
        elif sort_type == 'ALL':
            sorted_sim_list.append(sim_dict)

    print(sorted_sim_list)

    return sorted_sim_list


# ~~~AUXILLARY FUNCTIONS~~~

def simulation_to_dict(filepath, suffix):
    # function to input important information into simulation dict
    simulation_dict = {}

    # add simulation filepath and suffix
    simulation_dict['filepath'] = filepath
    simulation_dict['suffix'] = suffix

    # get all files associated with the simulation
    simulation_files = get_simulation_files(filepath, suffix)
    simulation_dict['simulation files'] = simulation_files

    # get status of simulation (CONVERGED/NOT CONVERGED) for simulation
    sim_status = simulation_status(simulation_files)
    simulation_dict['status'] = sim_status

    return simulation_dict



def suffix_from_filename(filename):
    # function gets the suffix for a given file
    if '_' in filename:
        suffix = filename[-4:]
    else:
        suffix = '.dat'
    return suffix


def get_simulation_files(directory, suffix):
    # function that gets all files ending with the same suffix as the simulation
    simulation_filepaths = []

    filelist = os.listdir(directory)
    filelist.sort()

    # go through files and add those ending with the given suffix
    for filename in filelist:
        filepath = os.path.join(directory, filename) #get the absolute file path

        check_file = os.path.isfile(filepath)   #check that file is actually a file
        check_suffix = suffix in filename         #check that the suffix (i.e. 0002) is in parameters, else '.dat' is always in a string
        
        #if all checks are fulfilled add the file to the filepath list
        if check_file and check_suffix:
            simulation_filepaths.append(filepath) 

    return simulation_filepaths



def simulation_status(simulation_files):
    #returns simulation status as CONVERGED or NOT CONVERGED based on omega file
    filetype = 'omega' #filetype to check simulation status

    for filepath in simulation_files:
        filename = os.path.basename(filepath)
        
        check_omega = filename.startswith(filetype)
        check_nonempty = (os.stat(filepath).st_size != 0)

        # check if file is omega file
        if check_omega:
            # check if omega file is empty or has data
            if check_nonempty:
                status = 'CONVERGED'
            else:
                status = 'NOT CONVERGED'

    return status




# ~~~TERMINAL COMMAND CODE~~~
if __name__ == "__main__":
    cwd = os.getcwd()
    simulation_list = simulations_to_list(cwd)


    # sort_sim_list = simulation_sorter(cwd)

    for simulation in simulation_list:
        print(simulation['filepath'])
        print(simulation['suffix'], simulation['status'])
        print('~~~~~~~~~~')



    