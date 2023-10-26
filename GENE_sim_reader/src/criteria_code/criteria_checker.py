
import numpy as np




def dict_criteria_check(criteria_dict_list:list, dict_to_check:dict, load_spec:list = ''):

    # This function is called because 'criteria_dict_list' has values in 'dict_to_check' so it either passes True or False

    # Assume True unless it fails a criteria
    add_simulation = True


    for criteria_dict in criteria_dict_list:
        crit_var_name = criteria_dict['variable_name']

        

        dict_to_check_value = dict_to_check.get(crit_var_name, None)

        # skip to next criteria_variable if it is not in the dict_to_check (i.e. "gamma" is not in "parameters_dict")
        if dict_to_check_value == None:
            raise ValueError(f'given input variables {crit_var_name} is not valid.')


        if criteria_dict['logic_op_list'] == None:
            if (crit_var_name in dict_to_check.keys()) and (dict_to_check_value==None):
                # If variable name ('gamma') is in dict ('omega_dict') but 
                return False
            else:
                add_simulation = True
                continue




        # Check for cases where no comparison is needed (i.e. 'gamma', 'n_mag1')
        if criteria_dict['logic_op_list'] == None:


            if (crit_var_name in dict_to_check.keys()) and (dict_to_check_value==None):
                # If variable name ('gamma') is in dict ('omega_dict') but 
                return False
            else:
                add_simulation = True
                continue


        print(crit_var_name, dict_to_check_value)

        
        if isinstance(dict_to_check_value, str):

            if criteria_dict['bounds'] == dict_to_check_value:
                add_simulation = True
            else:
                return False

        elif isinstance(dict_to_check_value, int) or isinstance(dict_to_check_value, float):
            if criteria_checker_float(dict_to_check_value, criteria_dict):
                add_simulation = True
            else:
                return False

        elif isinstance(dict_to_check_value, np.ndarray):
            pass


        else:
            raise ValueError(f'Input "{criteria_dict["bounds"]}" must be either a bound list or string.')







    return add_simulation







def dict_criteria_check_OLD(dict_to_check:dict, criteria_per_dict:dict, dict_name:str):

    add_simulation = True

    print(criteria_per_dict)

    if dict_name in criteria_per_dict.keys():
        criteria_list = criteria_per_dict[dict_name]

        for criteria_dict in criteria_list:

            var_name = criteria_dict['variable_name']
            criteria = criteria_dict['criteria']
            bounds = criteria_dict['bounds']

            if criteria==var_name:
                return add_simulation

            if var_name not in ['time'] or isinstance(bounds, list):                
                for key in list(dict_to_check.keys()):
                    if var_name in key:
                        if not eval(criteria, dict_to_check):
                            add_simulation = False
                            return add_simulation

    return add_simulation









#------------------------------------------------------------------------------------------------
# Function to check a criteria list against a given dict-----------------------------------------
#------------------------------------------------------------------------------------------------

def criteria_checker(input, criteria_dict:dict):

    if isinstance(input, float):
        return criteria_checker_float(input, criteria_dict)
    elif isinstance(input, np.ndarray):
        del_ind = []
        for ind, array_val in enumerate(input):
            if not criteria_checker_float(array_val, criteria_dict):
                del_ind.append(ind)
        
        return del_ind
    else:
        raise ValueError(f'Ensure input value {input} is either a float or numpy array.')








def criteria_checker_float(input_value:float, criteria_dict:dict):

    lower_bound, upper_bound = criteria_dict['bounds']
    op_lower, op_upper = criteria_dict['logic_op_list']

    if lower_bound == float('-inf'):
        lower_condition = True
    else:
        lower_condition = f"({input_value} {op_lower} {lower_bound})"

    if upper_bound == float('inf'):
        upper_condition = True
    else:
        upper_condition = f"({input_value} {op_upper} {upper_bound})"

    condition = f"{lower_condition} and {upper_condition}"
    return eval(condition)
    













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
    # remove criteria that don't have a numerical values (i.e. 'time==last' or 'time==first')
    
    print('before', criteria_dict_list)
    criteria_dict_list = remove_non_numerical_criteria(criteria_dict_list) 
    print('after', criteria_dict_list)


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

            var_in_dict = variable_key in dict_to_check['key_list'] # Check if variable_key is present in dict_to_check
            # THIS causes an issue for nrg dict as it doesn't have Q_ES but Q_ES1
            # Add a feature list to each dict to see if the criteria var is in the feature list instead

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

    # print(ind_crit_pass_list)

    return ind_crit_pass_list






def remove_non_numerical_criteria(criteria_dict_list:list):
    mod_criteria_dict_list = []

    for criteria_dict in criteria_dict_list:
        analysis = criteria_dict['analysis']

        if analysis != 'non-numerical':
            mod_criteria_dict_list.append(criteria_dict)

    return mod_criteria_dict_list