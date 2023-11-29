#!/usr/bin/env python3

import os
from GENE_sim_reader.src.utils.file_functions import file_checks, FileError, switch_suffix_file


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

    if check_empty:
        return {}
    else:
        omega_dict = {'filepath': omega_filepath}

    if not check_empty:
        # Read in the omega file
        with open(omega_filepath, 'r') as file:
            lines = file.readlines()

        # Split lines and put values into omega dict
        for line in lines:
            items = line.split()

            # Add the filename, filepath, and suffix to the omega dictionary
            # omega_dict['kymin'] = float(items[0])
            omega_dict['gamma'] = float(items[1])
            omega_dict['omega'] = float(items[2])   

    return omega_dict


#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT OMEGA TO DICT---------------------------------------------------------
#------------------------------------------------------------------------------------------------

def convergence_check(filetype_path:str):

    if not os.path.basename(filetype_path).startswith('omega'):
        omega_filepath = switch_suffix_file(filetype_path, 'omega')
    else:
        omega_filepath = filetype_path
    
    check_empty = (os.stat(omega_filepath).st_size == 0)
    if check_empty:
        return 'NOT_CONVERGED'
    else:
        return 'CONVERGED'


#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


if __name__=="__main__":
    filepath = os.getcwd()


