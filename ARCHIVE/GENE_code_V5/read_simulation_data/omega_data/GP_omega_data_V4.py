#!/usr/bin/env python3

import os
os.chdir("..")
from GP_file_functions_V4 import file_checks, FileError
# from criteria_checker.filetype_key_lists_V4 import omega_key_list


#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT OMEGA TO DICT---------------------------------------------------------
#------------------------------------------------------------------------------------------------

def omega_filepath_to_dict(omega_filepath:str, debug:bool = False):
    """
    Converts a 'omega' file at a given filepath to a omega dictionary.
    Returns the omega dictionary.
    """
    try:
        file_checks(omega_filepath, filetype='omega')
        omega_dict = create_omega_dict(omega_filepath)

        return omega_dict
    except FileError as e:
        print(e)



def create_omega_dict(omega_filepath:str):
    check_empty = (os.stat(omega_filepath).st_size == 0)

    # omega_filename, omega_directory, suffix = path_to_name_dir_suffix(omega_filepath)

    omega_dict = {
        'filepath': omega_filepath,
        # 'key_list': omega_key_list,
        'kymin': None,
        'gamma': None,
        'omega': None
    }

    if not check_empty:
        # Read in the omega file
        with open(omega_filepath, 'r') as file:
            lines = file.readlines()

        # Split lines and put values into omega dict
        for line in lines:
            items = line.split()

            # Add the filename, filepath, and suffix to the omega dictionary
            omega_dict['kymin'] = float(items[0])
            omega_dict['gamma'] = float(items[1])
            omega_dict['omega'] = float(items[2])   

        omega_dict['status'] = 'CONVERGED'

    return omega_dict



#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


if __name__=="__main__":
    filepath = os.getcwd()


