#!/usr/bin/env python3


import numpy as np

import os
from src.utils.file_functions import file_checks, FileError, switch_suffix_file
from src.filetype_key_lists import nrg_column_keys, nrg_key_list

# os.chdir("./parameters_data")
from src.dict_parameters_data import create_species_list, parameters_filepath_to_dict

#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT nrg TO DICT-----------------------------------------------------------
#------------------------------------------------------------------------------------------------


def nrg_filepath_to_dict(nrg_filepath:str, choose_time='all', named_spec_row='all', named_nrg_col='all', debug:bool=False):
    """
    Converts a 'nrg' file at a given filepath to an nrg dictionary.
    Returns the nrg dictionary.
    """

    try:
        file_checks(nrg_filepath, filetype='nrg')
        nrg_dict = create_nrg_dict(nrg_filepath, choose_time, named_spec_row, named_nrg_col, debug)

        return nrg_dict
    except FileError as e:
        print(e)



def create_nrg_dict(nrg_filepath:str, choose_time, named_spec_row, named_nrg_col, debug):

    # nrg_filename, nrg_directory, suffix = path_to_name_dir_suffix(nrg_filepath)

    nrg_dict = {
        'filepath': nrg_filepath,
        'key_list': nrg_key_list,
    }

    parameters_filepath = switch_suffix_file(nrg_filepath, 'parameters')
    param_dict = parameters_filepath_to_dict(parameters_filepath)
    n_spec = param_dict['n_spec']

    time_values = time_from_nrg(nrg_filepath, n_spec=n_spec, choose_time=choose_time)

    # Convert spec name and quantity names into coordinates for data retrieval
    spec_row, nrg_col = create_nrg_coordinate_list(nrg_filepath, named_spec_row, named_nrg_col)

    nrg_dict = extract_nrg_data(nrg_dict, time_values, n_spec, spec_row, nrg_col, debug=debug)

    return nrg_dict


#------------------------------------------------------------------------------------------------
# Helper functions to get nrg values at given times----------------------------------------------
#------------------------------------------------------------------------------------------------

def extract_nrg_data(nrg_dict:dict, time_values: list, n_spec:int, spec_row:list, nrg_col:list, debug: bool = False):

    # choose_time is either 'all', 'first', 'last', or [t_i, t_f] where t_i and t_f are the ranges
    nrg_dict = create_nrg_dict_keys(nrg_dict, n_spec, time_values)
    nrg_filepath = nrg_dict['filepath']

    with open(nrg_filepath, 'r') as file:
        data = file.readlines()

    for time in time_values:
        for data_ind, time_line in enumerate(data[::n_spec+1]):
            time_line = time_line.strip().split()
            time_in_nrg = float(time_line[0])

            if time == time_in_nrg:
                add_to_nrg_dict(nrg_dict, data, data_ind, n_spec, spec_row, nrg_col)
                
        # time_checker(nrg_dict, data, time, n_spec, spec_row, nrg_col)

    return nrg_dict

    
def add_to_nrg_dict(nrg_dict:dict, data, data_ind:int, n_spec:int, spec_row:tuple, nrg_col:tuple):

    for (spec_name, spec_num) in spec_row:
        data_row = data_ind*(n_spec + 1) + spec_num
        data_row_list = data[data_row].split()

        for (col_name, data_col) in nrg_col:
            data_value = float(data_row_list[data_col])
            key_name = col_name + str(spec_num)

            nrg_dict[key_name].append(data_value)




def create_nrg_dict_keys(nrg_dict:dict, n_spec:int, time_values: list):

    # Helper function to generate the base structure of the species energy dictionary
    def create_spec_nrg_dict():
        return {
            'n_mag':      [],
            'u_par_mag':  [],
            'T_par_mag':  [],
            'T_perp_mag': [],
            'Gamma_ES':   [],
            'Gamma_EM':   [],
            'Q_ES':       [],
            'Q_EM':       [],
            'Pi_ES':      [],
            'Pi_EM':      []
        }

    # Extract the keys from the base structure for later use
    spec_nrg_keys = list(create_spec_nrg_dict().keys())

    # Initialize the main dictionary to store all data
    nrg_dict['time'] = time_values
    for i in range(n_spec):
        species_number = i + 1
        for key_name in spec_nrg_keys:
            nrg_dict[key_name + str(species_number)] = create_spec_nrg_dict()[key_name]

    return nrg_dict



#------------------------------------------------------------------------------------------------
# Helper functions to get time values from nrg file----------------------------------------------
#------------------------------------------------------------------------------------------------

def time_from_nrg(nrg_filepath:str, n_spec: int, choose_time='all', debug:bool=False):

    with open(nrg_filepath, 'r') as file:
        data = file.readlines()

    time_values = []
    current_row = 0 
    
    if choose_time == 'last':
        data = reversed(data)

    for i, line in enumerate(data):

        if (choose_time in ('first', 'last')) and (len(time_values) > 0):
            # Get the first time value (in case 2 are added), convert to an array, and output
            time_values = [time_values[0]]
            time_values = np.array(time_values)
            return time_values

        line = line.strip().split()

        if len(line) == 1:
            tval = float(line[0])
            append_time_values_in_range(time_values, tval, choose_time)

            # Check that current_row matches n_spec, otherwise raise an error
            if (current_row != n_spec) and (current_row > 0):
                raise ValueError(f"Error: Current row count ({i}) in nrg file does not match n_spec = {n_spec}")

            current_row = 0  # Reset current_row when a new time value is added
        else:
            current_row += 1

    # Convert the time_values list to a NumPy array for better performance
    time_values = np.array(time_values)

    return time_values



def append_time_values_in_range(time_values: list, tval: float, choose_time):
    """
    Appends a time value 'tval' to a list 'time_values' if it falls within a specified time range 'choose_time',
    else it will append all time values
    
    Args:
        time_values (list): A list of time values to which 'tval' may be appended.
        tval (float OR string): The time value to be appended to 'time_values'.
        choose_time: A time range represented as either a list [start_time, end_time]
                     or a single value indicating no time range restrictions.
    
    Returns:
        list: The updated 'time_values' list after potentially appending 'tval'.
    
    Raises:
        ValueError: If 'choose_time' is a list and either of its values is negative,
                    or if the initial time is greater than the final time.
    """
    if isinstance(choose_time, list):
        # Check for negative values in the time range
        if (choose_time[0] < 0) or (choose_time[1] < 0):
            raise ValueError(f"Error: Values in time range cannot be negative. ({choose_time})")
        
        # Check if the initial time is greater than the final time
        if choose_time[0] > choose_time[1]:
            raise ValueError(f"Error: Initial time ({choose_time[0]}) value cannot be greater than final time value ({choose_time[1]})")
        
        # Check if 'tval' is within the specified time range
        if (tval >= choose_time[0]) and (tval <= choose_time[1]):
            time_values.append(tval)
    elif isinstance(choose_time, str):
        # If 'choose_time' is not a list ('all', 'last', or 'first'), append 'tval' without restrictions
        time_values.append(tval)

    return time_values




#------------------------------------------------------------------------------------------------
# Create nrg data extraction coordinates---------------------------------------------------------
#------------------------------------------------------------------------------------------------


def create_nrg_coordinate_list(nrg_filepath:str, named_spec_row = 'all', named_nrg_col = 'all'):

    parameters_filepath = switch_suffix_file(nrg_filepath, 'parameters')
    spec_tuple = create_species_list(parameters_filepath) #get species as [('i', 1), ('e', 2), ('c', 3)] or some variant

    #get nrg_quantity list as [('n_mag', 0), ('u_par_mag', 1), ('T_par_mag', 2), ...] or some variant
    nrg_quantity_tuple = tuple((nrg_key, col) for col, nrg_key in enumerate(nrg_column_keys))

    if named_spec_row == 'all':
        spec_row = spec_tuple
    else:
        spec_row = find_elements_in_tuple(named_spec_row, spec_tuple)

    if named_nrg_col == 'all':
        nrg_col = nrg_quantity_tuple
    else:
        nrg_col = find_elements_in_tuple(named_nrg_col, nrg_quantity_tuple)

    return spec_row, nrg_col


def find_elements_in_tuple(input_list, input_tuple):
    result = []
    for item in input_list:
        found = False
        for tup in input_tuple:
            if item == tup[0]:
                result.append(tup)
                found = True
                break
        if not found:
            item_list = [item[0] for item in input_tuple]
            raise ValueError(f"'{item}' not found in the list of variables: {item_list}")
    return tuple(result)


#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


def time_from_criteria_list(criteria_list:list):

    time_counter = 0

    for criteria_dict in criteria_list:
        var_name = criteria_dict['variable_key']
        if var_name == 'time': time_counter += 1

    if time_counter==0:
        return 'all'
    
    if time_counter==1:
        for criteria_dict in criteria_list:
            var_name = criteria_dict['variable_key']
            criteria = criteria_dict['criteria']

            if var_name=='time':

                if 'first' in criteria:
                    return 'first'
                elif 'last' in criteria:
                    return 'last'
                
                operators = ['==', '<', '=<', '>', '>=']
                for operator in operators:
                    if operator in criteria:
                        time_var, digit_str = criteria.split(operator)
                        digit = float(digit_str.strip())
                        if operator == '==':
                            return [digit, digit]
                        elif operator in ('<', '=<'):
                            return [0, digit]
                        elif operator in ('>', '>='):
                            return [digit, float('inf')]
                
                # Handle other cases or raise an error if needed
                raise ValueError("Unsupported operator in time criteria")

          
          
    
    elif time_counter==2:

        print(time_counter, criteria_list)

        time_slice = []

        return time_slice

    else:
        print("Please ensure you only use 'time' in one criteria set")
        return





def nrg_quantities_from_criteria(criteria_list:list):
    # note this code does not worry about misspellings of nrg col names (it simply skips them)

    nrg_quantities = []
    nrg_full_name_list = ['n_mag', 'u_par_mag', 'T_par_mag', 'T_perp_mag', 'Gamma_ES', 
                     'Gamma_EM', 'Q_ES', 'Q_EM', 'Pi_ES', 'Pi_EM']

    for criteria_dict in criteria_list:
        var_name = criteria_dict['variable_key']

        if var_name in nrg_full_name_list:
            nrg_quantities.append(var_name)

    if nrg_quantities == []:
        nrg_quantities = 'all'

    return nrg_quantities


#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------





if __name__=="__main__":
    filepath = os.getcwd()



