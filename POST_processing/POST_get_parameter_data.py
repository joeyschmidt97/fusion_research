import os
import pandas as pd
import sys
sys.path.insert(1, '/global/homes/j/joeschm/ifs_scripts')
from genetools import Parameters


def scanfile_all_parameter_dict(filepath):
    all_scanfile_list = []
    
    last_dir = os.path.basename(filepath)  # Get the last directory of the filepath
    if last_dir.startswith("scanfiles"):
        os.chdir(scanfile_path)
        file_list = os.listdir(scanfile_path)

        for file in file_list:
            size_check = (os.stat(file).st_size != 0)
            parameter_check = (file.startswith("parameters"))
            print(file)
            if size_check and parameter_check:
                par = Parameters()
                par.Read_Pars(file)  #read parameter file
                scanfile_dict = par.pardict  
                
                all_scanfile_list.append(scanfile_dict)
                # print(scanfile_dict)


            else:
                print('No parameter files found.')

    else:
        print("Filepath given is not a scanfile path. Please specify a filepath such as 'path/to/scanfileXXXX'.")

    return all_scanfile_list

def parameters_table(param_dict):
    # Convert the OrderedDict object into a dataframe
    param_df = pd.DataFrame(list(param_dict.items()), columns=['key', 'value'])
    return param_df







filepath = "/global/cscratch1/sd/joeschm/ST_research/NSTXU/129015_OM/TEST"
scanfile_path = filepath + '/scanfiles0000'

all_scanfile_list = scanfile_all_parameter_dict(scanfile_path)
param_df = parameters_table(all_scanfile_list[1])

print(len(all_scanfile_list))
print(param_df)