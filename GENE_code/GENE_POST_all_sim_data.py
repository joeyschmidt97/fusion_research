#!/usr/bin/env python3

# This code will go into all the sub-directories and extract all parameters data 
import os
from GENE_POST_param_data import parameters_filepaths, param_to_dict
from GENE_POST_omega_data import omegas_filepaths, omega_to_dict




def load_dicts_data(simulation_list, param_filepath):
    param_dict = param_to_dict(param_filepath)

    directory = os.path.dirname(param_filepath)
    parameter_file = os.path.basename(param_filepath)
    if '_' in parameter_file:
        suffix = parameter_file[-5:]
    else:
        suffix = '.dat'
    
    #omega dictionary builder
    omega_filepath = os.path.join(directory, 'omega' + suffix)
    omega_dict = omega_to_dict(omega_filepath)

    #if the omega dict is empty then don't add the simulation
    if omega_dict:
        simulation_dict = {}
        simulation_dict['parameter_file'] = param_dict
        simulation_dict['omega_file'] = omega_dict
        simulation_list.append(simulation_dict)
    else:
        pass

    return simulation_list



def simulations_to_list(filepath):
    simulation_list = []

    #get parameter filepaths and check how many there are
    param_filepath_list = parameters_filepaths(filepath)
    omega_filepath_list = omegas_filepaths(filepath)
    param_count = len(param_filepath_list)

    # print(len(param_filepath_list), len(omega_filepath_list))

    if param_count == 0:
        #if there are no parameter files check sub-directories for parameter files
        directory_list = os.listdir(filepath)
        directory_list.sort()

        for directory_name in directory_list:
            # Skip files that start with "X_" 
            if directory_name.startswith('X_'):
                pass
            else:
                directory_path = os.path.join(filepath, directory_name)
                # print(directory_path)
                #if the directory is actually a directory check for any parameters files
                if os.path.isdir(directory_path):
                    param_filepath_list = parameters_filepaths(directory_path)
                    
                    for param_filepath in param_filepath_list:
                        simulation_list = load_dicts_data(simulation_list, param_filepath)
                        

        pass
    else:
        #if there are any parameter file in the current directory convert them to a dict and add it to the list      
        for param_filepath in param_filepath_list:
            simulation_list = load_dicts_data(simulation_list, param_filepath)

   
    for simulation_dict in simulation_list:
        param_dict = simulation_dict['parameter_file']
        omega_dict = simulation_dict['omega_file']

        # print(param_dict['filename'] ,param_dict['kymin'], omega_dict['filename'], param_dict['kymin'])


    #if there are no parameters files in current or sub-directories throw an error message
    if len(simulation_list) == 0:
        print("Neither the current directory nor any of its child directories contain a file starting with 'parameters', or all child directories start with 'X_'.")


    return simulation_list










    

# def get_sim_filepath(param_dict, sim_dict):
#     sim_filepaths = []

#     #get parameter filename and path
#     param_filename = param_dict['filename']
#     param_directory = param_dict['filepath']

#     #extract suffix if present in parameters filename
#     if '_' in param_filename:
#         suffix = param_filename[-4:]
#     else:
#         suffix = ''
    
#     #get files from parameters directory
#     filelist = os.listdir(param_directory)
#     filelist.sort()

#     for filename in filelist:
#         filepath = os.path.join(param_directory, filename) #get the absolute file path

#         check1 = os.path.isfile(filepath)   #check that file is actually a file
#         check2 = suffix in filename         #check that the suffix (i.e. 0002) is in parameters, else '' is always in a string
#         check3 = (not filename.startswith('parameters')) #check that file is NOT a parameters file

#         #if all checks are fulfilled add the file to the filepath list
#         if check1 and check2 and check3:
#             sim_filepaths.append(filepath)

#     #add the filepath list to the parameter dictionary
#     param_dict['sim_files'] = sim_filepaths
    
#     return param_dict






# def simulations_to_data(filepath):
#     simulation_list = []

#     directory_list = os.listdir(filepath)
#     directory_list.sort()

#     for directory_name in directory_list:
        
#         # Skip files that start with "X_" 
#         if directory_name.startswith('X_'):
#             pass

#         else:
#             simulation_dict = {} 
#             directory_path = os.path.join(filepath, directory_name)

#             if os.path.isdir(directory_path):
#                 parameter_list = parameters_to_list(directory_path)
#                 simulation_dict['parameters'] = parameter_list

#                 omega_list = omegas_to_list(directory_path)
#                 simulation_dict['omegas'] = omega_list

#                 simulation_dict['filepath'] = directory_path
#                 simulation_list.append(simulation_dict)

#             else:  
#                 pass

#     return simulation_list









# if __name__ == "__main__":
#     cwd = os.getcwd()
#     simulation_list = simulations_to_data(cwd)

#     for simulation_dict in simulation_list:
#         filepath = simulation_dict['filepath']
#         parameter_list = simulation_dict['parameters']
#         omega_list = simulation_dict['omegas']

#         print(filepath)

#         for parameter in parameter_list:
#             print(parameter['kymin'], parameter['filename'])

#         for omega in omega_list:
#             print(omega['kymin'], omega['gamma (cs/a)'], omega['omega (cs/a)'], omega['filename'])
        
