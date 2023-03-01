import sys
sys.path.insert(1, '/global/homes/j/joeschm/fusion_research/PRE_processing')
from PRE_plot_PE_NE_OM_points import multiplot_PE_NE_OM
from PRE_plot_profiles_iterdb import plot_profiles, multi_plot_profiles


discharge_path_dict = {}
path = '/global/homes/j/joeschm/st_research/NSTXU_discharges/'

#Filepath for 129015
discharge = '129015'
path_discharge = path + discharge + '/'
discharge_path_dict[discharge] = {'filepath': path_discharge}


#Filepath for 129038
discharge = '129038'
path_discharge = path + discharge + '/'
discharge_path_dict[discharge] = {'filepath': path_discharge}

x_lim = 0.0
multi_plot_profiles(discharge_path_dict, x_lim)



# path_discharge = '/global/homes/j/joeschm/st_research/NSTXU_discharges/129015/'
# point_list = [.87, .85, .936]

# print(point_list)
# # multiplot_PE_NE_OM(path_discharge, point_list)



# #Filepath for 129038
# path_discharge = '/global/homes/j/joeschm/st_research/NSTXU_discharges/129038/'
# point_list = [.5, .655, .91]

# multiplot_PE_NE_OM(path_discharge, point_list)






