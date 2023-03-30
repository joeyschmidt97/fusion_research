#!/usr/bin/env python3

# This code will go into all the sub-directories and extract all parameters data 

import os
import sys
sys.path.insert(1, '/global/homes/j/joeschm/ifs_scripts')
from genetools import Parameters


def scan_or_single_check(filepath):
    pass

    return




cwd = os.getcwd()
directory_list = os.listdir(cwd)

for directory in directory_list:

    print(directory)

    if os.path.isdir(directory):  
        print("It is a directory\n")  
    else:  
        pass



        # size_check = (os.stat(file).st_size != 0)
        # parameter_check = (file.startswith("parameters"))
        # print(file)
        # if size_check and parameter_check:
        #     par = Parameters()
        #     par.Read_Pars(file)  #read parameter file
        #     scanfile_dict = par.pardict  
            
        #     all_scanfile_list.append(scanfile_dict)
        #     # print(scanfile_dict)


        # else:
        #     print('No parameter files found.')




def parameters_table(param_dict):
    # Convert the OrderedDict object into a dataframe
    param_df = pd.DataFrame(list(param_dict.items()), columns=['key', 'value'])
    return param_df







