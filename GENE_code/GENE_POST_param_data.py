#!/usr/bin/env python3

# This code will go extract all parameters data from the current directory or sub-directories

import os
import sys
sys.path.insert(1, '/global/homes/j/joeschm/ifs_scripts')
from genetools import Parameters



def param_to_dict(parameter_filepath):
    #get parameter filename and directory path
    parameter_file = os.path.basename(parameter_filepath)
    parameter_directory = os.path.dirname(parameter_filepath)
    os.chdir(parameter_directory)   #gp into parameter directory

    #create parameter dictionary
    par = Parameters()
    par.Read_Pars(parameter_file)  #read parameter file
    parameter_dict = par.pardict 

    #Add filename and filepath (can be different than diagdir) to dict
    parameter_dict['filename'] = parameter_file
    parameter_dict['filepath'] = parameter_directory

    # if '_' in parameter_file:
    #     suffix = parameter_file[-4:]
    # else:
    #     suffix = '.dat'
    
    # parameter_dict['suffix'] = suffix

    #add other simulation data filepaths to parameters dict
    # parameter_dict = get_sim_filepath(parameter_dict)

    return parameter_dict



# def get_sim_filepath(param_dict):
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





def parameters_filepaths(directory):
    param_filepath_list = []    #list to store parameter filepaths in the given directory
    filetype = 'parameters' #filetype to add to filepath list

    #get files in given directory
    filelist = os.listdir(directory)
    filelist.sort()
    for filename in filelist:
        filepath = os.path.join(directory, filename) #get the absolute file path

        # Check that the file is a parameter file and is ACTUALLY a file 
        if filename.startswith(filetype) and os.path.isfile(filepath):
            param_filepath_list.append(filepath) #add parameter filepath to list
    
    #if we have multiple parameters files then remove the base parameter file (parameters.dat)
    if len(param_filepath_list) > 1:
        for param_filepath in param_filepath_list[:]:  # iterate over a copy of the list to safely modify it
            if not os.path.basename(param_filepath).startswith('parameters_'):
                param_filepath_list.remove(param_filepath)

    return param_filepath_list






def parameters_to_list(filepath):
    parameter_list = []

    #get parameter filepaths and check how many there are
    param_filepath_list = parameters_filepaths(filepath)
    param_count = len(param_filepath_list)

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
                #if the directory is actually a directory check for any parameters files
                if os.path.isdir(directory_path):
                    param_filepath_list = parameters_filepaths(directory_path)
                    for param_filepath in param_filepath_list:
                        #get parameters dictionaries and add them to the parameters list
                        param_dict = param_to_dict(param_filepath)
                        parameter_list.append(param_dict)

        pass
    else:
        #if there are any parameter file in the current directory convert them to a dict and add it to the list
        for param_filepath in param_filepath_list:
            param_dict = param_to_dict(param_filepath)
            parameter_list.append(param_dict)

    #if there are no parameters files in current or sub-directories throw an error message
    if len(parameter_list) == 0:
        print("Neither the current directory nor any of its child directories contain a file starting with 'parameters', or all child directories start with 'X_'.")


    return parameter_list



def print_parameter(filepath, key_list):

    parameter_list = parameters_to_list(filepath)

    print(filepath)

    if isinstance(key_list, str):
        for parameter in parameter_list:
            print(os.path.basename(parameter['filepath']), '///', parameter['filepath'], key_list,':', parameter[key_list])

    elif isinstance(key_list, list):
        for parameter in parameter_list:
            print(os.path.basename(parameter['filepath']), '///', parameter['filename'])
            for key in key_list:
                print(key,':', parameter[key])


# if __name__=="__main__":
#     filepath = os.getcwd()

#     print(filepath)
#     parameter_list = parameters_to_list(filepath)

#     for param_dict in parameter_list:
#         print(param_dict['kymin'], param_dict['filename'])

#         # for sim_filepath in param_dict['sim_files']:
#         #     filename = os.path.basename(sim_filepath)
#         #     print(sim_filepath)
#     print('')
