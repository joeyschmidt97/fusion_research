#!/usr/bin/env python
# coding: utf-8

# ### Import Necessary Libraries

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

import sys
sys.path.insert(1, '/global/homes/j/joeschm/IFS_scripts')
from genetools import Parameters


# ### Function for Retrieving Non-zero Omega Files

# In[2]:


def get_pars(filename):
    #This function gets the reference values from the parameters file and outputs the reference omega value, istep_field, and n0_global
    
    suffix = filename[-4:]     #get 00xx suffix for omega file
    par = Parameters()
    par.Read_Pars('parameters_' + suffix)  #read parameter file

    pars = par.pardict                   #create a dictionary of values

    return pars, suffix


# In[3]:


def split_omega_data(suffix, pars):
    #This function splits the omega data and outputs ky_min, gamma, and omega
    file = "omega_" + suffix
    
    if (os.path.isfile(file)) and (os.stat(file).st_size != 0):   #if the omega file exists and is not-empty
        data = open(file, "r")     #read omega file
        line = data.readline()     #read first line of data file
        data.close()               #close data file

        sline = line.split()             #split line (sline) into separate strings
        sline = list(map(float, sline))  #convert string list to float list

        ky_min = sline[0]
        gamma = sline[1]
        omega = sline[2]
        
        #Retrieve reference values
        n0_global = pars['n0_global']
        
        TJ = pars['Tref']*1000.0*1.602e-19   #ion temperature in (J)
        mi = pars['mref']*1.6726e-27         #ion mass
        cs = np.sqrt(TJ/mi)                  #speed of sound in a plasma 
        om_ref = cs/pars['Lref']             #reference omega

        omega_kHz = omega*om_ref/1000.0/(2.0*np.pi) #convert omega to kHz
        gamma_kHz = gamma*om_ref/1000.0/(2.0*np.pi) #convert omega to kHz

    else:             #if the omega file is empty, then set values to 0
        ky_min = 0
        gamma = 0
        omega = 0
        n0_global = 0
        omega_kHz = 0 
        gamma_kHz = 0

    return ky_min, n0_global, gamma, omega, gamma_kHz, omega_kHz


# In[4]:


def omega_df(filepath, criteria_list, displayed_outputs):
    
    omega_df = pd.DataFrame(columns=[])
    
    print_parameters = False
    if "PARAMETERS" in criteria_list:
        print_parameters = True
    
    
    scanfile_list = os.listdir(filepath)
    for scanfile in scanfile_list:                #run through list of scanfiles
        scanfile_path = filepath + "/" + scanfile
        os.chdir(scanfile_path)                   #enter into scanfile directory      
        
        #print(scanfile)
        
        if scanfile.startswith("scanfiles"):

            for filename in os.listdir(os.getcwd()):
                #print(filename)

                if filename.startswith("parameters_") and (os.stat(filename).st_size != 0): #check parameter (only for scans) if it's not empty
                    crit_col = []
                    output_vals = []

                    pars, suffix = get_pars(filename) #get pars file and suffix

                    ky_min, n0_global, gamma, omega, gamma_kHz, omega_kHz = split_omega_data(suffix, pars)  #read the omega file
                    C1 = (omega != 0) and (gamma != 0)                 #additional criteria that gamma and omega be greater than 0

                    crit_sum = 0
                    for key, value in pars.items():
                        for criteria in criteria_list:
                            if not print_parameters:
                                if key in criteria:
                                    if eval(criteria.replace(key, str(value))):
                                        crit_sum += 1

                                        for key in criteria.split():  #if a pars key is in the criteria list add the key and its value to lists 
                                            if key in pars.keys():
                                                crit_col.append(key)
                                                output_vals.append(pars[key])



                    if crit_sum + C1 == len(criteria_list) + 1: #if the crit sum and criteria length match then execute

                        #Default dataframe data and column headings
                        df_data = [scanfile, suffix, ky_min, n0_global, gamma, gamma_kHz, omega, omega_kHz]
                        omega_col = ['scanfile', 'suffix', 'ky_min', 'n0_global','gamma(cs/a)','gamma(kHz)', 'omega(cs/a)', 'omega(kHz)']

                        for item in displayed_outputs:  #append the desired output column name and its value to the dataframe
                            df_data.append(pars[item])
                            omega_col.append(item)


                        df_data.extend(output_vals) #add the values to the dataframe
                        omega_col.extend(crit_col)  #add the criteria key variables to the dataframe column headers

                        omega_scan = pd.DataFrame([df_data], columns = omega_col)
                        omega_df = omega_df.append(omega_scan)

                        omega_df = omega_df.sort_values(by=['ky_min'])   #sort dataframe by increasing ky_min values
    
    if print_parameters:   #if "PARAMETERS" is in the criteria list then print the keys
        print(pars.keys())
    
    return omega_df
# In[8]:


def plot_omega_gamma(df_1, df_2, label_1, label_2, marker_style, size):
    if df_1.empty or df_2.empty:
        print('one of the dataframes is empty and cannot be plotted!')
        pass
        
    else:
        ax = df_1.plot(x ='n0_global', y='omega(kHz)', kind = 'scatter', color = 'red', label = label_1, alpha = 0.5, marker = marker_style, s = size)
        df_2.plot(x ='n0_global', y='omega(kHz)', kind = 'scatter', color = 'blue', label = label_2,  alpha = 0.5, marker = marker_style, s=size, ax = ax)
        
        plt.legend()
        plt.show()
        
        ax = df_1.plot(x ='n0_global', y='gamma(kHz)', kind = 'scatter', color = 'red', label = label_1, alpha = 0.5, marker = marker_style, s = size)
        df_2.plot(x ='n0_global', y='gamma(kHz)', kind = 'scatter', color = 'blue', label = label_2,  alpha = 0.5, marker = marker_style, s = size, ax = ax)

        plt.legend()
        plt.show()
    


# In[ ]:




