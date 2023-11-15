import os

from src.dict_simulation_data import sim_filepath_to_df
from src.dict_parameters_data import parameters_filepath_to_dict, create_species_tuple



def MTM_dataframe(filepath):

    spec_name = 'e'

    # filepath = '/pscratch/sd/j/joeschm/NSXTU_discharges/129038/r_0.909990_OM_top/MTM_limit/kymin_0.1/'
    criteria = ['time==last', 'Q_ES', 'Q_EM']

    sim_df = sim_filepath_to_df(filepath_list=filepath, criteria_list=criteria, load_spec=spec_name)
    sim_df = get_reference_values(sim_df, spec_name)

    sim_df['coll_dist'] = sim_df['coll'] - sim_df['ref_coll']
    sim_df['beta_dist'] = sim_df['beta'] - sim_df['ref_beta']
    sim_df['omt_dist'] = sim_df['coll'] - sim_df['ref_omt']

    sim_df['euclidean_dist'] = (sim_df['coll_dist']**2 + sim_df['beta_dist']**2 + sim_df['omt_dist']**2)**0.5


    #TODO - dist should be different for kymin=0.1

    # Add normalized Q_EM/Q_ES ratio (note if ratio > 0.5 it is electromagnetically dominant)
    Q_EM = sim_df['Q_EM2']
    Q_ES = sim_df['Q_ES2']
    norm_Q_ratio = Q_EM/(Q_EM + Q_ES)
    sim_df['norm_Q_ratio'] = norm_Q_ratio


    return sim_df
    




def get_reference_values(sim_df, spec_name):

    unique_directories = sim_df['directory'].unique()

    for dir_filepath in unique_directories:
        input_param_filepath = os.path.join(dir_filepath, 'parameters')
        ref_param_dict = parameters_filepath_to_dict(input_param_filepath)

        spec_tuple, _ = sim_df.loc[sim_df['directory'] == dir_filepath, 'species_info'].iloc[0]
        
        for (name, num) in spec_tuple:
            if name==spec_name:
                spec_num = num
                break
            
        # Extract the float values associated with these keys
        ref_coll = extract_value_from_string(ref_param_dict['coll'])
        ref_beta = extract_value_from_string(ref_param_dict['beta'])
        omt_name = 'omt'+ str(spec_num)
        ref_omt = extract_value_from_string(ref_param_dict[omt_name])

        sim_df.loc[sim_df['directory'] == dir_filepath, 'ref_coll'] = ref_coll
        sim_df.loc[sim_df['directory'] == dir_filepath, 'ref_beta'] = ref_beta
        sim_df.loc[sim_df['directory'] == dir_filepath, 'ref_omt'] = ref_omt

    return sim_df




def extract_value_from_string(value_str: str) -> float:
    """
    Extract float value from a string based on the predefined format.
    Args:
    - value_str (str): The input string, e.g., "value=123.45  !scan:123.45*perc(0)"
    Returns:
    - float: Extracted float value from the string.
    """
    # Split the string by '!scan:', take the last part, then split by '*' and take the first part, and finally strip to convert to float
    
    return float(value_str.split('!scan:')[-1].split('*')[0].strip())


















def dist_3D_from_reference_point(kymin_data_points_dict:dict):

    coll_list = kymin_data_points_dict['coll']
    beta_list = kymin_data_points_dict['beta']
    omt_list = kymin_data_points_dict['omt']
    ratio_Q_EM_Q_ES = kymin_data_points_dict['Q_EM/Q_ES']

    rescale_ratio_Q_EM_Q_ES = []
    for ratio_Q in ratio_Q_EM_Q_ES:
        if ratio_Q > 1:
            ratio_Q = 2

        rescale_ratio_Q_EM_Q_ES.append(ratio_Q)

    ratio_Q_EM_Q_ES = rescale_ratio_Q_EM_Q_ES
    
    # Extracting reference point values
    reference_point = kymin_data_points_dict['reference_point']
    ref_coll, ref_beta, ref_omt = reference_point['coll'], reference_point['beta'], reference_point['omt']
        
    # Calculating 3D distances
    distances = []
    for coll, beta, omt in zip(coll_list, beta_list, omt_list):
        distance = ((coll - ref_coll)**2 + (beta - ref_beta)**2 + (omt - ref_omt)**2)**0.5
        distances.append(distance)
    


    # Add distances to dict
    kymin_data_points_dict['3D_distances'] = distances

    return kymin_data_points_dict








