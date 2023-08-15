#!/usr/bin/env python3

import os
import numpy as np
from GP_file_functions_V3 import file_check, suffix_from_filename


#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT nrg TO DICT-----------------------------------------------------------
#------------------------------------------------------------------------------------------------

import os
import numpy as np

def nrg_filepath_to_dict(nrg_filepath: str, n_spec: int, debug: bool = False):
    """
    Converts a 'nrg' file at a given filepath to a nrg dictionary.
    Returns the nrg dictionary.
    """
    
    # Check if the filepath is a valid 'nrg' file
    check_param = file_check(nrg_filepath, 'nrg')
    
    # If the file check fails, print an error message and return an empty dictionary
    if not check_param:
        if debug:
            print('Filepath given is not an nrg file, is empty, or is not a file. Filepath:\n', nrg_filepath)
        return {}

    # Helper function to generate the base structure of the species energy dictionary
    def create_spec_nrg_dict():
        return {
            'n_mag':      {'value': [], 'units': 'cs/a'},
            'u_par_mag':  {'value': [], 'units': 'cs/a'},
            'T_par_mag':  {'value': [], 'units': 'cs/a'},
            'T_perp_mag': {'value': [], 'units': 'cs/a'},
            'Gamma_ES':   {'value': [], 'units': 'cs/a'},
            'Gamma_EM':   {'value': [], 'units': 'cs/a'},
            'Q_ES':       {'value': [], 'units': 'cs/a'},
            'Q_EM':       {'value': [], 'units': 'cs/a'},
            'Pi_ES':      {'value': [], 'units': 'cs/a'},
            'Pi_EM':      {'value': [], 'units': 'cs/a'}
        }

    # Extract the keys from the base structure for later use
    spec_nrg_keys = list(create_spec_nrg_dict().keys())

    # Initialize the main dictionary to store all data
    nrg_dict = {'time': {'value': [], 'units': 's'}}
    for i in range(n_spec):
        species_number = i + 1
        for key_name in spec_nrg_keys:
            nrg_dict[key_name + str(species_number)] = create_spec_nrg_dict()[key_name]

    # Read the nrg file and parse the data
    with open(nrg_filepath, 'r') as file:
        spec_count = 0

        for line in file:
            items = line.split()
            
            # If there's only one item in the line, it's a timestamp
            if len(items) == 1:
                nrg_dict['time']['value'].append(float(items[0]))
                spec_count = 0
            else:
                # Otherwise, parse the species energy values
                spec_count += 1
                for j, key_name in enumerate(spec_nrg_keys):    #j values refer to columns in nrg file
                    nrg_dict[key_name + str(spec_count)]['value'].append(float(items[j]))

    # Convert lists to numpy arrays for efficiency
    for key in nrg_dict.keys():
        if 'value' in nrg_dict[key]:
            nrg_dict[key]['value'] = np.array(nrg_dict[key]['value'])

    # Extract meta information like filename, directory path, and suffix
    nrg_file = os.path.basename(nrg_filepath)
    nrg_directory = os.path.dirname(nrg_filepath)
    suffix = suffix_from_filename(nrg_file)

    # Append meta information to the main dictionary
    nrg_dict['filename'] = nrg_file
    nrg_dict['filepath'] = nrg_directory
    nrg_dict['suffix'] = suffix

    return nrg_dict


#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


if __name__=="__main__":
    filepath = os.getcwd()



