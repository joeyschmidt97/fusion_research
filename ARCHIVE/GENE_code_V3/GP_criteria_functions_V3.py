#!/usr/bin/env python3

import re

#------------------------------------------------------------------------------------------------
# Function to extract units from given criteria--------------------------------------------------
#------------------------------------------------------------------------------------------------

def extract_units_criteria(input_criteria:str):
    """
    Extracts the units and criteria from a given input string.
    Parameters:
        - input_criteria (str): The input string containing criteria and possibly units.
    Returns:
        - tuple: A tuple containing the extracted criteria and units.
    """
    # Remove spaces from the input criteria
    input_criteria = input_criteria.replace(' ', '')
    
    # Check if input criteria contains parenthesis which indicates units
    if ("(" or ")") in input_criteria:
        # Split the string into the criteria part and the units part
        criteria_L, units_R = input_criteria.split("(")
        units, criteria_R = units_R.split(")")
        criteria = criteria_L + criteria_R
    else:
        criteria = input_criteria
        units = None
        
    return criteria, units

#------------------------------------------------------------------------------------------------
# Function to split string that has multiple conditions------------------------------------------
#------------------------------------------------------------------------------------------------

def criteria_spliter(input_criteria:str):
    """
    Splits a given criteria string that contains multiple conditions.
    Parameters:
        - input_criteria (str): The input criteria string.
    Returns:
        - list: A list containing split criteria.
    """
    # Check if there are multiple "<" which indicates multiple conditions
    if input_criteria.count('<') > 1:    
        # Split the input string into lower and upper bounds
        lower_bound, variable, upper_bound = input_criteria.split("<")

        # Remove any leading or trailing whitespace
        lower_bound = lower_bound.strip()
        variable = variable.strip()
        upper_bound = upper_bound.strip()

        # Create the list of split strings
        split_list = [f"{variable}>{lower_bound}", f"{variable}<{upper_bound}"]

    else:
        split_list = [input_criteria]
        
    return split_list

#------------------------------------------------------------------------------------------------
# Function to splits a criteria string list into a crtieria dict list----------------------------
#------------------------------------------------------------------------------------------------

def criteria_parser(criteria_list):
    """
    Generates a list of dictionaries containing the variable, criteria, and units for each criteria.
    Parameters:
        - criteria_list (list): A list of criteria strings.
    Prints:
        - list: A list of dictionaries for each criteria.
    """
    criteria_dict_list = []
    
    # Iterate over each criteria in the list
    for criteria_w_units in criteria_list:
        criteria_no_units, units = extract_units_criteria(criteria_w_units)
        criteria_split = criteria_spliter(criteria_no_units)
        
        # Iterate over each split criteria
        for criteria in criteria_split:
            
            # If any criteria contains logical operators then extract the variable
            if any(op in criteria for op in ['<=', '>=', '==', '<', '>']):
                split_values = re.split(r'(<=|>=|==|<|>)', criteria)
                variable_key = split_values[0]    
                criteria_dict = {'variable_key': variable_key, 'criteria': criteria, 'units': units}     
            # Otherwise, there is no criteria
            else:
                variable_key = criteria
                criteria_dict = {'variable_key': variable_key, 'criteria': None, 'units': units}            
            
            criteria_dict_list.append(criteria_dict)

    return criteria_dict_list

#------------------------------------------------------------------------------------------------
# Function to check a criteria list against a given dict-----------------------------------------
#------------------------------------------------------------------------------------------------

def criteria_dict_checker(criteria_dict_list:list, global_crit_check:list, dict_to_check:dict, debug = False):
    """
    Evaluate a list of criteria against a given dictionary.
    
    This function checks if the criteria specified in `criteria_dict_list` are met
    in the `dict_to_check`. It takes into account previous global criteria checks to avoid
    redundant evaluations.

    Parameters:
    - criteria_dict_list (list): List of dictionaries where each dictionary represents a criterion. 
                                Each criterion dictionary has keys 'variable_key', 'units', and 'criteria'.
    - global_crit_check (list): A list of boolean values indicating if a global criterion has already been satisfied.
    - dict_to_check (dict): Dictionary to check against the criteria.
    - debug (bool): A flag for printing debug information. Default is False.

    Returns:
    - list: A list of boolean values indicating if each criteria is met or not.
    """

    # List to store if each criterion passes or fails.
    ind_crit_pass_list = []

    # Iterate over each criterion
    for i, criterion_dict in enumerate(criteria_dict_list):
        
        # If the criteria has already been satisfied by another dict skip the criteria check
        if global_crit_check[i] == True:
            ind_crit_pass_list.append(0)
        else:
            # Extract parts of the criterion dictionary
            variable_key = criterion_dict['variable_key']
            units = criterion_dict['units']
            criteria = criterion_dict['criteria']

            var_in_dict = variable_key in dict_to_check # Check if variable_key is present in dict_to_check
            unitless = (units == None)  # Check if criterion doesn't have units
            criterion_is_variable = (criteria == None)  # Check if criterion is not set

            # Evaluate if variable_key is present in the dictionary
            if var_in_dict:
                # If the criterion does not have units associated
                if unitless:
                    # If there is no specific criteria, then it's automatically satisfied
                    if criterion_is_variable:
                        ind_crit_pass_list.append(True)

                        if debug: print(variable_key, '==', variable_key, '// units:', units)
                    # Evaluate the criterion against the dict_to_check
                    else:
                        ind_crit_pass_list.append(eval(criteria, dict_to_check))
                        
                        if debug: print(criteria, '//', variable_key, '=', dict_to_check[variable_key], '// units:', units)
                # If the criterion has units
                else:
                    if criterion_is_variable:
                        # TODO: Convert variable_key to specific units

                        ind_crit_pass_list.append(False)

                        if debug: print(variable_key, '==', variable_key, '// units:', units)
                    else:
                        # TODO: Convert variable_key to specific units and evaluate
                        # Placeholder for the conversion function and evaluation

                        if debug: print('still need to do units conversions checking', units, '//', criteria, '//', variable_key, '=', dict_to_check[variable_key])
                        
                        # ind_crit_pass_list.append(eval(criteria, dict_to_check))
                        ind_crit_pass_list.append(False)
            # If variable_key is not present in dict_to_check, return False
            else: 
                ind_crit_pass_list.append(False)

    return ind_crit_pass_list


