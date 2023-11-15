#!/usr/bin/env python3
import os
import pandas as pd
from src.utils.file_functions import suffix_from_filename, string_to_list, switch_suffix_file
from src.utils.find_buried_filetypes import find_buried_filetypes

from src.dict_parameters_data import parameters_filepath_to_dict, create_species_tuple
from src.dict_omega_data import omega_filepath_to_dict, convergence_check
from src.dict_nrg_data import nrg_filepath_to_dict
from src.dict_field_data import field_filepath_to_dict


from src.filetype_key_lists import load_criteria_per_dict, simulation_key_list, time_quantities_from_criteria_list, remove_non_numerical_crit
from src.criteria_code.criteria_parser import multi_criteria_to_list
from src.criteria_code.criteria_checker import dict_criteria_check, criteria_array_sifter



#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT filepath list TO simulation dict list---------------------------------
#------------------------------------------------------------------------------------------------

def filepath_to_simulation_dict_list(filepath_list, criteria_list=[], load_spec='all', debug:bool=False):
    """
    Parse a list of file paths to extract simulation dictionaries based on given criteria.
    
    This function scans the specified file paths to extract simulation-related information
    and checks if they meet the criteria provided. It's designed primarily for 'parameters' files.
    
    Parameters:
    - filepath_list (str or list): File paths or directory paths where 'parameters' files might be found.
    - criteria_list (str or list): List of criteria to filter simulations.
    - debug (bool): A flag for printing debug information. Default is False.
    
    Returns:
    - list: A list of dictionaries containing simulation information that matches the criteria.
    """
    
    simulation_dict_list = []

    # Convert string inputs to list if they are not already lists
    filepath_list = string_to_list(filepath_list)

    # Search for 'parameters' files up to a specified depth
    max_depth = 3
    parameter_filepath_list = find_buried_filetypes(filepath_list, 'parameters', max_depth)

    # Handle case where no 'parameters' files are found
    if len(parameter_filepath_list) == 0:
        print(f"No 'parameters' files found at maximum depth of {max_depth} directories down. Try giving a more specific filepath or moving your simulations up directories.")
    else:
        # Process each 'parameters' file found
        for parameter_filepath in parameter_filepath_list:

            # Convert file paths to dictionaries containing simulation information
            simulation_dict, criteria_per_dict = create_sim_dict(parameter_filepath, criteria_list, load_spec)

            if simulation_dict == False:
                continue
            else:
                simulation_dict_list.append(simulation_dict)
            
    
    # Provide feedback if no results are found
    if not simulation_dict_list and not criteria_list:
        print('No simulations could be found. Please check the directory path given to ensure there are simulations.')
    elif not simulation_dict_list and criteria_list:
        print('No simulations could be found with the following criteria. Please relax the criteria given.')

    return simulation_dict_list, criteria_per_dict


#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT simulation TO DICT----------------------------------------------------
#------------------------------------------------------------------------------------------------

def create_sim_dict(parameter_filepath:str, criteria_list:list, load_spec='all'):
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
    # Get relevant simulation information
    parameter_filename = os.path.basename(parameter_filepath)
    suffix = suffix_from_filename(parameter_filename)
    simulation_directory = os.path.dirname(parameter_filepath)

    # short_sim_directory = simulation_directory.split('/')[4:]
    # short_sim_directory = os.path.join(*short_sim_directory)

    # Base simulation dictionary with the directory and suffix
    simulation_dict = {'directory': simulation_directory,
                       'suffix': suffix,
                       'status': convergence_check(parameter_filepath),
                       'simulation_filepaths': get_simulation_files(simulation_directory, suffix),
                       'key_list': simulation_key_list,
                       'species_info': create_species_tuple(parameter_filepath)}


    # Create parameters dict by default
    parameter_dict = parameters_filepath_to_dict(parameter_filepath)
    simulation_dict['parameters_dict'] = parameter_dict

    # If no criteria is given add the parameters dict and return simulation dict
    if criteria_list == []:
        return simulation_dict, {}


    
    species_tuple, _ = create_species_tuple(parameter_filepath, load_spec)

    # Convert the criteria list into a list of criteria dict and group them by which criteria goes to which dict type
    criteria_dict_list = multi_criteria_to_list(criteria_list)
    criteria_per_dict = load_criteria_per_dict(criteria_dict_list, parameter_dict, species_tuple)


    if 'simulation' in list(criteria_per_dict.keys()):
        add_simulation = dict_criteria_check(criteria_per_dict['simulation'], simulation_dict)

        if add_simulation == False:
            return False, criteria_per_dict


    if 'parameters' in list(criteria_per_dict.keys()):
        add_simulation = dict_criteria_check(criteria_per_dict['parameters'], parameter_dict)

        if add_simulation == True:
            simulation_dict['parameters_dict'] = parameter_dict
        else:
            return False, criteria_per_dict


    if 'omega' in list(criteria_per_dict.keys()):
        omega_filepath = switch_suffix_file(parameter_filepath, 'omega')
        omega_dict = omega_filepath_to_dict(omega_filepath)

        add_simulation = dict_criteria_check(criteria_per_dict['omega'], omega_dict)

        if add_simulation == True:
            simulation_dict['omega_dict'] = omega_dict
        else:
            return False, criteria_per_dict
    
    

    if 'nrg' in list(criteria_per_dict.keys()):

        time_criteria, nrg_quantities = time_quantities_from_criteria_list(criteria_per_dict['nrg'], parameter_dict, 'nrg')

        criteria_per_dict['nrg'] = remove_non_numerical_crit(criteria_per_dict['nrg'])

        nrg_filepath = switch_suffix_file(parameter_filepath, 'nrg')
        nrg_dict = nrg_filepath_to_dict(nrg_filepath, time_criteria, load_spec, nrg_quantities)

        nrg_dict = criteria_array_sifter(criteria_per_dict['nrg'], nrg_dict)
        add_simulation = dict_criteria_check(criteria_per_dict['nrg'], nrg_dict)

        if add_simulation == True:
            simulation_dict['nrg_dict'] = nrg_dict
        else:
            return False, criteria_per_dict


    if 'field' in list(criteria_per_dict.keys()):
        pass

    return simulation_dict, criteria_per_dict






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










def sim_filepath_to_df(filepath_list, criteria_list=[], load_spec='all'):

    sim_dict_list, _ = filepath_to_simulation_dict_list(filepath_list, criteria_list, load_spec)
    flat_sim_data_list = []

    for sim in sim_dict_list:
        flat_sim_data = {}
        for key, val in sim.items():
            if isinstance(sim[key], dict):
                for sub_key, sub_val in val.items():
                    flat_sim_data[sub_key] = sub_val
            else:
                flat_sim_data[key] = val
        flat_sim_data_list.append(flat_sim_data)

    # Convert the list of dictionaries to a DataFrame
    sim_df = pd.DataFrame(flat_sim_data_list)

    return sim_df















# #------------------------------------------------------------------------------------------------
# # Function to check if the simulations meet the specified criteria-------------------------------
# #------------------------------------------------------------------------------------------------

# def all_criteria_checker(simulation_dict:dict, criteria_dict_list:list, debug:bool = False):
#     """
#     Checks if a simulation dictionary meets all the specified criteria.
    
#     This function iterates through the keys of the simulation dictionary and checks
#     if the associated sub-dictionaries meet the criteria provided in criteria_dict_list.
#     It ensures that every criterion is satisfied by at least one sub-dictionary.
    
#     Parameters:
#     - simulation_dict (dict): A dictionary containing simulation information.
#     - criteria_dict_list (list): A list of dictionaries, each dict specifying a criterion.
#     - debug (bool): A flag for printing debug information. Default is False.
    
#     Returns:
#     - bool: True if all criteria are met, otherwise False.
#     """

    
#     # Debug printouts for input data
#     if debug:
#         print(criteria_dict_list)
#         print(simulation_dict['filepath'], simulation_dict['suffix'], simulation_dict.keys())

#     # Initialize a list to keep track of which criteria have been met
#     global_crit_check = [0] * len(criteria_dict_list)

#     # Iterate over keys of the simulation dictionary
#     for key_name in simulation_dict.keys():
#         dict_to_check = simulation_dict[key_name]

        
        
#         # If the current key points to a dictionary, check its criteria
#         if isinstance(dict_to_check, dict):
#             dict_crit_pass_list = criteria_dict_checker(criteria_dict_list, global_crit_check, dict_to_check, debug)
            
#             # Update the global criteria checklist
#             global_crit_check = [x + y > 0 for x, y in zip(global_crit_check, dict_crit_pass_list)]

#             # Debug printouts for current checks
#             if debug: 
#                 print(dict_crit_pass_list)
#                 print('--------------------')

#     # Determine if all criteria were met
#     if False in global_crit_check:
#         passed_all_criteria = False
#     else: 
#         passed_all_criteria = True

#     # Debug printouts for the final results
#     if debug: 
#         print('global criteria check:', global_crit_check)
#         print('all criteria passed:', passed_all_criteria)
#         print('////////////////////')

#     return passed_all_criteria

# #------------------------------------------------------------------------------------------------
# # Function to printout specific simulation data--------------------------------------------------
# #------------------------------------------------------------------------------------------------





# def load_simulation_filepath(simulation_dict:dict, filetype:str) -> str:
#     """
#     Searches for a file with the specified filetype within a dictionary of simulation file paths 
#     and returns its path if found.

#     Parameters:
#     - simulation_dict (dict): Dictionary containing a key 'simulation_filepaths' that maps to a list of file paths.
#     - filetype (str): Type of file to search for within the filepaths (e.g., 'omega' or 'nrg').

#     Returns:
#     - str: File path of the file with the specified type. None if not found.
#     """
    
#     # Extract the list of simulation file paths from the dictionary.
#     simulation_filepaths = simulation_dict['simulation_filepaths']

#     # Iterate through the file paths.
#     for filepath in simulation_filepaths:
#         # Extract the filename from the filename. (i.e. 'omega_0003')
#         filename = os.path.basename(filepath)

#         # If the filename contains the specified filetype, return its path. (if 'omega' in 'omega_0003')
#         if filetype in filename:
#             return filepath

# #------------------------------------------------------------------------------------------------
# #------------------------------------------------------------------------------------------------
# #------------------------------------------------------------------------------------------------




# ~~~TERMINAL COMMAND CODE~~~
if __name__ == "__main__":
    cwd = os.getcwd()
    
