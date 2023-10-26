#!/usr/bin/env python3

import os
import sys
from GP_file_functions_V3 import file_check, suffix_from_filename, string_to_list, find_filetype_files
sys.path.append('/global/homes/j/joeschm/ifs_scripts')
from ParIO import Parameters

#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT PARAMETER TO DICT-----------------------------------------------------
#------------------------------------------------------------------------------------------------

def parameter_filepath_to_dict(parameter_filepath:str):
    """
    Converts a 'parameters' file at a given filepath to a parameter dictionary.
    Returns the parameter dictionary.
    """
    # Check if the filepath is a valid 'parameters' file
    check_param = file_check(parameter_filepath, 'parameters')

    if check_param:
        # Get the parameter filename and directory path
        parameter_file = os.path.basename(parameter_filepath)
        parameter_directory = os.path.dirname(parameter_filepath)
        suffix = suffix_from_filename(parameter_file)
        
        # Change the current working directory to the parameter directory
        os.chdir(parameter_directory)

        # Create a parameter dictionary using the Parameters class
        par = Parameters()
        par.Read_Pars(parameter_file)  # Read the parameter file
        parameter_dict = par.pardict 

        # Add the filename, filepath, and suffix to the parameter dictionary
        parameter_dict['filename'] = parameter_file
        parameter_dict['filepath'] = parameter_directory
        parameter_dict['suffix'] = suffix

        return parameter_dict

    else:
        # If the filepath is not a valid 'parameters' file, print an error message and return None
        print('Filepath given is not a parameter file, is empty, or is not a file. Filepath:\n', parameter_filepath)
        return None


#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT PARAMETER TO DICT-----------------------------------------------------
#------------------------------------------------------------------------------------------------

def species_name_to_number(parameters_dict:dict, species_name:str):

    GENE_spec_label = []  # To store species labels present in the GENE parameters
    found = False  # Flag to check if the desired key was found

    # Loop through all species specified in the GENE parameters
    for i in range(parameters_dict['n_spec']):
        species_number = i + 1  # Adjust for 1-based indexing
        spec_name = 'name' + str(species_number)  # Construct the species name key (e.g., "name1", "name2", ...)
        current_species_name = parameters_dict[spec_name].strip("'")  # Get the species name from parameters and strip any surrounding single quotes

        # Add the current species name to the GENE_spec_label list
        GENE_spec_label.append(current_species_name)
        
        # Check if the current species name matches the target species name
        if current_species_name == species_name.strip("'"):
            return species_number

    # If the desired key wasn't found, display an error message and print available species labels
    if not found:
        print(f'No such key {species_name} could be found. Check you have the right variable name and species label used in the GENE parameters file.')
        print('GENE species labels:', GENE_spec_label)




#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


if __name__=="__main__":
    filepath = os.getcwd()
