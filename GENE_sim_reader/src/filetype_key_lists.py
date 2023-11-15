

### SIMULATION KEY LIST

simulation_key_list = ['input_directory', 'status', 'suffix']

### OMEGA KEY LIST

omega_key_list = ['gamma','omega']


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
field_column_keys = ['phi', 'apar', 'bpar']
field_key_list = field_extra_keys + field_column_keys






def load_criteria_per_dict(criteria_dict_list: list, param_dict:dict, species_tuple:tuple):
    

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

            if variable_name in nrg_column_keys:
                for (_, spec_num) in species_tuple:
                    new_criteria = crit_dict.copy()

                    # Change 'nrg' to 'nrg1', 'nrg2' depending on species
                    old_var_name = crit_dict['variable_name']
                    new_var_name = crit_dict['variable_name'] + str(spec_num)

                    new_criteria['variable_name'] = crit_dict['variable_name'].replace(old_var_name, new_var_name)
                    new_criteria['criteria'] = crit_dict['criteria'].replace(old_var_name, new_var_name)
                    append_to_load_dict(load_dict_keys, new_criteria, 'nrg')
            else:
                append_to_load_dict(load_dict_keys, crit_dict, 'nrg')
            variable_found = True

        if variable_name in field_key_list:
            append_to_load_dict(load_dict_keys, crit_dict, 'field')
            variable_found = True

        if not variable_found:
            raise ValueError(f'Please ensure "{variable_name}" is a valid name found in one of the GENE filetypes')
        
            # TODO - add user input to ask which filetype keys they want to see (i.e. omega, nrg, etc.) and print these keys




    keys_to_remove = []
    for dict_name in list(load_dict_keys.keys()):
        if dict_name in ['nrg', 'field']:
            criteria_list = load_dict_keys[dict_name]

            for criteria in criteria_list:
                if (len(criteria_list) == 1) and ('time' in criteria['variable_name']):
                    keys_to_remove.append(dict_name)


    
    for key in keys_to_remove:
        del load_dict_keys[key]
    

  
                
    return load_dict_keys




def remove_non_numerical_crit(crit_list:list):

    new_crit_list = []

    for crit in crit_list:
        if crit['bounds'] not in ['first', 'last']:
            new_crit_list.append(crit)

    return new_crit_list 




def time_quantities_from_criteria_list(criteria_dict_list:list, param_dict:dict, dict_type:str):

    time_count = 0
    for crit_dict in criteria_dict_list:
        if crit_dict['variable_name']=='time':
            choose_time = crit_dict
            time_count += 1

    if time_count == 0:
        choose_time = 'all'
    elif time_count > 1:
        raise ValueError(f'Ensure only one time constraint is used.')


    quantity_list = []

    for criteria_dict in criteria_dict_list:
        var_name = criteria_dict['variable_name']

        if (dict_type == 'simulation') and (var_name in simulation_key_list):
            quantity_list.append(var_name)
        
        if (dict_type == 'parameters') and (var_name in param_dict.keys()):
            quantity_list.append(var_name)

        if (dict_type == 'omega') and (var_name in omega_key_list):
            quantity_list.append(var_name)

        if (dict_type == 'nrg'):            
            for nrg_quantity in nrg_column_keys:
                if nrg_quantity in var_name:
                    quantity_list.append(nrg_quantity)
        
        if (dict_type == 'field') and (var_name in field_column_keys):
            quantity_list.append(var_name)

    if quantity_list==[]:
        quantity_list = 'all'

    return choose_time, quantity_list





