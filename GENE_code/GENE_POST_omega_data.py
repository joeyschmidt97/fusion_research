#!/usr/bin/env python3

# This code will go into all the sub-directories and extract all omega data 
import os
import numpy as np
from GENE_POST_param_data import param_to_dict



def omega_to_dict(omega_file, omega_filepath):
    omega_dict = {}

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

    return omega_dict


def omegas_to_list(filepath):
    omega_list = []
    empty_omega = False

    #Change into the current filepath and get all files
    os.chdir(filepath)
    file_list = os.listdir()
    file_list.sort()

    #Cycle through all the files in a directory
    for file in file_list:
        omega_check = file.startswith('omega')
        size_check = (os.stat(file).st_size != 0) #Check that the file isn't empty

        # If the file is not empty and an omega file then convert to dictionary
        if size_check and omega_check:
            omega_dict = omega_to_dict(file, filepath)   
            omega_list.append(omega_dict) #Add parameter dict to a list
        elif (size_check == False):
            empty_omega = True #Flip switch if omega is empty file

    if (len(omega_list) == 0) and not empty_omega:
        print('There are no files starting with "omega" in:', filepath)

    return omega_list


def omega_to_Hz(omega_dict):
    #Go into filepath where the omega file was found
    omega_filepath = omega_dict['filepath']
    os.chdir(omega_filepath)

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

    # Retrieve relevant conversion variables from parameters file
    parameter_dict = param_to_dict(parameter_file, omega_filepath)
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



if __name__ == "__main__":
    filepath = os.getcwd()
    omega_list = omegas_to_list(filepath)

    for omega_dict in omega_list:
        
        omega_to_Hz(omega_dict)

        print(omega_dict)
