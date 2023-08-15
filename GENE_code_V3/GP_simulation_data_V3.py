#!/usr/bin/env python3
import os
from GP_file_functions_V3 import suffix_from_filename, file_check, string_to_list, find_filetype_files
from GP_criteria_functions_V3 import criteria_parser, criteria_dict_checker

from GP_parameter_data_V3 import parameter_filepath_to_dict
from GP_omega_data_V3 import omega_filepath_to_dict
from GP_nrg_data_V3 import nrg_filepath_to_dict

import time


#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT filepath list TO simulation dict list---------------------------------
#------------------------------------------------------------------------------------------------

def filepath_to_simulation_dict_list(filepath_list, criteria_list=[], load_files='parameters', debug:bool=False):
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

    # Convert string inputs to list if they are not already lists
    filepath_list = string_to_list(filepath_list)
    criteria_list = string_to_list(criteria_list)
    load_files = string_to_list(load_files)

    simulation_dict_list = []

    # Convert the criteria list into a list of dictionaries for easier checking
    criteria_dict_list = criteria_parser(criteria_list)

    # Search for 'parameters' files up to a specified depth
    max_depth = 2
    parameter_filepath_list = find_filetype_files(filepath_list, 'parameters', max_depth)

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
            simulation_dict = simulation_filepath_to_dict(simulation_directory, suffix, load_files)

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

def simulation_filepath_to_dict(simulation_filepath:str, suffix:str, load_files:list = []):
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
    
    # Base simulation dictionary with the directory and suffix
    simulation_dict = {'filepath': simulation_filepath,
                       'suffix': suffix}
    
    # If suffix has a '.dat', no change is needed, otherwise prepend an underscore
    mod_suffix = suffix if '.dat' in suffix else '_' + suffix
    
    # Construct the filepath for the 'parameters' file and extract its content into a dictionary
    parameter_filename = 'parameters' + mod_suffix
    parameter_filepath = os.path.join(simulation_filepath, parameter_filename)
    parameter_dict = parameter_filepath_to_dict(parameter_filepath)
    simulation_dict['parameters_dict'] = parameter_dict

    # If 'omega' is in the list of files to load, construct its filepath and extract its content
    if 'omega' in load_files: 
        omega_filename = 'omega' + mod_suffix
        omega_filepath = os.path.join(simulation_filepath, omega_filename)
        omega_dict = omega_filepath_to_dict(omega_filepath)
        simulation_dict['omega_dict'] = omega_dict 
    
    # If 'nrg' is in the list of files to load, construct its filepath, 
    # and using the 'n_spec' value from the parameters, extract its content
    if 'nrg' in load_files:
        nrg_filename = 'nrg' + mod_suffix
        nrg_filepath = os.path.join(simulation_filepath, nrg_filename)
        n_spec = parameter_dict['n_spec']
        nrg_dict = nrg_filepath_to_dict(nrg_filepath, n_spec)
        simulation_dict['nrg_dict'] = nrg_dict
    
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
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


# ~~~TERMINAL COMMAND CODE~~~
if __name__ == "__main__":
    cwd = os.getcwd()
    
