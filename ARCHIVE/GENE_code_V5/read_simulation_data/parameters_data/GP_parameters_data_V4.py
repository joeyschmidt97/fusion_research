#!/usr/bin/env python3

import os
from ParIO import Parameters
import os
os.chdir("..")
from GP_file_functions_V4 import file_checks, FileError


#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT PARAMETER TO DICT-----------------------------------------------------
#------------------------------------------------------------------------------------------------

def parameters_filepath_to_dict(parameters_filepath:str, debug:bool = False):
    """
    Converts a 'parameters' file at a given filepath to a parameter dictionary.
    Returns the parameter dictionary.
    """

    try:
        file_checks(parameters_filepath, filetype='parameters')
        parameters_dict = create_parameters_dict(parameters_filepath)

        return parameters_dict
    except FileError as e:
        print(e)



def create_parameters_dict(parameters_filepath:str):

    # Create a parameter dictionary using the Parameters class
    par = Parameters()
    par.Read_Pars(parameters_filepath)  # Read the parameter file
    parameter_dict = par.pardict 

    # Add the filename, filepath, and suffix to the parameter dictionary
    parameter_dict['filepath'] = parameters_filepath
    parameter_dict['key_list'] = list(parameter_dict.keys())

    return parameter_dict


#------------------------------------------------------------------------------------------------
# -----------------------------------------------------
#------------------------------------------------------------------------------------------------

def species_list(parameters_filepath: str):
    param_dict = parameters_filepath_to_dict(parameters_filepath)
    n_spec = param_dict['n_spec']

    spec_tuple = ()

    for spec_num in range(1, n_spec + 1):
        spec_name = param_dict['name' + str(spec_num)].strip("'")
        spec_tuple += ((spec_name, spec_num),)

    return spec_tuple

#------------------------------------------------------------------------------------------------
# -----------------------------------------------------
#------------------------------------------------------------------------------------------------


if __name__=="__main__":
    filepath = os.getcwd()
