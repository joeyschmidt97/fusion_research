#!/usr/bin/env python3

import re


#------------------------------------------------------------------------------------------------
# Turn criteria string list into criteria dict list----------------------------------------------
#------------------------------------------------------------------------------------------------

def multi_criteria_to_list(criteria_list:list) -> list:
    criteria_dict_list = []

    if isinstance(criteria_list,str):
        criteria_dict = criteria_parser(criteria_list)
        criteria_dict_list.append(criteria_dict)
    
    elif isinstance(criteria_list,list):
        for raw_criteria in criteria_list:
            criteria_dict = criteria_parser(raw_criteria)
            criteria_dict_list.append(criteria_dict)
    else:
        raise ValueError('Ensure criteria is either a string or list of criteria')

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

def criteria_parser(raw_criteria: str) -> dict:
    criteria_dict = {}

    criteria = raw_criteria.replace(' ', '') # Remove spaces from the raw criteria string
    unitless_criteria, units = parse_units_from_criteria(criteria)

    split_values = re.split(r'(<=|>=|==|<|>)', unitless_criteria) # Split the criteria using logical operators (<=, >=, ==, <, >)

    if len(split_values) == 1:
        # "gamma", "omega", "n_mag"
        variable_name = split_values[0]
        bounds = None
        logic_op_list = None

    elif len(split_values) == 3:
        # "gamma <= 3", "time == last"
        variable_name, bounds, logic_op_list = single_logical_operator(split_values, raw_criteria)
            
    elif len(split_values) == 5:
        # "1 < omega < 2"
        variable_name, bounds, logic_op_list = double_logical_operator(split_values, raw_criteria)
        
    else:
        raise LogicalOperatorError(raw_criteria) # raise error if not properly formatted
    
    criteria_dict['criteria'] = unitless_criteria
    criteria_dict['variable_name'] = variable_name
    criteria_dict['units'] = units
    criteria_dict['bounds'] = bounds
    criteria_dict['logic_op_list'] = logic_op_list

    return criteria_dict




def parse_units_from_criteria(criteria_string:str) -> tuple:
    start_index = criteria_string.find('(')
    end_index = criteria_string.find(')')
    
    if start_index != -1 and end_index != -1:
        units = criteria_string[start_index + 1:end_index]
        unitless_criteria = criteria_string[:start_index] + criteria_string[end_index + 1:]

        unitless_criteria = unitless_criteria.replace(' ', '')
        units = units.replace(' ', '')

        return unitless_criteria, units
    else:
        criteria_string = criteria_string.replace(' ', '')
        return criteria_string, None





def is_float_convertible(value) -> bool:
    try:
        _ = float(value)
        return True
    except ValueError:
        return False


def single_logical_operator(split_values:list, raw_criteria:str) -> tuple:
    variable_name, log_operator, upper_bound = split_values

    if variable_name == 'suffix':
        pattern = re.compile(r'^\d{4}$')
        if log_operator=='==' and bool(pattern.match(upper_bound)):
            return variable_name, upper_bound, None
        else:
            raise ValueError(f'Ensure "{raw_criteria}" is written in the form "suffix==0001".')




    elif (variable_name=='time') and (upper_bound in ['last', 'first']):
        if log_operator=='==':
            return variable_name, upper_bound, None
        else:
            raise ValueError(f'Ensure "{raw_criteria}" is written in the form "time==last" or "time==first".')

    elif not is_float_convertible(upper_bound) and log_operator=='==':
        return variable_name, upper_bound, None

    elif is_float_convertible(upper_bound):
        upper_bound = float(upper_bound)
                
        if log_operator in ['<=', '<']: 
            # time<=3 -> [time>-inf, time<=3] -> [-inf,3], ['>', '<=']
            bounds = [float('-inf'), upper_bound]
            logic_op_list = ['>', log_operator]

        elif log_operator in ['>=', '>']:   
            # time>10 -> [time>10, time<inf] -> [10, inf], ['>', '<']
            bounds = [upper_bound, float('inf')]
            logic_op_list = [log_operator, '<']

        elif log_operator in ['==']: 
            # time==4 -> [time>=4, time<=4] 
            bounds = [upper_bound, upper_bound]
            logic_op_list = ['>=', '<=']
        
        return variable_name, bounds, logic_op_list
    
    else:
        raise LogicalOperatorError(raw_criteria)





def double_logical_operator(split_values:list, raw_criteria:str):
        
    lower_bound, lower_log_operator, variable_name, upper_log_operator, upper_bound = split_values

    if is_float_convertible(upper_bound) and is_float_convertible(lower_bound):
        upper_bound = float(upper_bound)
        lower_bound = float(lower_bound)
    else:    
        raise ValueError(f'Ensure "{upper_bound}" and "{lower_bound}" in "{raw_criteria}" are numerical values (i.e. "5", "3.14", "20")')
    
    if lower_bound >= upper_bound:
        raise ValueError(f"In criteria '{raw_criteria}' ensure lower bound: ({lower_bound}) < upper bound: ({upper_bound})")

    bounds = [lower_bound, upper_bound]

    if lower_log_operator=='<':
        logic_op_list = ['>', upper_log_operator]
    elif lower_log_operator=='<=':
        logic_op_list = ['>=', upper_log_operator]


    return variable_name, bounds, logic_op_list













































# def extract_criteria_values(raw_criteria: str) -> list:
#     """
#     Extracts and parses criteria values from a raw criteria string.
    
#     Args:
#         raw_criteria (str): The raw criteria string to be parsed.
        
#     Returns:
#         list: A list of tuples containing parsed criteria values.
#               Each tuple has the format (variable, comparison, units, analysis).

#     """
#     criteria_val_list = []

#     criteria = raw_criteria.replace(' ', '') # Remove spaces from the raw criteria string
#     split_values = re.split(r'(<=|>=|==|<|>)', criteria) # Split the criteria using logical operators (<=, >=, ==, <, >)

#     # Isolate the variable string (with/without) units
#     if (len(split_values) == 1) or (len(split_values) == 3):
#         variable_w_units = split_values[0]
#     elif len(split_values) == 5:
#         variable_w_units = split_values[2]
#     else:
#         raise LogicalOperatorError(raw_criteria) # raise error if not properly formatted
    
#     # Extract variable and units from the variable with units
#     variable, units = units_from_variable(variable_w_units)
#     analysis = get_analysis_type(split_values) # Get the analysis type for criteria (numerical, non-numerical, None)

#     # Remove units from criteria if they are present
#     if units==None:
#         clean_criteria = raw_criteria
#     else:
#         clean_criteria = raw_criteria.replace('(' + units + ')', "")
    
#     # If there is an in between comparisons (a < val < b), split them and add both to the list, else just add criteria info
#     if len(split_values) == 5:
#         left_comparison, right_comparison = split_comparator_statement(clean_criteria)
#         criteria_val_list.append((variable, left_comparison, units, analysis))
#         criteria_val_list.append((variable, right_comparison, units, analysis))
#     else:
#         criteria_val_list.append((variable, clean_criteria, units, analysis))
  
#     return criteria_val_list



# #------------------------------------------------------------------------------------------------
# # Function to determine the type of analysis based on a string with multiple conditions----------
# #------------------------------------------------------------------------------------------------

# def get_analysis_type(split_values):
#     """
#     Determine the type of analysis based on the provided list of split values.

#     Parameters:
#     - split_values (list): A list of values obtained by splitting a string.

#     Returns:
#     - str: The analysis type, which can be 'numerical' if all values are convertible to floats, 
#          'non-numerical' if not all values are convertible to floats, or None if there's no logical operations.
#     """
    
#     if len(split_values) == 1:
#         analysis = None

#     elif len(split_values) == 3:
#         val1 = split_values[-1]
#         try:
#             float(val1)
#             analysis = 'numerical'
#         except:
#             analysis = None

#     else:
#         val1, val2 = split_values[0], split_values[-1]
#         try:
#             float(val1)
#             float(val2)
#             analysis = 'numerical'
#         except ValueError:
#             raise ValueError(f"Both '{val1}' and '{val2}' must be float convertible (i.e., '3.2' and '5')")

#     return analysis

















# #------------------------------------------------------------------------------------------------
# # Function to extract units from a string with a variable name and optional units in parentheses-
# #------------------------------------------------------------------------------------------------

# def units_from_variable(variable_w_units: str): 
#     """
#     Extract the variable name and optional units from a string in the format 'variable_name(units)'.

#     Parameters:
#     - variable_w_units (str): A string containing a variable name and optional units in parentheses.

#     Returns:
#     - tuple: A tuple containing the variable name and units. If there are no units, the units will be None.

#     """
#     if ("(" in variable_w_units) or (")" in variable_w_units):

#         parenthesis_structure = ''.join(char for char in variable_w_units if char in '()')
#         parenthesis_mismatch = (parenthesis_structure != '()')

#         if not parenthesis_mismatch:
#             units = ''.join(variable_w_units.split('(')[-1].rsplit(')')[0])
#             variable = variable_w_units.split('(')[0]

#             units = units.replace(' ', '')
#             variable = variable.replace(' ', '')
            
#             units_empty = (units == '')

#         if parenthesis_mismatch or units_empty:
#             raise ValueError(f"Please ensure input '{variable_w_units}' is written with parentheses as 'variable_name(units)'")
#     else:
#         units = None
#         variable = variable_w_units.replace(' ', '')
    
#     return variable, units


# #------------------------------------------------------------------------------------------------
# # Function to split string that has multiple conditions------------------------------------------
# #------------------------------------------------------------------------------------------------

# def split_comparator_statement(input_criteria:str):
#     """
#     Splits a given criteria string that contains multiple conditions, like '1<var<2' or '1<=var<2' etc.\n
#     Parameters:
#         - input_criteria (str): The input criteria string.\n
#     Returns:
#         - list: A tuple containing split criteria.
#     """

#     # Define regular expression pattern to match comparator statements
#     # pattern = r'(\d+)\s*([<>]=?)\s*(\w+)\s*([<>]=?)\s*(\d+)'  # doesn't work with floats
#     pattern = r'(\d*\.\d+|\d+)\s*([<>]=?)\s*(\w+)\s*([<>]=?)\s*(\d*\.\d+|\d+)'

    
#     # Search for matches in the input statement
#     match = re.match(pattern, input_criteria)
    
#     if match:
#         # Extract parts of the statement
#         left_operand = match.group(1)
#         left_operator = match.group(2)
#         variable = match.group(3)
#         right_operator = match.group(4)
#         right_operand = match.group(5)

#         # Ensure lower bound is not greater than upper bound
#         if left_operand >= right_operand:
#             raise ValueError(f"In criteria '{input_criteria}' ensure lower bound: ({left_operand}) < upper bound: ({right_operand})")
        
#         # Switch operators to ensure format (variable LOG_OP value)
#         if left_operator=='<':
#             mod_left_operator = '>'
#         elif left_operator=='<=':
#             mod_left_operator = '>='


#         # Create two separate strings
#         left_comparison = f"{variable}{mod_left_operator}{left_operand}"
#         right_comparison = f"{variable}{right_operator}{right_operand}"
        
#         return left_comparison, right_comparison
#     else:
#         raise ValueError(f"Ensure criteria '{input_criteria}' is formatted correctly as 'a < var < b' ")













