import sys
sys.path.insert(1, '/global/homes/j/joeschm/fusion_research/PRE_processing')
from PRE_prof_data_from_iterdb import auto_create_profiles


path_discharge = '/global/homes/j/joeschm/st_research/NSTXU_discharges/129015/'
profile_dict, g_plot_dict = auto_create_profiles(path_discharge)

print(profile_dict.keys())