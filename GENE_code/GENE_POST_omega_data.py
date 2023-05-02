#!/usr/bin/env python3

# This code will go into all the sub-directories and extract all omega data 
import os
import numpy as np
from GENE_POST_param_data import param_to_dict




def omegas_filepaths(directory):
    omega_filepath_list = []    #list to store parameter filepaths in the given directory
    filetype = 'omega' #filetype to add to filepath list

    #get files in given directory
    filelist = os.listdir(directory)
    filelist.sort()
    for filename in filelist:
        filepath = os.path.join(directory, filename) #get the absolute file path

        check1 = filename.startswith(filetype)
        check2 = os.path.isfile(filepath)
        check3 = (os.stat(filepath).st_size != 0)

        # Check that the file is a parameter file and is ACTUALLY a file 
        if check1 and check2 and check3:
            omega_filepath_list.append(filepath) #add parameter filepath to list

    return omega_filepath_list














def omega_to_dict(omega_filepath):
    #get parameter filename and directory path
    omega_file = os.path.basename(omega_filepath)
    omega_directory = os.path.dirname(omega_filepath)
    os.chdir(omega_directory)   #gp into parameter directory

    omega_dict = {}

    check_exists = os.path.exists(omega_filepath)
    check_nonempty = (os.stat(omega_filepath).st_size != 0)

    if check_exists and check_nonempty:
        # Read in the omega file
        with open(omega_file, 'r') as file:
            lines = file.readlines()

        # Split lines and put values into omega dict
        for line in lines:
            items = line.split()

            omega_dict['kymin'] = float(items[0])
            omega_dict['gamma (cs/a)'] = float(items[1])
            omega_dict['omega (cs/a)'] = float(items[2])
        
        # Add filename and filepath to omege dictionary
        omega_dict['filename'] = omega_file
        omega_dict['filepath'] = omega_filepath

        omega_dict = omega_to_Hz(omega_dict)
    else:
        pass
    
    return omega_dict


def omega_to_Hz(omega_dict):
    #Go into filepath where the omega file was found
    omega_filepath = omega_dict['filepath']
    omega_dir = os.path.dirname(omega_filepath)
    os.chdir(omega_dir)

    # Collect filename and relevant values
    omega_file = omega_dict['filename']
    omega_cs = omega_dict['omega (cs/a)']
    gamma_cs = omega_dict['gamma (cs/a)']

    # Get suffix if multiples files exist and get parameters_XXXX or parameters file 
    if '_' in omega_file:
        suffix = omega_file[-4:]
        parameter_file = 'parameters_' + suffix
    else:
        parameter_file = 'parameters.dat'

    parameter_filepath = os.path.join(omega_dir, parameter_file)
    # Retrieve relevant conversion variables from parameters file
    parameter_dict = param_to_dict(parameter_filepath)
    
    
    TJ = parameter_dict['Tref']      #ion temperature in (J)
    mi = parameter_dict['mref']      #ion mass
    Lf = parameter_dict['Lref']      #reference length of the device
    cs = np.sqrt(TJ/mi)              #speed of sound in a plasma 
    om_ref = cs/Lf                   #reference omega
    

    # Convert omega and gamma to kHz range
    omega_dict['omega (kHz)'] = omega_cs*om_ref/1000.0/(2.0*np.pi) #convert omega to kHz
    omega_dict['gamma (kHz)'] = gamma_cs*om_ref/1000.0/(2.0*np.pi) #convert omega to kHz

    # Add global kymin values to omega dict
    n0_global = parameter_dict['n0_global']
    omega_dict['n0_global'] = n0_global

    return omega_dict












# if __name__ == "__main__":
#     filepath = os.getcwd()
#     omega_list = omegas_to_list(filepath)

#     for omega_dict in omega_list:
        
#         omega_to_Hz(omega_dict)

#         print(omega_dict)
