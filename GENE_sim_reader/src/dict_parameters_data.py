#!/usr/bin/env python3
import os

from src.utils.ParIO import Parameters
from src.utils.file_functions import file_checks, FileError, string_to_list

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

def create_species_tuple(parameters_filepath: str, input_spec_list:list='all'):

    input_spec_list = string_to_list(input_spec_list) # 'i', ['i', 'c'], 'all'

    param_dict = parameters_filepath_to_dict(parameters_filepath)
    n_spec = param_dict['n_spec']

    all_species_tuple = ()
    for spec_num in range(1, n_spec + 1):
        spec_name = param_dict['name' + str(spec_num)].strip("'")
        all_species_tuple += ((spec_name, spec_num),)

    if input_spec_list==['all']:
        return all_species_tuple, n_spec


    output_spec_tuple = ()
    for input_spec_name in input_spec_list:

        input_spec_found = False
        for spec in all_species_tuple:
            if input_spec_name in spec:
                output_spec_tuple += (spec,)
                input_spec_found = True

        if not input_spec_found:
            printout_spec_list = [spec_name for spec_name, _ in all_species_tuple]
            raise ValueError(f'Species "{input_spec_name}" is not a valid species. Please choose from: {printout_spec_list}')


    return output_spec_tuple, n_spec


#------------------------------------------------------------------------------------------------
# -----------------------------------------------------
#------------------------------------------------------------------------------------------------


if __name__=="__main__":
    filepath = os.getcwd()
