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


    elif (upper_bound in ['True', 'False']) and (log_operator=='=='):
        bool_val = upper_bound == "True"
        return variable_name, bool_val, None


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




