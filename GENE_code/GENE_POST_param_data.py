#!/usr/bin/env python3

# This code will go into all the sub-directories and extract all parameters data 

import os
import sys
sys.path.insert(1, '/global/homes/j/joeschm/ifs_scripts')
from genetools import Parameters


def param_to_dict(parameter_file, filepath):
    par = Parameters()
    par.Read_Pars(parameter_file)  #read parameter file
    parameter_dict = par.pardict 

    #If the diagdir variable is different than the current directory then overwrite it
    if parameter_dict['diagdir'] != filepath:
        parameter_dict['diagdir'] = filepath
    
    return parameter_dict


def param_list(filepath):
    parameter_list = []

    #Change into the current filepath and get all files
    os.chdir(filepath)
    file_list = os.listdir()
    file_list.sort()

    #Count how many parameter files there are
    param_files = 0
    for file in file_list:
        if file.startswith('parameters'):
            param_files += 1

    #If there are any parameter files then execute
    if param_files > 0:
        for file in file_list:
            size_check = (os.stat(file).st_size != 0) #Check that the file isn't empty

            #Default to search for a single parameter file but override if more are present
            parameter_check = (file.startswith("parameters"))
            if param_files > 1:
                parameter_check = (file.startswith("parameters_"))

            # If the file is not empty and a parameter file then convert to dictionary
            if size_check and parameter_check:
                parameter_dict = param_to_dict(file, filepath)   
                parameter_list.append(parameter_dict) #Add parameter dict to a list
            else:
                pass
    else:
        print('There are no files starting with "parameters" in:', filepath)

    return parameter_list



def parameters_table(param_dict):
    # Convert the OrderedDict object into a dataframe
    param_df = pd.DataFrame(list(param_dict.items()), columns=['key', 'value'])
    return param_df

