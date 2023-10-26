#!/usr/bin/env python3
import os
import sys
import pandas as pd
from GP_file_functions_V4 import suffix_from_filename, string_to_list, find_buried_filetype_files
from GP_criteria_functions_V4 import criteria_parser, criteria_dict_checker

cwd = os.getcwd()
os.chdir(os.path.join(cwd, 'parameters_data'))
from GP_parameters_data_V4 import parameters_filepath_to_dict
os.chdir(os.path.join(cwd, 'omega_data'))
from GP_omega_data_V4 import omega_filepath_to_dict
os.chdir(os.path.join(cwd, 'nrg_data'))
from GP_nrg_data_V4 import nrg_filepath_to_dict, nrg_quantities_from_criteria, time_from_criteria_list

import time


simulation_key_list = ['input_directory', 
                       'filepath', 
                       'suffix', 
                       'simulation_filepaths', 
                       'status']

#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT filepath list TO simulation dict list---------------------------------
#------------------------------------------------------------------------------------------------

def filepath_to_simulation_dict_list(filepath_list, criteria_list=[], load_files='parameters', load_spec='all', debug:bool=False):
    """
    Parse a list of file paths to extract simulation dictionaries based on given criteria.
    
    This function scans the specified file paths to extract simulation-related information
    and checks if they meet the criteria provided. It's designed primarily for 'parameters' files.
    
    Parameters:
    - filepath_list (str or list): File paths or directory paths where 'parameters' files might be found.
    - criteria_list (str or list): List of criteria to filter simulations.
    - load_files (str or list): File types to load.
    - debug (bool): A flag for printing debug information. Default is False.
    
    Returns:
    - list: A list of dictionaries containing simulation information that matches the criteria.
    """

    if debug: start_time = time.time()

    simulation_dict_list = []

    # Convert string inputs to list if they are not already lists
    filepath_list = string_to_list(filepath_list)
    common_path = os.path.commonpath(filepath_list)

    # Convert the criteria list into a list, and then to a list of dictionaries for easier checking
    criteria_list = string_to_list(criteria_list)
    criteria_dict_list = criteria_parser(criteria_list)

    
    load_files = string_to_list(load_files)
    if load_spec != 'all':
        load_spec = string_to_list(load_spec)

        
    # Search for 'parameters' files up to a specified depth
    max_depth = 2
    parameter_filepath_list = find_buried_filetype_files(filepath_list, 'parameters', max_depth)


    # Handle case where no 'parameters' files are found
    if len(parameter_filepath_list) == 0:
        print(f"No 'parameters' files found at maximum depth of {max_depth} directories down. Try giving a more specific filepath or moving your simulations up directories.")
    else:
        # Process each 'parameters' file found
        for parameter_filepath in parameter_filepath_list:
            parameter_filename = os.path.basename(parameter_filepath)
            simulation_directory = os.path.dirname(parameter_filepath)
            suffix = suffix_from_filename(parameter_filename)

            
            # Convert file paths to dictionaries containing simulation information
            simulation_dict = simulation_filepath_to_dict(simulation_directory, common_path, suffix, 
                                                          load_files, load_spec, criteria_dict_list)            

            # Check if all criteria are satisfied
            all_criteria_pass = all_criteria_checker(simulation_dict, criteria_dict_list, debug)

            # Append to results if criteria are met
            if all_criteria_pass:
                simulation_dict_list.append(simulation_dict)

    # Debug logging
    if debug:
        end_time = time.time()
        print(filepath_list)
        print('Total run time to find simulation files:', end_time - start_time, 's')

    # Provide feedback if no results are found
    if not simulation_dict_list and not criteria_list:
        print('No simulations could be found. Please check the directory path given to ensure there are simulations.')
    elif not simulation_dict_list and criteria_list:
        print('No simulations could be found with the following criteria. Please relax the criteria given.')

    return simulation_dict_list


#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT simulation TO DICT----------------------------------------------------
#------------------------------------------------------------------------------------------------

def simulation_filepath_to_dict(simulation_filepath:str, common_path:str, suffix:str, 
                                load_files:list, load_spec:list, criteria_dict_list:list):
    """
    Convert a simulation filepath to a dictionary containing simulation information.

    This function extracts relevant information from a simulation file path and 
    other specified files based on the provided suffix and files to load. 
    It's specifically designed to handle files with '.dat' suffix and parameters, 
    omega, and nrg file types. Additional file types can be added as needed.
    
    Parameters:
    - simulation_filepath (str): The directory path of the simulation.
    - suffix (str): The suffix used for specific simulation files. 
                    If the suffix already has a '.dat' extension, it's used as is; 
                    otherwise, an underscore is prepended.
    - load_files (list): List of file types to extract from the simulation directory. 
                         Current supported types are 'omega' and 'nrg'.
    
    Returns:
    - dict: A dictionary containing information extracted from the simulation 
            and the specified files.
    """
    #Extract unique portion of simulation filepath
    unique_simulation_filepath = os.path.relpath(simulation_filepath, common_path)


    # Base simulation dictionary with the directory and suffix
    simulation_dict = {'input_directory': simulation_filepath,
                       'filepath': unique_simulation_filepath,
                       'suffix': suffix,
                       'simulation_filepaths': get_simulation_files(simulation_filepath, suffix),
                       'key_list': simulation_key_list}
    
    omega_filepath = load_simulation_filepath(simulation_dict, 'omega')
    check_empty = (os.stat(omega_filepath).st_size == 0)
    if check_empty:
        simulation_dict['status'] = 'NOT CONVERGED'
    else:
        simulation_dict['status'] = 'CONVERGED'




    # If suffix has a '.dat', no change is needed, otherwise prepend an underscore
    mod_suffix = suffix if '.dat' in suffix else '_' + suffix
    
    # Construct the filepath for the 'parameters' file and extract its content into a dictionary
    parameter_filename = 'parameters' + mod_suffix
    parameter_filepath = os.path.join(simulation_filepath, parameter_filename)
    parameter_dict = parameters_filepath_to_dict(parameter_filepath)
    simulation_dict['parameters_dict'] = parameter_dict

    # If 'omega' is in the list of files to load, construct its filepath and extract its content
    if 'omega' in load_files:
        omega_filepath = load_simulation_filepath(simulation_dict, 'omega')
        omega_dict = omega_filepath_to_dict(omega_filepath)
        simulation_dict['omega_dict'] = omega_dict 
    
    # If 'nrg' is in the list of files to load, construct its filepath, 
    # and using the 'n_spec' value from the parameters, extract its content
    if 'nrg' in load_files:
        nrg_filepath = load_simulation_filepath(simulation_dict, 'nrg')

        # get time slice from criteria
        nrg_quantities = nrg_quantities_from_criteria(criteria_dict_list)
        time_slice = time_from_criteria_list(criteria_dict_list)

        # get nrg column values from criteria

        # print(nrg_filepath)
        # print(time_slice)
        # print(load_spec)
        # print(nrg_quantities)


        nrg_dict = nrg_filepath_to_dict(nrg_filepath, choose_time=time_slice, 
                                        named_spec_row=load_spec, named_nrg_col=nrg_quantities)
        simulation_dict['nrg_dict'] = nrg_dict

        # print(nrg_dict)
    
    # Placeholder for more file types that might be needed in the future
    # TODO: - add more filetypes if statements
     
    return simulation_dict





#------------------------------------------------------------------------------------------------
# Function to check if the simulations meet the specified criteria-------------------------------
#------------------------------------------------------------------------------------------------

def all_criteria_checker(simulation_dict:dict, criteria_dict_list:list, debug:bool = False):
    """
    Checks if a simulation dictionary meets all the specified criteria.
    
    This function iterates through the keys of the simulation dictionary and checks
    if the associated sub-dictionaries meet the criteria provided in criteria_dict_list.
    It ensures that every criterion is satisfied by at least one sub-dictionary.
    
    Parameters:
    - simulation_dict (dict): A dictionary containing simulation information.
    - criteria_dict_list (list): A list of dictionaries, each dict specifying a criterion.
    - debug (bool): A flag for printing debug information. Default is False.
    
    Returns:
    - bool: True if all criteria are met, otherwise False.
    """

    
    # Debug printouts for input data
    if debug:
        print(criteria_dict_list)
        print(simulation_dict['filepath'], simulation_dict['suffix'], simulation_dict.keys())

    # Initialize a list to keep track of which criteria have been met
    global_crit_check = [0] * len(criteria_dict_list)

    # Iterate over keys of the simulation dictionary
    for key_name in simulation_dict.keys():
        dict_to_check = simulation_dict[key_name]

        
        
        # If the current key points to a dictionary, check its criteria
        if isinstance(dict_to_check, dict):
            dict_crit_pass_list = criteria_dict_checker(criteria_dict_list, global_crit_check, dict_to_check, debug)
            
            # Update the global criteria checklist
            global_crit_check = [x + y > 0 for x, y in zip(global_crit_check, dict_crit_pass_list)]

            # Debug printouts for current checks
            if debug: 
                print(dict_crit_pass_list)
                print('--------------------')

    # Determine if all criteria were met
    if False in global_crit_check:
        passed_all_criteria = False
    else: 
        passed_all_criteria = True

    # Debug printouts for the final results
    if debug: 
        print('global criteria check:', global_crit_check)
        print('all criteria passed:', passed_all_criteria)
        print('////////////////////')

    return passed_all_criteria

#------------------------------------------------------------------------------------------------
# Function to printout specific simulation data--------------------------------------------------
#------------------------------------------------------------------------------------------------



def printout_simulation_data(filepath_list:str, criteria_list:list=[], load_files:str='parameters', debug:bool=False):
    # Convert string inputs to list if they are not already lists
    if not criteria_list:
        criteria_list = ['filepath', 'suffix']


    filepath_list = string_to_list(filepath_list)
    criteria_list = string_to_list(criteria_list)
    load_files = string_to_list(load_files)

    simulation_dict_list = filepath_to_simulation_dict_list(filepath_list, criteria_list, load_files, debug)
    criteria_dict_list = criteria_parser(criteria_list)

    temp_simulation_dict_list = []

    for simulation_dict in simulation_dict_list:
        temp_simulation_dict = {}

        # Check if all criteria are satisfied
        all_criteria_pass = all_criteria_checker(simulation_dict, criteria_dict_list, debug)

        if all_criteria_pass:
            for criteria_dict in criteria_dict_list:
                units = criteria_dict['units']
                variable_key = criteria_dict['variable_key']

                for sim_key in simulation_dict:
                    
                    if isinstance(simulation_dict[sim_key], dict):
                        current_dict = simulation_dict[sim_key]
                        
                        for current_key in current_dict:
                            unitless = (units==None)
                            
                            if unitless:
                                if variable_key==current_key:
                                    temp_simulation_dict[current_key] = current_dict[current_key]
                            else:
                                if (variable_key in current_key) and (units in current_key):
                                    temp_simulation_dict[current_key] = current_dict[current_key]
                            
                    elif variable_key==sim_key:
                        temp_simulation_dict[sim_key] = simulation_dict[sim_key]
                    elif (sim_key=='filepath') or (sim_key=='suffix'):
                        temp_simulation_dict[sim_key] = simulation_dict[sim_key]
            
            temp_simulation_dict_list.append(temp_simulation_dict)


    df = pd.DataFrame(temp_simulation_dict_list)
    print(df)   





def get_simulation_files(directory:str, suffix:str) -> list:
    """
    Retrieves a list of file paths from a given directory that end with the specified suffix.

    Parameters:
    - directory (str): Path to the directory containing the files.
    - suffix (str): The file suffix to look for (e.g., '.dat' or '0002').

    Returns:
    - list: A sorted list of file paths that end with the specified suffix.
    """
    
    # Initialize an empty list to store the file paths of the simulation files.
    simulation_filepaths = []

    # List all files in the provided directory and sort them.
    filelist = os.listdir(directory)
    filelist.sort()

    # Iterate through the sorted list of filenames.
    for filename in filelist:
        # Construct the absolute path for the current file.
        filepath = os.path.join(directory, filename)
        
        # Check if the current path points to a file.
        check_file = os.path.isfile(filepath)
        # Check if the current filename contains the specified suffix.
        check_suffix = suffix in filename
        
        # If both conditions are satisfied, add the file path to the result list.
        if check_file and check_suffix:
            simulation_filepaths.append(filepath) 

    return simulation_filepaths



def load_simulation_filepath(simulation_dict:dict, filetype:str) -> str:
    """
    Searches for a file with the specified filetype within a dictionary of simulation file paths 
    and returns its path if found.

    Parameters:
    - simulation_dict (dict): Dictionary containing a key 'simulation_filepaths' that maps to a list of file paths.
    - filetype (str): Type of file to search for within the filepaths (e.g., 'omega' or 'nrg').

    Returns:
    - str: File path of the file with the specified type. None if not found.
    """
    
    # Extract the list of simulation file paths from the dictionary.
    simulation_filepaths = simulation_dict['simulation_filepaths']

    # Iterate through the file paths.
    for filepath in simulation_filepaths:
        # Extract the filename from the filename. (i.e. 'omega_0003')
        filename = os.path.basename(filepath)

        # If the filename contains the specified filetype, return its path. (if 'omega' in 'omega_0003')
        if filetype in filename:
            return filepath

#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


# ~~~TERMINAL COMMAND CODE~~~
if __name__ == "__main__":
    cwd = os.getcwd()
    
