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
    # Check if the filepath is a valid 'omega' file
    check_param = file_check(omega_filepath, 'omega')

    if check_param:
        omega_dict = {}

        # Get the omega filename and directory path
        omega_file = os.path.basename(omega_filepath)
        omega_directory = os.path.dirname(omega_filepath)
        suffix = suffix_from_filename(omega_filepath)
        
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

        # Add the filename, filepath, and suffix to the omega dictionary
        omega_dict['filename'] = omega_file
        omega_dict['filepath'] = omega_directory
        omega_dict['suffix'] = suffix

        return omega_dict

    else:
        # If the filepath is not a valid 'omega' file, print an error message and return None
        if debug:
            print('Filepath given is not a omega file, is empty, or is not a file. Filepath:\n', omega_filepath)
        
        return {}


#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


if __name__=="__main__":
    filepath = os.getcwd()







# def omega_dict_to_Hz(simulation_dict):
#     param_dict = simulation_dict['parameters']
#     omega_dict = simulation_dict['omega']

#     # collect filename and relevant values
#     omega_cs = omega_dict['omega (cs/a)']
#     gamma_cs = omega_dict['gamma (cs/a)']

#     # collect parameter values to convert omega values
#     TJ = param_dict['Tref']      #ion temperature in (J)
#     mi = param_dict['mref']      #ion mass
#     Lf = param_dict['Lref']      #reference length of the device
#     cs = np.sqrt(TJ/mi)              #speed of sound in a plasma 
#     om_ref = cs/Lf                   #reference omega
    
#     # Convert omega and gamma to kHz range
#     omega_dict['omega (kHz)'] = omega_cs*om_ref/1000.0/(2.0*np.pi) #convert omega to kHz
#     omega_dict['gamma (kHz)'] = gamma_cs*om_ref/1000.0/(2.0*np.pi) #convert omega to kHz

#     # Add global kymin values to omega dict
#     omega_dict['n0_global'] = param_dict['n0_global']

#     return simulation_dict


