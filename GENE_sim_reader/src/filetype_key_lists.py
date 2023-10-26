

### SIMULATION KEY LIST

simulation_key_list = ['input_directory', 
                       'filepath',
                       'simulation_filepaths', 
                       'status']

### OMEGA KEY LIST

omega_key_list = ['gamma',
                  'omega']


### NRG KEY LIST

nrg_extra_keys = ['time']

nrg_column_keys = ['n_mag' ,
                'u_par_mag',
                'T_par_mag',
                'T_perp_mag',
                'Gamma_ES',
                'Gamma_EM',
                'Q_ES',
                'Q_EM',
                'Pi_ES',
                'Pi_EM']

nrg_key_list = nrg_extra_keys + nrg_column_keys

### FIELD KEY LIST

field_extra_keys = ['time']

field_column_keys = ['phi',
                     'apar',
                     'bpar']

field_key_list = field_extra_keys + field_column_keys








def load_criteria_per_dict(criteria_dict_list: list, param_dict:dict):
    
    def append_to_load_dict(load_dict_keys:dict, crit_dict:dict, dict_name:str):
        if dict_name not in load_dict_keys:
            load_dict_keys[dict_name] = []
        load_dict_keys[dict_name].append(crit_dict)

    load_dict_keys = {}

    for crit_dict in criteria_dict_list:
        variable_name = crit_dict['variable_name']
        variable_found = False
        # print(variable_name)
        
        if variable_name in simulation_key_list:
            append_to_load_dict(load_dict_keys, crit_dict, 'simulation')
            variable_found = True
        if variable_name in param_dict.keys():
            append_to_load_dict(load_dict_keys, crit_dict, 'parameters')
            variable_found = True
        if variable_name in omega_key_list:
            append_to_load_dict(load_dict_keys, crit_dict, 'omega')
            variable_found = True
        if variable_name in nrg_key_list:
            append_to_load_dict(load_dict_keys, crit_dict, 'nrg')
            variable_found = True
        if variable_name in field_key_list:
            append_to_load_dict(load_dict_keys, crit_dict, 'field')
            variable_found = True

        if not variable_found:
            raise ValueError(f'Please ensure "{variable_name}" is a valid name found in one of the GENE filetypes')
        
            # TODO - add user input to ask which filetype keys they want to see (i.e. omega, nrg, etc.) and print these keys

    return load_dict_keys







def time_quantities_from_criteria_list(criteria_dict_list:list, param_dict:dict, dict_type:str):

    time_count = 0
    for crit_dict in criteria_dict_list:
        if crit_dict['variable_name']=='time':
            choose_time = crit_dict
            time_count += 1

    if time_count > 1:
        raise ValueError(f'Ensure only one time constraint is used.')


    quantity_list = []

    for criteria_dict in criteria_dict_list:
        var_name = criteria_dict['variable_key']

        if (dict_type == 'simulation') and (var_name in simulation_key_list):
            quantity_list.append(var_name)
        
        if (dict_type == 'parameters') and (var_name in param_dict.keys()):
            quantity_list.append(var_name)

        if (dict_type == 'omega') and (var_name in omega_key_list):
            quantity_list.append(var_name)

        if (dict_type == 'nrg') and (var_name in nrg_column_keys):
            quantity_list.append(var_name)
        
        if (dict_type == 'field') and (var_name in field_column_keys):
            quantity_list.append(var_name)

    

    return choose_time, quantity_list







# def nrg_quantities_from_criteria(criteria_list:list):
#     # note this code does not worry about misspellings of nrg col names (it simply skips them)

#     nrg_quantities = []
#     nrg_full_name_list = ['n_mag', 'u_par_mag', 'T_par_mag', 'T_perp_mag', 'Gamma_ES', 
#                      'Gamma_EM', 'Q_ES', 'Q_EM', 'Pi_ES', 'Pi_EM']

#     for criteria_dict in criteria_list:
#         var_name = criteria_dict['variable_key']

#         if var_name in nrg_full_name_list:
#             nrg_quantities.append(var_name)

#     if nrg_quantities == []:
#         nrg_quantities = 'all'

#     return nrg_quantities

