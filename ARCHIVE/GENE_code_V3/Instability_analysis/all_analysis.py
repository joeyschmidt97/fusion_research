#!/usr/bin/env python3

import sys
import os
sys.path.insert(1, '/global/homes/j/joeschm/fusion_research/GENE_code_V3/Instability_analysis')
from MTM_analysis import MTM_plots

def all_analysis(discharge_filepath:str, analysis_dict:dict):

    MTM_analysis = True
    MTM_filepath = 'MTM_limit' #Note this is added to discharge_filepath (discharge_filepath + MTM_filepath)




    if MTM_analysis:
        print('MTM Analysis')
        filepath_list = os.path.join(discharge_filepath, MTM_filepath)
        MTM_plots(filepath_list, plot_type = '3D')