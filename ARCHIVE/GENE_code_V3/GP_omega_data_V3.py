#!/usr/bin/env python3

import os
from GP_file_functions_V3 import file_check, suffix_from_filename, string_to_list, find_filetype_files


#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT OMEGA TO DICT---------------------------------------------------------
#------------------------------------------------------------------------------------------------

def omega_filepath_to_dict(omega_filepath:str, debug:bool = False):
    """
    Converts a 'omega' file at a given filepath to a omega dictionary.
    Returns the omega dictionary.
    """
    # Get the omega filename and directory path
    omega_file = os.path.basename(omega_filepath)
    omega_directory = os.path.dirname(omega_filepath)
    
    # Check if the filepath is a valid 'omega' file
    check_omega = file_check(omega_filepath, 'omega')
    omega_dict = {}

    if check_omega:
        # Change the current working directory to the omega directory
        os.chdir(omega_directory)

        # Read in the omega file
        with open(omega_file, 'r') as file:
            lines = file.readlines()

        # Split lines and put values into omega dict
        for line in lines:
            items = line.split()

            omega_dict['kymin'] = float(items[0])
            omega_dict['gamma'] = float(items[1])
            omega_dict['omega'] = float(items[2])   

        simulation_status = 'CONVERGED'     

        suffix = suffix_from_filename(omega_filepath)
        omega_dict['suffix'] = suffix

    else:
        # If the filepath is not a valid 'omega' file, print an error message and return None
        if debug:
            print('Filepath given is not a omega file, is empty, or is not a file. Filepath:\n', omega_filepath)
        simulation_status = 'NOT CONVERGED'
      
    # Add the filename, filepath, and suffix to the omega dictionary
    omega_dict['filename'] = omega_file
    omega_dict['filepath'] = omega_directory
    omega_dict['status'] = simulation_status

    return omega_dict


#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


if __name__=="__main__":
    filepath = os.getcwd()


