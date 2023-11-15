# import pandas as pd

from src.dict_simulation_data import sim_filepath_to_df


def KBM_dataframe(filepath):

    # filepath = '/pscratch/sd/j/joeschm/NSXTU_discharges/129038/r_0.909990_OM_top/MTM_limit/kymin_0.1/'
    criteria = ['time==last', 'Q_ES', 'Q_EM']

    sim_df = sim_filepath_to_df(filepath_list=filepath, criteria_list=criteria, load_spec='e')

    # Add normalized Q_EM/Q_ES ratio (note if ratio > 0.5 it is electromagnetically dominant)
    Q_EM = sim_df['Q_EM2']
    Q_ES = sim_df['Q_ES2']
    norm_Q_ratio = Q_EM/(Q_EM + Q_ES)
    sim_df['norm_Q_ratio'] = norm_Q_ratio

    

    





