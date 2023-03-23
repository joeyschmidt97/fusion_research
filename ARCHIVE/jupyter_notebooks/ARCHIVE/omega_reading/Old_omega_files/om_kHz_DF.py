#!/usr/bin/env python
# coding: utf-8

# ### Import Necessary Libraries

# In[1]:


import pandas as pd
import numpy as np
import os

import sys
sys.path.insert(1, '/global/homes/j/joeschm/IFS_scripts')
from genetools import Parameters


# ### Function for Retrieving Non-zero Omega Files

# In[2]:


def get_om_ref(filename):
    #This function gets the reference values from the parameters file and outputs the reference omega value, istep_field, and n0_global
    
    suffix = filename[-4:]     #get 00xx suffix for omega file
    par = Parameters()
    par.Read_Pars('parameters_'+suffix)  #read parameter file

    pars = par.pardict                   #create a dictionary of values
    TJ = pars['Tref']*1000.0*1.602e-19   #ion temperature in (J)
    mi = pars['mref']*1.6726e-27         #ion mass
    cs = np.sqrt(TJ/mi)                  #speed of sound in a plasma 
    om_ref = cs/pars['Lref']             #reference omega
       
    return om_ref, pars


# In[3]:


def split_omega_data(filename):
    #This function splits the omega data and outputs ky_min, gamma, and omega
    
    data = open(filename, "r") #read omega file
    line = data.readline()     #read first line of data file
    data.close()               #close data file

    sline = line.split()             #split line (sline) into separate strings
    sline = list(map(float, sline))  #convert string list to float list

    ky_min = sline[0]
    gamma = sline[1]
    omega = sline[2]

    return ky_min, gamma, omega


# In[4]:


def omega_df(filepath, nz0_low, nz0_high):
    omega_col = ['scanfile', 'ky_min', 'n0_global','gamma(cs/a)','gamma(kHz)', 'omega(kHz)', 'nz0', 'hyp_z']
    omega_df = pd.DataFrame(columns=omega_col)

    scanfile_list = os.listdir(filepath)
    for scanfile in scanfile_list:                #run through list of scanfiles
        scanfile_path = filepath + "/" + scanfile
        os.chdir(scanfile_path)                   #enter into scanfile directory

        
        
        for filename in os.listdir(os.getcwd()):
            if filename.startswith("omega_") and (os.stat(filename).st_size != 0): #open omega file and extract data if it is non-empty
                om_ref, pars = get_om_ref(filename)  #retrieve reference and parameter values         
                ky_min, gamma, omega = split_omega_data(filename) #split data from omega file
                
                omega_kHz = omega*om_ref/1000.0/(2.0*np.pi) #convert omega to kHz
                gamma_kHz = gamma*om_ref/1000.0/(2.0*np.pi) #convert omega to kHz
                
                
                n0_global = float(pars['n0_global'])
                istep_field = pars['istep_field']    #read istep_field value
                nz0 = pars['nz0']
                hyp_z = pars['hyp_z']

                C1 = (omega and gamma) != 0
                C2 = nz0_low < nz0 < nz0_high
                C3 = istep_field <= 10
                criteria = C1 and C2 and C3
                #criteria = ((omega and gamma) != 0) and (istep_field == 10) #proceed if growth rate isn't 0 or is considered stable
                
                if criteria:
                    omega_scan = pd.DataFrame([[scanfile, ky_min, n0_global,gamma, gamma_kHz, omega_kHz, nz0, hyp_z]], columns = omega_col)
                    omega_df = omega_df.append(omega_scan)
    
    omega_df = omega_df.sort_values(by=['ky_min'])   #sort dataframe by increasing ky_min values
    
    return omega_df

