#!/usr/bin/env python
# coding: utf-8

# ### Import Necessary Libraries

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from os.path import exists

import sys
sys.path.insert(1, '/global/homes/j/joeschm/IFS_scripts')
from genetools import Parameters


# ### Function for Retrieving Non-zero Omega Files

# In[7]:


def omega_EV_df(filepath):
    omega_col = ['scanfile', 'kymin', 'n0_global','gamma(cs/a)', 'omega(kHz)']
    omega_df = pd.DataFrame(columns=omega_col)

    scanfile_list = os.listdir(filepath)
    for scanfile in scanfile_list:                #run through list of scanfiles

        scanfile_path = filepath + "/" + scanfile
        os.chdir(scanfile_path)                   #enter into scanfile directory
        
        if exists(scanfile_path + "/" + "EV_log.csv"):
            

            omega_CSV = pd.read_csv("EV_log.csv")
            omega_CSV['n0_global'] = 0

            ky_n0_col = ['kymin', 'n0_global']
            ky_n0_df = pd.DataFrame(columns=ky_n0_col)

            for filename in os.listdir(os.getcwd()):
                if filename.startswith("parameters_"):
                    suffix = filename[-4:]     #get 00xx suffix for omega file
                    par = Parameters()
                    par.Read_Pars('parameters_'+suffix)  #read parameter file

                    pars = par.pardict                   #create a dictionary of values
                    n0_global = pars['n0_global']   #
                    kymin = pars['kymin']         #ion mass

                    ky_n0_scan = pd.DataFrame([[kymin, n0_global]], columns = ky_n0_col)
                    ky_n0_df = ky_n0_df.append(ky_n0_scan)

            #omega_CSV.drop_duplicates(inplace=True)

            omega_CSV = ky_n0_df.set_index('kymin').combine_first(omega_CSV.drop_duplicates().set_index('kymin')).reset_index() #fill in n0_global values according to kymin values
            omega_CSV['n0_global'] = omega_CSV.n0_global.astype(float) #convert from an object to a float


            omega_temp = pd.DataFrame(columns=omega_col)
            omega_temp = pd.DataFrame({'scanfile': scanfile , 'kymin': omega_CSV['kymin'], 'n0_global': 0, 'gamma(cs/a)': 0, 'omega(kHz)': 0})
            omega_temp['kymin'] = omega_CSV['kymin']
            omega_temp['n0_global'] = omega_CSV['n0_global']
            omega_temp['gamma(cs/a)'] = omega_CSV['gamma(cs/a)']
            omega_temp['omega(kHz)'] = omega_CSV['omega(kHz)']

            omega_df = omega_df.append(omega_temp)
            #print(omega_temp)

    return omega_df


# ### Check Data Output and Plot

# In[8]:


efit2_path = "/global/cscratch1/sd/joeschm/AUG/efit2_EVS"
miller2_path = "/global/cscratch1/sd/joeschm/AUG/miller2_EVS"


# In[9]:


efit2_omega = omega_EV_df(efit2_path).reset_index()
print(efit2_omega)


# In[10]:


miller2_omega = omega_EV_df(miller2_path).reset_index()
print(miller2_omega)


# In[11]:


ax = efit2_omega.plot(x ='n0_global', y='omega(kHz)', kind = 'scatter', color = 'red', label = 'efit2', alpha = 0.2)
miller2_omega.plot(x ='n0_global', y='omega(kHz)', kind = 'scatter', ax = ax, label = 'miller2', alpha = 0.2)

#plt.ylim(-30000,-3000)
plt.legend()
plt.show()


# In[ ]:





# In[ ]:




