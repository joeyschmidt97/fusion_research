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
        - Exampe input_criteria: 
            - 'var(unit)'
            - 'var(unit)<0.4'
            - 'var(unit)<0.4'
    Returns:
        - tuple: A tuple containing the extracted criteria and units.
    """
    # Remove spaces from the input criteria
    input_criteria = input_criteria.replace(' ', '')

    # Error handling
    #------------------------------------------------------------   
    if ("(" in input_criteria) or (")" in input_criteria):

        parenthesis_structure = ''.join(char for char in input_criteria if char in '()')
        parenthesis_mismatch = (parenthesis_structure != '()')

        if not parenthesis_mismatch:
            units = ''.join(input_criteria.split('(')[-1].rsplit(')')[0])
            units_empty = (units=='')

        # TODO: add error checking for cases like 'time(s)dsa'?

        if parenthesis_mismatch or units_empty:
            raise ValueError(f"Please ensure input '{input_criteria}' is written with parentheses as 'variable_name(units)'")
    #------------------------------------------------------------    

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

def range_spliter(input_criteria:str):
    """
    Splits a given criteria string that contains multiple conditions, like '1<var<2' or '1<=var<2' etc.
    Parameters:
        - input_criteria (str): The input criteria string.
    Returns:
        - list: A list containing split criteria.
    """
    # Remove spaces from the input criteria
    input_criteria = input_criteria.replace(' ', '')

    # Check if there are multiple "<" which indicates multiple conditions
    log_op_count = 0
    for log_op in ['<=', '<']:
        log_op_count += input_criteria.count(log_op)


    if log_op_count > 1:    
        # Split the input string into lower and upper bounds
        lower_bound, variable, upper_bound = re.split(r'<=|<', input_criteria)

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
# Function to splits an individual criteria string into a crtieria dict--------------------------
#------------------------------------------------------------------------------------------------

def ind_criteria_parser(criteria: str, units: str):
    """
    Parses an individual criteria string to determine its type (numerical or non-numerical) and extracts relevant information.

    Args:
    criteria (str): The criteria string to be parsed.
    units (str): The units associated with the criteria.

    Returns:
    dict: A dictionary containing the parsed information:
        - 'variable_key': The variable name for dictionary key comparison.
        - 'criteria': The original criteria string.
        - 'units': The units associated with the criteria.
        - 'analysis': The type of analysis (either 'numerical' or 'non-numerical').
                     If there's no criteria, it will be None.
    """
    criteria_dict = {}
    logical_operators = ['<=', '>=', '==', '<', '>']

    if any(op in criteria for op in logical_operators):
        # Split the criteria using logical operators as delimiters
        split_values = re.split(r'(<=|>=|==|<|>)', criteria)
        variable_key = split_values[0]  # Get variable name for dictionary key comparison later
        criteria_comparator = split_values[-1]  # Get value to the right of the logical operator

        # Check if the value to the right of the logical operator is a float (indicating numerical criteria)
        try:
            float(criteria_comparator)
            analysis = 'numerical'
        except:
            analysis = 'non-numerical'
    
    else:
        # If there are no logical operators, the criteria is non-numerical
        variable_key = criteria
        analysis = None

    # Create a dictionary to store the parsed information
    criteria_dict = {'variable_key': variable_key, 'criteria': criteria, 'units': units, 'analysis': analysis}            

    return criteria_dict


#------------------------------------------------------------------------------------------------
# Function to splits a criteria string list into a crtieria dict list----------------------------
#------------------------------------------------------------------------------------------------

def criteria_list_parser(criteria_list:list):
    """
    Generates a list of dictionaries containing the variable, criteria, units, and analysis for each criteria.
    Parameters:
        - criteria_list (list): A list of criteria strings.
    Prints:
        - list: A list of dictionaries for each criteria.
    """
    criteria_dict_list = []

    # Iterate over each criteria in the list
    for criteria_w_units in criteria_list:
        criteria_no_units, units = extract_units_criteria(criteria_w_units)
        # if criteria is of the form 'a < var < b' then split into two lists, otherwise, just put criteria into a list
        criteria_split = range_spliter(criteria_no_units)
        
        # Iterate over each split criteria (if there is a range split)
        for criteria in criteria_split:

            criteria_dict = ind_criteria_parser(criteria, units)            
            criteria_dict_list.append(criteria_dict)

    return criteria_dict_list

