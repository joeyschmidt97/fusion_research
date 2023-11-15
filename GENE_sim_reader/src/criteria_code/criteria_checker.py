
import numpy as np




def dict_criteria_check(criteria_dict_list:list, dict_to_check:dict):

    if dict_to_check == {}:
        return False


    # Assume True unless it fails a criteria
    add_simulation = True


    for criteria_dict in criteria_dict_list:
        crit_var_name = criteria_dict['variable_name']

        if crit_var_name == criteria_dict['criteria']:
            add_simulation = True
            continue

        dict_to_check_value = dict_to_check.get(crit_var_name, None)
  

        if isinstance(dict_to_check_value, type(None)):
            raise ValueError(f'given input variable "{crit_var_name}" is not valid.')


        elif isinstance(dict_to_check_value, bool):
            if bool(criteria_dict['bounds']) == dict_to_check_value:
                add_simulation = True
            else:
                return False


        elif isinstance(dict_to_check_value, str):

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

            del_ind = criteria_checker(dict_to_check_value, criteria_dict)
            if del_ind == []:
                add_simulation = True
            else:
                return False



    return add_simulation





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
    




def criteria_array_sifter(criteria_dict_list:list, dict_to_sift:dict):

    for criteria_dict in criteria_dict_list:
        crit_var_name = criteria_dict['variable_name']

        if crit_var_name == criteria_dict['criteria']:
            continue

        dict_to_check_value = dict_to_sift.get(crit_var_name, None)

        if isinstance(dict_to_check_value,type(None)):
            raise(f'Variable "{crit_var_name}" is not in the given dict.')

        del_ind = criteria_checker(dict_to_check_value, criteria_dict)

        # Use np.delete to remove values at specified indices
        for key in dict_to_sift.keys():
            if isinstance(dict_to_sift[key], np.ndarray):
                dict_to_sift[key] = np.delete(dict_to_sift[key], del_ind)

                if len(dict_to_sift[key])==0:
                    return {}

    

    return dict_to_sift