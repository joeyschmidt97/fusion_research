



# TODO: implement non-numerical and None removal for criteria and fix up code



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