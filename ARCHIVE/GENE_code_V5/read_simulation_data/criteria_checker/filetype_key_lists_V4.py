


simulation_key_list = ['input_directory', 
                       'filepath', 
                       'suffix', 
                       'simulation_filepaths', 
                       'status']


omega_key_list = ['kymin',
                  'gamma',
                  'omega']


nrg_key_list = ['time',
                'n_mag' ,
                'u_par_mag',
                'T_par_mag',
                'T_perp_mag',
                'Gamma_ES',
                'Gamma_EM',
                'Q_ES',
                'Q_EM',
                'Pi_ES',
                'Pi_EM']



def load_files_from_criteria(criteria_dict_list: list):
    load_files = []

    for criteria_dict in criteria_dict_list:
        variable_name = criteria_dict['variable_key']

        if (variable_name in omega_key_list) and ('omega' not in load_files):
            load_files.append('omega')
        elif (variable_name in nrg_key_list) and ('nrg' not in load_files):
            load_files.append('nrg')



    return load_files