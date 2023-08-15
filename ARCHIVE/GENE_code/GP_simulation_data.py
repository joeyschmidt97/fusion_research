#!/usr/bin/env python3
import os
from GP_convergence_check import convergence_check
from GP_file_checks import suffix_from_filename, file_check



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

    return sorted_sim_list


# ~~~AUXILLARY FUNCTIONS~~~

def parameters_filepaths(directory):
    param_filepath_list = []    #list to store parameter filepaths in the given directory
    
    #get files in given directory
    filelist = os.listdir(directory)
    filelist.sort()
    for filename in filelist:
        filepath = os.path.join(directory, filename) #get the absolute file path
        check_param = file_check(filepath , 'parameters') # check file is parameter, is a file, and non-empty

        if check_param:
            param_filepath_list.append(filepath) #add parameter filepath to list
    
    #if we have multiple parameters files then remove the base parameter file (parameters.dat)
    if len(param_filepath_list) > 1:
        for param_filepath in param_filepath_list[:]:  # iterate over a copy of the list to safely modify it
            if not os.path.basename(param_filepath).startswith('parameters_'):
                param_filepath_list.remove(param_filepath)

    return param_filepath_list



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
    sim_status = convergence_check(simulation_dict)
    simulation_dict['status'] = sim_status

    return simulation_dict



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



# ~~~TERMINAL COMMAND CODE~~~
if __name__ == "__main__":
    cwd = os.getcwd()
    simulation_list = simulations_to_list(cwd)

    # sort_sim_list = simulation_sorter(cwd)

    for simulation in simulation_list:
        print(simulation['filepath'])
        print(simulation['suffix'], simulation['status'])
        print('~~~~~~~~~~')

