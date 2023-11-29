# import pandas as pd

from GENE_sim_reader.src.dict_simulation_data import sim_filepath_to_df
from GENE_sim_reader.src.utils.file_functions import string_to_list

def growth_freq_dataframe(filepath, input_criteria = ['gamma', 'omega']):

    input_criteria = string_to_list(input_criteria)

    # Check if 'gamma' and 'omega' are in the criteria, if not then add them
    default_vals = ['gamma', 'omega']
    for check_val in default_vals:
        if not any(check_val in criteria for criteria in input_criteria):
            input_criteria.append(check_val)
    
    sim_df = sim_filepath_to_df(filepath_list=filepath, criteria_list=input_criteria)

    return sim_df
    





