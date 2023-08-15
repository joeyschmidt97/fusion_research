#!/usr/bin/env python3

import os
import sys
import re
import pandas as pd
from GP_file_functions import file_check, suffix_from_filename, string_to_list, find_filetype_files


#------------------------------------------------------------------------------------------------
# COLLECTING OMEGA DATA IF IT MEETS THE CRITERIA SET---------------------------------------------
#------------------------------------------------------------------------------------------------

def filepath_to_omega_dict_list(omega_filepath_list, omega_criteria_list=[]):
    """
    Converts a list of filepaths to omega dictionaries that meet specified criteria.
    Returns a list of omega dictionaries that meet the criteria.
    """
    # Convert the input parameter filepath list and criteria list from strings to lists
    omega_filepath_list = string_to_list(omega_filepath_list)
    omega_criteria_list = string_to_list(omega_criteria_list)

    # Initialize an empty list to store the parameter dictionaries that meet the criteria
    omega_dict_list = []

    # Loop through each parameter filepath in the list
    for omega_filepath in omega_filepath_list:
        # Convert the parameter filepath to a dictionary
        omega_dict = omega_filepath_to_dict(omega_filepath)

        # Check if the omega dictionary meets the criteria
        meets_criteria = all(eval(condition, omega_dict) for condition in omega_criteria_list)
        if meets_criteria or (omega_criteria_list == []):
            # If the parameter dictionary meets the criteria or no criteria were specified, add it to the list
            omega_dict_list.append(omega_dict)
        
    # Return the list of parameter dictionaries that meet the criteria
    return omega_dict_list

#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT OMEGA TO DICT---------------------------------------------------------
#------------------------------------------------------------------------------------------------

def omega_filepath_to_dict(omega_filepath):
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

            omega_dict['kymin'] = {'ky*rho_s': float(items[0])}
            omega_dict['gamma'] = {'cs/a': float(items[1])}
            omega_dict['omega'] = {'cs/a': float(items[2])}
        

        # Add the filename, filepath, and suffix to the omega dictionary
        omega_dict['filename'] = omega_file
        omega_dict['filepath'] = omega_directory
        omega_dict['suffix'] = suffix

        return omega_dict

    else:
        # If the filepath is not a valid 'parameters' file, print an error message and return None
        print('Filepath given is not a omega file, is empty, or is not a file. Filepath:\n', omega_filepath)
        return None

#------------------------------------------------------------------------------------------------
# OUTPUTTING OF DATA ----------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------

def filepath_list_to_omega_df(omega_filepath_list, omega_criteria_list = []):
    """
    Converts a list of filepaths to a pandas DataFrame of omega dictionaries that meet specified criteria.
    Displays the DataFrame in the console.
    """
    # If omega_filepath_list does not contain omega files, search for them up to a maximum depth of 2 directories
    max_depth = 2
    omega_filepath_list = find_filetype_files(omega_filepath_list, 'omega', max_depth)
    
    if len(omega_filepath_list) == 0:
        # If no 'parameters' files are found, print an error message
        print(f"No 'omega' files found at maximum depth of {max_depth} directories down. Try giving a more specific filepath or moving your simulations up directories.")
    else:
        # Convert omega filepath to dict list
        omega_dict_list = filepath_to_omega_dict_list(omega_filepath_list, omega_criteria_list)
        if len(omega_dict_list) == 0:
            # If no omega dictionaries meet the criteria, print an error message
            print(f"No 'omega' files matching the given criteria. Please check criteria again or relax the criteria given.")
        else:
            # Create a pandas DataFrame from the omega dictionary list
            df = pd.DataFrame(omega_dict_list)

            # Convert omega criteria list to only have strings (avoids comprehension reading errors)
            pattern = re.compile(r'^\w+')
            omega_criteria_list = [re.findall(pattern, criteria)[0] for criteria in omega_criteria_list]

            if omega_criteria_list == []:
                # If omega list is empty, show the values that are unique between all

                unique_counts = df.nunique()
                # Select only the columns where the count is greater than 1
                columns_to_show = unique_counts[unique_counts > 1].index.tolist()

                # remove_column_list = []
                # columns_to_show = [col for col in columns_to_show if col not in remove_column_list]

                if len(omega_dict_list) == 1:
                    standard_columns = ['filepath', 'filename', 'suffix']
                    columns_to_show = omega_criteria_list + standard_columns

            else:
                # If omega list is not empty, show only the specified columns
                omega_criteria_list = string_to_list(omega_criteria_list)
                
                standard_columns = ['filepath', 'filename', 'suffix']
                columns_to_show = omega_criteria_list + standard_columns

            # Use the loc accessor to select only the specified columns
            df_subset = df.loc[:, columns_to_show]

            # Display the DataFrame in the console
            print(df_subset)

#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


if __name__=="__main__":
    filepath = os.getcwd()

    filepath_list_to_omega_df(filepath)







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


