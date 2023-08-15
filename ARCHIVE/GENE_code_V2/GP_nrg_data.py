#!/usr/bin/env python3

import os
import sys
import re
import pandas as pd
import numpy as np
from GP_file_functions import file_check, suffix_from_filename, string_to_list, find_filetype_files


#------------------------------------------------------------------------------------------------
# COLLECTING NRG DATA IF IT MEETS THE CRITERIA SET-----------------------------------------
#------------------------------------------------------------------------------------------------

def filepath_to_nrg_dict_list(nrg_filepath_list, nrg_criteria_list:list = []):
    """
    Converts a list of filepaths to nrg dictionaries that meet specified criteria.
    Returns a list of nrg dictionaries that meet the criteria.
    """
    # Convert the input nrg filepath list and criteria list from strings to lists
    nrg_filepath_list = string_to_list(nrg_filepath_list)
    nrg_criteria_list = string_to_list(nrg_criteria_list)

    # Initialize an empty list to store the nrg dictionaries that meet the criteria
    nrg_dict_list = []

    # Loop through each nrg filepath in the list
    for nrg_filepath in nrg_filepath_list:
        # Convert the nrg filepath to a dictionary
        nrg_dict = nrg_filepath_to_dict(nrg_filepath)

        # Check if the nrg dictionary meets the criteria
        meets_criteria = all(eval(condition, nrg_dict) for condition in nrg_criteria_list)
        if meets_criteria or (nrg_criteria_list == []):
            # If the nrg dictionary meets the criteria or no criteria were specified, add it to the list
            nrg_dict_list.append(nrg_dict)
        
    # Return the list of nrg dictionaries that meet the criteria
    return nrg_dict_list

#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT nrg TO DICT-----------------------------------------------------
#------------------------------------------------------------------------------------------------





def nrg_filepath_to_dict(nrg_filepath:str, n_spec = 3):
    """
    Converts a 'nrg' file at a given filepath to a nrg dictionary.
    Returns the nrg dictionary.
    """
    # MAKE N_SPEC MORE DYNAMIC


    # Check if the filepath is a valid 'nrgs' file
    check_param = file_check(nrg_filepath, 'nrg')

    if check_param:

        nrg_dict = {'spec_nrg_list': [], 
                    'time':     {'values': np.array([]), 'units': 's'}
                    }
        
        for i in range(n_spec):
            spec_nrg_dict = {'species':    i+1,  
                             'n_mag':      {'values': np.array([]), 'units': 'cs/a'}, 
                             'u_par_mag':  {'values': np.array([]), 'units': 'cs/a'}, 
                             'T_par_mag':  {'values': np.array([]), 'units': 'cs/a'}, 
                             'T_perp_mag': {'values': np.array([]), 'units': 'cs/a'}, 
                             'Gamma_ES':   {'values': np.array([]), 'units': 'cs/a'}, 
                             'Gamma_EM':   {'values': np.array([]), 'units': 'cs/a'}, 
                             'Q_ES':       {'values': np.array([]), 'units': 'cs/a'},
                             'Q_EM':       {'values': np.array([]), 'units': 'cs/a'},
                             'Pi_ES':      {'values': np.array([]), 'units': 'cs/a'},
                             'Pi_EM':      {'values': np.array([]), 'units': 'cs/a'}
                             }
            
            nrg_dict['spec_nrg_list'].append(spec_nrg_dict)

        
        
        # Get the nrg filename and directory path
        nrg_file = os.path.basename(nrg_filepath)
        nrg_directory = os.path.dirname(nrg_filepath)
        suffix = suffix_from_filename(nrg_file)
        
        # Change the current working directory to the nrg directory
        os.chdir(nrg_directory)

        # Read in the nrg file
        with open(nrg_file, 'r') as file:
            lines = file.readlines()

        # Split lines and put values into omega dict
        spec_count = 0

        for line in lines:
            items = line.split()
            # print(items)

            # print(len(items))
            if len(items) == 1:
                time_dict = nrg_dict['time']
                time_dict['values'] = np.append(time_dict['values'], float(items[0]))
                spec_count = 0
            
            else:
                spec_count += 1
                
                for spec_nrg_dict in nrg_dict['spec_nrg_list']:
                    if spec_nrg_dict['species'] == spec_count:

                        spec_nrg_dict['n_mag']['values'] =    np.append(spec_nrg_dict['n_mag']['values'], float(items[0]))
                        spec_nrg_dict['u_par_mag']['values'] = np.append(spec_nrg_dict['u_par_mag']['values'], float(items[1]))
                        spec_nrg_dict['T_par_mag']['values'] = np.append(spec_nrg_dict['T_par_mag']['values'], float(items[2]))
                        spec_nrg_dict['T_perp_mag']['values'] = np.append(spec_nrg_dict['T_perp_mag']['values'], float(items[3]))
                        spec_nrg_dict['Gamma_ES']['values'] = np.append(spec_nrg_dict['Gamma_ES']['values'], float(items[4]))
                        spec_nrg_dict['Gamma_EM']['values'] = np.append(spec_nrg_dict['Gamma_EM']['values'], float(items[5]))
                        spec_nrg_dict['Q_ES']['values'] = np.append(spec_nrg_dict['Q_ES']['values'], float(items[6]))
                        spec_nrg_dict['Q_EM']['values'] = np.append(spec_nrg_dict['Q_EM']['values'], float(items[7]))
                        spec_nrg_dict['Pi_ES']['values'] = np.append(spec_nrg_dict['Pi_ES']['values'], float(items[8]))
                        spec_nrg_dict['Pi_EM']['values'] = np.append(spec_nrg_dict['Pi_EM']['values'], float(items[9]))




        
       

        # Add the filename, filepath, and suffix to the nrg dictionary
        nrg_dict['filename'] = nrg_file
        nrg_dict['filepath'] = nrg_directory
        nrg_dict['suffix'] = suffix

        return nrg_dict

    else:
        # If the filepath is not a valid 'nrg' file, print an error message and return None
        print('Filepath given is not a nrg file, is empty, or is not a file. Filepath:\n', nrg_filepath)
        return None








#------------------------------------------------------------------------------------------------
# OUTPUTTING OF DATA ----------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------

def filepath_list_to_nrg_df(nrg_filepath_list, nrg_criteria_list = []):
    """
    Converts a list of filepaths to a pandas DataFrame of nrg dictionaries that meet specified criteria.
    Displays the DataFrame in the console.
    """
    #convert filepath and criteria string to list if necessary
    nrg_filepath_list = string_to_list(nrg_filepath_list)
    nrg_criteria_list = string_to_list(nrg_criteria_list)
    
    # If nrg_filepath_list does not contain nrg files, search for them up to a maximum depth of 2 directories
    max_depth = 2
    nrg_filepath_list = find_filetype_files(nrg_filepath_list, 'nrg', max_depth)
    
    
    if len(nrg_filepath_list) == 0:
        # If no 'nrg' files are found, print an error message
        print(f"No 'nrg' files found at maximum depth of {max_depth} directories down. Try giving a more specific filepath or moving your simulations up directories.")
    else:
        # Convert nrg filepath to dict list
        nrg_dict_list = filepath_to_nrg_dict_list(nrg_filepath_list, nrg_criteria_list)
        if len(nrg_dict_list) == 0:
            # If no nrg dictionaries meet the criteria, print an error message
            print(f"No 'nrg' files matching the given criteria. Please check criteria again or relax the criteria given.")
        else:
            # Create a pandas DataFrame from the nrg dictionary list
            df = pd.DataFrame(nrg_dict_list)

            # Convert nrg criteria list to only have strings (avoids comprehension reading errors)
            pattern = re.compile(r'^\w+')
            nrg_criteria_list = [re.findall(pattern, criteria)[0] for criteria in nrg_criteria_list]

            if nrg_criteria_list == []:
                # If nrg list is empty, show the values that are unique between all

                unique_counts = df.nunique()
                # Select only the columns where the count is greater than 1
                columns_to_show = unique_counts[unique_counts > 1].index.tolist()

                remove_column_list = ['step_time', 
                                    'number of computed time steps',
                                    'time for initial value solver',
                                    'init_time']

                columns_to_show = [col for col in columns_to_show if col not in remove_column_list]

                if len(nrg_dict_list) == 1:
                    standard_columns = ['filepath', 'filename', 'suffix']
                    columns_to_show = nrg_criteria_list + standard_columns

            else:
                # If nrg list is not empty, show only the specified columns
                
                standard_columns = ['filepath', 'filename', 'suffix']
                columns_to_show = nrg_criteria_list + standard_columns

            # Use the loc accessor to select only the specified columns
            df_subset = df.loc[:, columns_to_show]

            # Display the DataFrame in the console
            print(df_subset)

#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


if __name__=="__main__":
    filepath = os.getcwd()

    filepath_list_to_nrg_df(filepath)


