#!/usr/bin/env python3

import os
import numpy as np
from src.utils.file_functions import file_checks, FileError, switch_suffix_file, string_to_list
from src.criteria_code.criteria_checker import criteria_checker
from src.filetype_key_lists import nrg_column_keys, nrg_key_list

from src.dict_parameters_data import create_species_tuple


#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT nrg TO DICT-----------------------------------------------------------
#------------------------------------------------------------------------------------------------

def nrg_filepath_to_dict(nrg_filepath:str, time_criteria='all', nrg_spec='all', nrg_quantities='all'):
    try:
        file_checks(nrg_filepath, filetype='nrg')
        nrg_dict = create_nrg_dict(nrg_filepath, time_criteria, nrg_spec, nrg_quantities)
        
        return nrg_dict
    except FileError as e:
        print(e)




def create_nrg_dict(nrg_filepath:str, time_criteria='all', nrg_spec='all', nrg_quantities='all'):
    # Initializing the nrg dictionary with default values
    nrg_dict = {}

    if time_criteria=='all':
        time_criteria = {'bounds': [float('-inf'), float('inf')], 'logic_op_list': ['>', '<']}

    # Extracting parameters from the corresponding parameters file
    parameter_filepath = switch_suffix_file(nrg_filepath, 'parameters')
    nrg_spec_ind, n_spec = create_species_tuple(parameter_filepath, nrg_spec)

    nrg_quant_ind = nrg_quantity_indices(nrg_quantities)


    for (_ , spec_num) in nrg_spec_ind:
        for (nrg_quantity, _) in nrg_quant_ind:
            nrg_dict[nrg_quantity + str(spec_num)] = []

    

    with open(nrg_filepath, 'r') as nrg_file:
        data = nrg_file.readlines()

        if time_criteria['bounds']=='last':
            data = data[::-1]
            n_spec = 0

        for ind in range(0, len(data), n_spec + 1):
            line = data[ind].strip().split()

            if len(line)==1:
                time = float(line[0])

                if time_criteria['bounds'] in ['last', 'first']:
                    nrg_dict.setdefault('time', []).append(time)
                    # nrg_dict['time'].append(time)
                    nrg_dict = extract_nrg_data(nrg_dict, data, ind, nrg_spec_ind, nrg_quant_ind, time_criteria['bounds'])

                    nrg_dict = nrg_final_checks(nrg_dict, nrg_filepath, nrg_key_list)
                    return nrg_dict
                
                elif criteria_checker(time, time_criteria):
                    nrg_dict.setdefault('time', []).append(time)
                    nrg_dict = extract_nrg_data(nrg_dict, data, ind, nrg_spec_ind, nrg_quant_ind, time_criteria['bounds'])

    nrg_dict = nrg_final_checks(nrg_dict, nrg_filepath, nrg_key_list)
    return nrg_dict                



def nrg_final_checks(nrg_dict:dict, nrg_filepath:str, nrg_key_list:list):

    if 'time' not in nrg_dict.keys():
        return {}
    else:

        for key in nrg_dict.keys():
            if isinstance(nrg_dict[key], list) and key not in ['key_list', 'filepath']:
                try:
                    nrg_dict[key] = np.array(nrg_dict[key])
                except:
                    pass

        nrg_dict['filepath'] = nrg_filepath
        nrg_dict['key_list'] = nrg_key_list

        return nrg_dict

    







def extract_nrg_data(nrg_dict:dict, data:list, ind:int, nrg_spec_ind:list, nrg_quant_ind:list, choose_time):
    
    for ( _ , spec_num) in nrg_spec_ind:
        
        if choose_time == 'last':
            spec_line = data[ind - spec_num].strip().split()
        else:
            spec_line = data[ind + spec_num].strip().split()

        for (quant_name, quant_num) in nrg_quant_ind:   
            nrg_value = float(spec_line[quant_num])
            nrg_dict[quant_name + str(spec_num)].append(nrg_value)

    return nrg_dict





#------------------------------------------------------------------------------------------------
# Helper function to get indices for nrg quantities----------------------------------------
#------------------------------------------------------------------------------------------------

def nrg_quantity_indices(nrg_quantities):

    nrg_quantities = string_to_list(nrg_quantities)

    # Specify which columns and quantities of nrg data are added
    if nrg_quantities == ['all']:
        # all nrg quantities ['n_mag' , 'u_par_mag', 'T_par_mag', 'T_perp_mag', ...]
        nrg_quant_ind = tuple((nrg_quant, nrg_ind) for nrg_ind, nrg_quant in enumerate(nrg_column_keys))
    else:
        invalid_quantities = [q for q in nrg_quantities if q not in nrg_column_keys]
        if invalid_quantities:
            raise ValueError(f'The following nrg quantities are not valid: {invalid_quantities}. Please choose from the following: \n {nrg_column_keys}')
    
        nrg_quant_ind = tuple((nrg_quant, nrg_ind) for nrg_ind, nrg_quant in enumerate(nrg_column_keys) if nrg_quant in nrg_quantities)

    return nrg_quant_ind




if __name__=="__main__":
    filepath = os.getcwd()



