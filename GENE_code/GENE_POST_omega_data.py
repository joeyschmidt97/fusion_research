#!/usr/bin/env python3

# This code will go into all the sub-directories and extract all omega data 
import os


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


# if __name__=="__main__":
#     omegas_to_list(os.getcwd())
