#!/usr/bin/env python3

import re


#------------------------------------------------------------------------------------------------
# Turn criteria string list into criteria dict list----------------------------------------------
#------------------------------------------------------------------------------------------------


def criteria_list_to_dict_list(criteria_list:list) -> list:
    """
    Generates a list of dictionaries containing the variable, criteria, units, and analysis for each criteria.\n
    Parameters:
        - criteria_list (list): A list of criteria strings.\n
    Prints:
        - list: A list of dictionaries for each criteria.
    """
    criteria_dict_list = []

    # Iterate over each criteria in the list
    for raw_criteria in criteria_list:
        criteria_tuple_list = extract_criteria_values(raw_criteria)

        # Iterate over each split criteria (if there is a range split)
        for criteria_tuple in criteria_tuple_list:

            variable_key, clean_criteria, units, analysis = criteria_tuple

            criteria_dict = {'variable_key': variable_key, 
                             'criteria': clean_criteria, 
                             'units': units, 
                             'analysis': analysis}
            
            criteria_dict_list.append(criteria_dict)

    return criteria_dict_list


#------------------------------------------------------------------------------------------------
# Error handling for improper formatting---------------------------------------------------------
#------------------------------------------------------------------------------------------------


class LogicalOperatorError(Exception):
    def __init__(self, raw_criteria):
        self.message = f"""Please ensure criteria '{raw_criteria}' is written using proper logical operators. Examples are given below:
                         - gamma(kHz) <= 1
                         - 1 < kymin < 10
                         - time == last"""
        super().__init__(self.message)


#------------------------------------------------------------------------------------------------
# Extract key values from criteria for loading into dict-----------------------------------------
#------------------------------------------------------------------------------------------------


def extract_criteria_values(raw_criteria: str) -> list:
    """
    Extracts and parses criteria values from a raw criteria string.
    
    Args:
        raw_criteria (str): The raw criteria string to be parsed.
        
    Returns:
        list: A list of tuples containing parsed criteria values.
              Each tuple has the format (variable, comparison, units, analysis).

    """
    criteria_val_list = []

    criteria = raw_criteria.replace(' ', '') # Remove spaces from the raw criteria string
    split_values = re.split(r'(<=|>=|==|<|>)', criteria) # Split the criteria using logical operators (<=, >=, ==, <, >)

    # Isolate the variable string (with/without) units
    if (len(split_values) == 1) or (len(split_values) == 3):
        variable_w_units = split_values[0]
    elif len(split_values) == 5:
        variable_w_units = split_values[2]
    else:
        raise LogicalOperatorError(raw_criteria) # raise error if not properly formatted
    
    # Extract variable and units from the variable with units
    variable, units = units_from_variable(variable_w_units)
    analysis = get_analysis_type(split_values) # Get the analysis type for criteria (numerical, non-numerical, None)

    # Remove units from criteria if they are present
    if units==None:
        clean_criteria = raw_criteria
    else:
        clean_criteria = raw_criteria.replace('(' + units + ')', "")
    
    # If there is an in between comparisons (a < val < b), split them and add both to the list, else just add criteria info
    if len(split_values) == 5:
        left_comparison, right_comparison = split_comparator_statement(clean_criteria)
        criteria_val_list.append((variable, left_comparison, units, analysis))
        criteria_val_list.append((variable, right_comparison, units, analysis))
    else:
        criteria_val_list.append((variable, clean_criteria, units, analysis))
  
    return criteria_val_list



#------------------------------------------------------------------------------------------------
# Function to determine the type of analysis based on a string with multiple conditions----------
#------------------------------------------------------------------------------------------------

def get_analysis_type(split_values):
    """
    Determine the type of analysis based on the provided list of split values.

    Parameters:
    - split_values (list): A list of values obtained by splitting a string.

    Returns:
    - str: The analysis type, which can be 'numerical' if all values are convertible to floats, 
         'non-numerical' if not all values are convertible to floats, or None if there's no logical operations.
    """
    
    if len(split_values) == 1:
        analysis = None

    elif len(split_values) == 3:
        val1 = split_values[-1]
        try:
            float(val1)
            analysis = 'numerical'
        except:
            analysis = 'non-numerical'

    else:
        val1, val2 = split_values[0], split_values[-1]
        try:
            float(val1)
            float(val2)
            analysis = 'numerical'
        except ValueError:
            raise ValueError(f"Both '{val1}' and '{val2}' must be float convertible (i.e., '3' and '5')")

    return analysis

#------------------------------------------------------------------------------------------------
# Function to extract units from a string with a variable name and optional units in parentheses-
#------------------------------------------------------------------------------------------------

def units_from_variable(variable_w_units: str): 
    """
    Extract the variable name and optional units from a string in the format 'variable_name(units)'.

    Parameters:
    - variable_w_units (str): A string containing a variable name and optional units in parentheses.

    Returns:
    - tuple: A tuple containing the variable name and units. If there are no units, the units will be None.

    """
    if ("(" in variable_w_units) or (")" in variable_w_units):

        parenthesis_structure = ''.join(char for char in variable_w_units if char in '()')
        parenthesis_mismatch = (parenthesis_structure != '()')

        if not parenthesis_mismatch:
            units = ''.join(variable_w_units.split('(')[-1].rsplit(')')[0])
            variable = variable_w_units.split('(')[0]

            units_empty = (units == '')

        if parenthesis_mismatch or units_empty:
            raise ValueError(f"Please ensure input '{variable_w_units}' is written with parentheses as 'variable_name(units)'")
    else:
        units = None
        variable = variable_w_units

    return variable, units


#------------------------------------------------------------------------------------------------
# Function to split string that has multiple conditions------------------------------------------
#------------------------------------------------------------------------------------------------

def split_comparator_statement(input_criteria:str):
    """
    Splits a given criteria string that contains multiple conditions, like '1<var<2' or '1<=var<2' etc.\n
    Parameters:
        - input_criteria (str): The input criteria string.\n
    Returns:
        - list: A tuple containing split criteria.
    """

    # Define regular expression pattern to match comparator statements
    pattern = r'(\d+)\s*([<>]=?)\s*(\w+)\s*([<>]=?)\s*(\d+)'
    
    # Search for matches in the input statement
    match = re.match(pattern, input_criteria)
    
    if match:
        # Extract parts of the statement
        left_operand = match.group(1)
        left_operator = match.group(2)
        variable = match.group(3)
        right_operator = match.group(4)
        right_operand = match.group(5)

        # Ensure lower bound is not greater than upper bound
        if left_operand >= right_operand:
            raise ValueError(f"In criteria '{input_criteria}' ensure lower bound: ({left_operand}) < upper bound: ({right_operand})")
        
        # Switch operators to ensure format (variable LOG_OP value)
        if left_operator=='<':
            mod_left_operator = '>'
        elif left_operator=='<=':
            mod_left_operator = '>='


        # Create two separate strings
        left_comparison = f"{variable}{mod_left_operator}{left_operand}"
        right_comparison = f"{variable}{right_operator}{right_operand}"
        
        return left_comparison, right_comparison
    else:
        raise ValueError(f"Ensure criteria '{input_criteria}' is formatted correctly as 'a < var < b' ")













