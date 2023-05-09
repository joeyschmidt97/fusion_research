#!/usr/bin/env python3

# This code will go into all the sub-directories and extract all omega data 
import os
import numpy as np
from GENE_POST_param_data import parameter_to_sim_dict
from GENE_POST_file_checks import suffix_from_filename, file_check



# def omega_to_sim_dict(simulation_list):
def omega_to_sim_dict(simulation_dict):
    simulation_files = simulation_dict['simulation files']

    for filepath in simulation_files:
        check_omega = file_check(filepath, 'omega')

        # check if file is omega file
        if check_omega:
            omega_dict = omega_filepath_to_dict(filepath)
            simulation_dict['omega'] = omega_dict
            parameter_to_sim_dict(simulation_dict)

            omega_dict_to_Hz(simulation_dict)
    
    return simulation_dict



# ~~~AUXILLARY FUNCTIONS~~~


def omega_filepath_to_dict(omega_filepath):
    #get oemga filename and directory path
    omega_file = os.path.basename(omega_filepath)
    omega_directory = os.path.dirname(omega_filepath)
    suffix = suffix_from_filename(omega_file)

    os.chdir(omega_directory)   #go into omega directory

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
    omega_dict['suffix'] = suffix

    return omega_dict






def omega_dict_to_Hz(simulation_dict):
    param_dict = simulation_dict['parameters']
    omega_dict = simulation_dict['omega']

    # collect filename and relevant values
    omega_cs = omega_dict['omega (cs/a)']
    gamma_cs = omega_dict['gamma (cs/a)']

    # collect parameter values to convert omega values
    TJ = param_dict['Tref']      #ion temperature in (J)
    mi = param_dict['mref']      #ion mass
    Lf = param_dict['Lref']      #reference length of the device
    cs = np.sqrt(TJ/mi)              #speed of sound in a plasma 
    om_ref = cs/Lf                   #reference omega
    
    # Convert omega and gamma to kHz range
    omega_dict['omega (kHz)'] = omega_cs*om_ref/1000.0/(2.0*np.pi) #convert omega to kHz
    omega_dict['gamma (kHz)'] = gamma_cs*om_ref/1000.0/(2.0*np.pi) #convert omega to kHz

    # Add global kymin values to omega dict
    omega_dict['n0_global'] = param_dict['n0_global']

    return simulation_dict












# if __name__ == "__main__":
#     filepath = os.getcwd()
#     omega_list = omegas_to_list(filepath)

#     for omega_dict in omega_list:
        
#         omega_to_Hz(omega_dict)

#         print(omega_dict)
