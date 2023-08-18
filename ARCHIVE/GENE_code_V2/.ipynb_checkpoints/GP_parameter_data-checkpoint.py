#!/usr/bin/env python3

import os
import sys
import re
import pandas as pd
from GP_file_functions import file_check, suffix_from_filename, string_to_list, find_filetype_files
sys.path.append('/global/homes/j/joeschm/ifs_scripts')
from genetools import Parameters

#------------------------------------------------------------------------------------------------
# COLLECTING PARAMETER DATA IF IT MEETS THE CRITERIA SET-----------------------------------------
#------------------------------------------------------------------------------------------------

def filepath_to_parameter_dict_list(parameter_filepath_list, parameter_criteria_list:list = []):
    """
    Converts a list of filepaths to parameter dictionaries that meet specified criteria.
    Returns a list of parameter dictionaries that meet the criteria.
    """
    # Convert the input parameter filepath list and criteria list from strings to lists
    parameter_filepath_list = string_to_list(parameter_filepath_list)
    parameter_criteria_list = string_to_list(parameter_criteria_list)

    # Initialize an empty list to store the parameter dictionaries that meet the criteria
    parameter_dict_list = []

    # Loop through each parameter filepath in the list
    for parameter_filepath in parameter_filepath_list:
        # Convert the parameter filepath to a dictionary
        parameter_dict = parameter_filepath_to_dict(parameter_filepath)

        # Check if the parameter dictionary meets the criteria
        meets_criteria = all(eval(condition, parameter_dict) for condition in parameter_criteria_list)
        if meets_criteria or (parameter_criteria_list == []):
            # If the parameter dictionary meets the criteria or no criteria were specified, add it to the list
            parameter_dict_list.append(parameter_dict)
        
    # Return the list of parameter dictionaries that meet the criteria
    return parameter_dict_list

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
# OUTPUTTING OF DATA ----------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------

def filepath_list_to_param_df(parameter_filepath_list, parameter_criteria_list = []):
    """
    Converts a list of filepaths to a pandas DataFrame of parameter dictionaries that meet specified criteria.
    Displays the DataFrame in the console.
    """
    #convert filepath and criteria string to list if necessary
    parameter_filepath_list = string_to_list(parameter_filepath_list)
    parameter_criteria_list = string_to_list(parameter_criteria_list)
    
    # If parameter_filepath_list does not contain parameter files, search for them up to a maximum depth of 2 directories
    max_depth = 2
    parameter_filepath_list = find_filetype_files(parameter_filepath_list, 'parameters', max_depth)
    
    
    if len(parameter_filepath_list) == 0:
        # If no 'parameters' files are found, print an error message
        print(f"No 'parameters' files found at maximum depth of {max_depth} directories down. Try giving a more specific filepath or moving your simulations up directories.")
    else:
        # Convert parameter filepath to dict list
        parameter_dict_list = filepath_to_parameter_dict_list(parameter_filepath_list, parameter_criteria_list)
        if len(parameter_dict_list) == 0:
            # If no parameter dictionaries meet the criteria, print an error message
            print(f"No 'parameters' files matching the given criteria. Please check criteria again or relax the criteria given.")
        else:
            # Create a pandas DataFrame from the parameter dictionary list
            df = pd.DataFrame(parameter_dict_list)

            # Convert parameter criteria list to only have strings (avoids comprehension reading errors)
            pattern = re.compile(r'^\w+')
            parameter_criteria_list = [re.findall(pattern, criteria)[0] for criteria in parameter_criteria_list]

            if parameter_criteria_list == []:
                # If parameter list is empty, show the values that are unique between all

                unique_counts = df.nunique()
                # Select only the columns where the count is greater than 1
                columns_to_show = unique_counts[unique_counts > 1].index.tolist()

                remove_column_list = ['step_time', 
                                    'number of computed time steps',
                                    'time for initial value solver',
                                    'init_time']

                columns_to_show = [col for col in columns_to_show if col not in remove_column_list]

                if len(parameter_dict_list) == 1:
                    standard_columns = ['filepath', 'filename', 'suffix']
                    columns_to_show = parameter_criteria_list + standard_columns

            else:
                # If parameter list is not empty, show only the specified columns
                
                standard_columns = ['filepath', 'filename', 'suffix']
                columns_to_show = parameter_criteria_list + standard_columns

            # Use the loc accessor to select only the specified columns
            df_subset = df.loc[:, columns_to_show]

            # Display the DataFrame in the console
            print(df_subset)

#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


if __name__=="__main__":
    filepath = os.getcwd()

    filepath_list_to_param_df(filepath)


