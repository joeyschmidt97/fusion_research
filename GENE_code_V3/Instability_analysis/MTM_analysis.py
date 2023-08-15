#!/usr/bin/env python3

import sys
sys.path.insert(1, '/global/u1/j/joeschm/fusion_research/GENE_code_V3')
from GP_simulation_data_V3 import filepath_to_simulation_dict_list


def dsa():
    return



#------------------------------------------------------------------------------------------------
# BASE FUNCTION TO CONVERT filepath list TO simulation dict list---------------------------------
#------------------------------------------------------------------------------------------------


def collect_kymin_list(filepath_list):
    kymin_list = []

    simulation_dict_list = filepath_to_simulation_dict_list(filepath_list)

    for simulation_dict in simulation_dict_list:
        kymin = simulation_dict['parameters_dict']['kymin']

        if kymin not in kymin_list:
            kymin_list.append(kymin)

    return kymin_list