import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

import sys
sys.path.insert(1, '/global/homes/j/joeschm/ifs_scripts')
from genetools import Parameters

sys.path.insert(1, '/global/u1/j/joeschm/jojo_github/ST_research/coding_tools')
from scanfile_tools_V2 import path_to_scanfile_info
from plot_mode_structures_JOEY_V2 import plot_mode_structures, plot_mode_structures_AUTO_LIMITER


def get_pars(file_list, suffix):
    #This function gets the reference values from the parameters file and outputs the reference omega value, istep_field, and n0_global
    
    file = 'parameters_' + suffix
    if file in file_list:   #if the omega file exists
        par = Parameters()
        par.Read_Pars(file)  #read parameter file
        pars = par.pardict                   #create a dictionary of values   
        # print(pars) 
        return pars
    
    else:
        pass


def split_omega_data(file_list, suffix, pars):
    #This function splits the omega data and outputs ky_min, gamma, and omega
    file = "omega_" + suffix
    
    if (file in file_list) and os.stat(file).st_size != 0:   #if the omega file exists
        data = open(file, "r")     #read omega file
        line = data.readline()     #read first line of data file
        data.close()               #close data file
        
        sline = line.split()             #split line (sline) into separate strings
        sline = list(map(float, sline))  #convert string list to float list

        if len(sline) > 1:
            gamma = sline[1]
            omega = sline[2]
        else:
            gamma = 0
            omega = 0

        #Retrieve reference values
        ky_min = pars['kymin']
        n0_global = pars['n0_global']
        
        TJ = pars['Tref']*1000.0*1.602e-19   #ion temperature in (J)
        mi = pars['mref']*1.6726e-27         #ion mass
        cs = np.sqrt(TJ/mi)                  #speed of sound in a plasma 
        om_ref = cs/pars['Lref']             #reference omega

        omega_kHz = omega*om_ref/1000.0/(2.0*np.pi) #convert omega to kHz
        gamma_kHz = gamma*om_ref/1000.0/(2.0*np.pi) #convert omega to kHz

    else:             #if the omega file is empty, then set values to 0
        ky_min = pars['kymin']
        gamma = 0
        omega = 0
        n0_global = 0
        omega_kHz = 0 
        gamma_kHz = 0

    return ky_min, n0_global, gamma, omega, gamma_kHz, omega_kHz




def split_nrg_data(file_list, suffix):
    #This function splits the omega data and outputs ky_min, gamma, and omega
    file = "nrg_" + suffix
    
    if (file in file_list) and os.stat(file).st_size != 0:   #if the omega file exists

        data = open(file, "r")     #read nrg file
        line = data.readlines()     #read first line of data file
        data.close()               #close data file
        
        last_line = line[-1]
        # print(line[0:10])

        sline = last_line.split()             #split line (sline) into separate strings
        sline = list(map(float, sline))  #convert string list to float list

        Gamma_ES = sline[4]
        Q_ES = sline[6]
        ratio_Gamma_Q = Gamma_ES/Q_ES
        # Gamma_ES = 0
        # Q_ES = 0
        # ratio_Gamma_Q = 0

    else:             #if the omega file is empty, then set values to 0
        Gamma_ES = 0
        Q_ES = 0
        ratio_Gamma_Q = 0

    return Gamma_ES, Q_ES, ratio_Gamma_Q




def omega_dataframes(filepath: str, scanfile_outputs: list = [], criteria_list: list = []):
    
    if 'kymin' not in scanfile_outputs: 
        scanfile_outputs.append('kymin')

    scanfile_df = path_to_scanfile_info(filepath, scanfile_outputs, criteria_list)
    scanfile_suffix_list = scanfile_df[['path', 'suffix']].values.tolist()
    
    temp_df = pd.DataFrame(columns=[])
    
    for scanfile_suffix in scanfile_suffix_list:
        scanfile_path = scanfile_suffix[0]
        suffix = scanfile_suffix[1]
        os.chdir(scanfile_path)
        
        file_list = os.listdir(scanfile_path)
        file_list.sort()
        
        pars = get_pars(file_list, suffix) #get parameters file
        ky_min, n0_global, gamma, omega, gamma_kHz, omega_kHz = split_omega_data(file_list, suffix, pars)
        Gamma_ES, Q_ES, ratio_Gamma_Q = split_nrg_data(file_list, suffix)

        omn_e = pars['omn1']
        omt_e = pars['omt1']
        
        Canik_ratio = ratio_Gamma_Q*(omt_e/omn_e)

        # omega_col = ['n0_global','gamma(cs/a)','gamma(kHz)', 'omega(cs/a)', 'omega(kHz)']
        # omega_data = [n0_global, gamma, gamma_kHz, omega, omega_kHz]

        omega_col = ['n0_global','gamma(cs/a)','gamma(kHz)', 'omega(cs/a)', 'omega(kHz)','Gamma_ES','Q_ES', 'Gamma_ES/Q_ES', 'Canik_ratio']
        omega_data = [n0_global, gamma, gamma_kHz, omega, omega_kHz, Gamma_ES, Q_ES, ratio_Gamma_Q, Canik_ratio]

        omega_scan = pd.DataFrame([omega_data], columns = omega_col) #create dataframe with column titles and data
        temp_df = pd.concat([temp_df, omega_scan]) #append omega scan to temporary dataframe

        # nrg_col = ['n0_global','Gamma_ES','Q_ES', 'Gamma_ES/Q_ES']
        # nrg_data = [n0_global, Gamma_ES, Q_ES, ratio_Gamma_Q]

        # nrg_scan = pd.DataFrame([nrg_data], columns = nrg_col) #create dataframe with column titles and data
        # temp_nrg_df = pd.concat([temp_df, omega_scan]) #append omega scan to temporary dataframe


        # omega_df = omega_df.sort_values(by=['ky_min'])   #sort dataframe by increasing ky_min values

    temp_df.reset_index(drop=True, inplace = True)
    scanfile_omega_df = pd.concat([scanfile_df, temp_df], axis=1) #append omega data to scanfile dataframe
    omega_df = scanfile_omega_df[(scanfile_omega_df[['n0_global', 'gamma(cs/a)']] != 0).all(axis=1)] #remove rows where n0_global and gamma are zero
    no_omega_df = scanfile_omega_df[(scanfile_omega_df[['omega(cs/a)', 'gamma(cs/a)']] == 0).all(axis=1)] #remove rows where n0_global and gamma are zero
    

    # temp_nrg_df.reset_index(drop=True, inplace = True)
    # nrg_df = pd.concat([scanfile_df, temp_nrg_df], axis=1) #append omega data to scanfile dataframe
    

    # display(scanfile_df.loc[:, scanfile_df.columns != 'path'])
    
    omega_df = omega_df.sort_values(by=['kymin'])

    dataframe_dic = {'omega_df': omega_df, 'no_omega_df': no_omega_df, 'all_scanfile_df': scanfile_df}

    return dataframe_dic



# PRINT AND PLOT RELEVANT DATA


def display_omega_df(omega_df, ky_min_arrange = True):
    # if kymin_arrange:
    #     omega_df = omega_df.sort_values(by=['kymin'])

    display(omega_df.loc[:, omega_df.columns != 'path'])
    return None




def log_plot(omega_df, x_value, y_value, ax=None, **kwargs):
    x = omega_df[[x_value]].to_numpy()
    y = omega_df[[y_value]].to_numpy()
    
    ax = ax or plt.gca()
    ax.set_xscale('log')
    
    ax.set_xlabel(x_value, fontsize=15)
    ax.set_ylabel(y_value, fontsize=15)
    
    return ax.plot(x,y, **kwargs)



def plot_Gamma_Q_ratio(filepath1, filepath2, filepath3, plot_type = 'global'):

    print('filepath 1:', filepath1)
    print('filepath 2:', filepath2)
    print('filepath 3:', filepath3)


    dataframe_dic_1 = omega_dataframes(filepath1)
    dataframe_dic_2 = omega_dataframes(filepath2)
    dataframe_dic_3 = omega_dataframes(filepath3)



    omega_df1 = dataframe_dic_1['omega_df']

    Gamma_sum = sum(omega_df1['Gamma_ES'])
    Q_sum = sum(omega_df1['Q_ES'])
    ratio = Gamma_sum/Q_sum
    print('filepath', filepath1)
    print('ratio:', ratio)



    omega_df2 = dataframe_dic_2['omega_df']

    Gamma_sum = sum(omega_df2['Gamma_ES'])
    Q_sum = sum(omega_df2['Q_ES'])
    ratio = Gamma_sum/Q_sum
    print('filepath', filepath2)
    print('ratio:', ratio)



    omega_df3 = dataframe_dic_3['omega_df']

    Gamma_sum = sum(omega_df3['Gamma_ES'])
    Q_sum = sum(omega_df3['Q_ES'])
    ratio = Gamma_sum/Q_sum
    print('filepath', filepath3)
    print('ratio:', ratio)



    

    fig, (ax1,ax2) = plt.subplots(1,2, figsize=(10, 4))
    if plot_type == 'global':
        log_plot(omega_df1, 'n0_global', 'Gamma_ES/Q_ES', ax1, color='blue', linestyle = 'dotted', marker = 'o', label='OM')
        log_plot(omega_df2, 'n0_global', 'Gamma_ES/Q_ES', ax1, color='green', linestyle = 'dotted', marker = 'x', label='OM (density +30%)')
        log_plot(omega_df3, 'n0_global', 'Gamma_ES/Q_ES', ax1, color='red', linestyle = 'dotted', marker = 'v', label='OM (density -30%)')
        ax1.legend(loc="upper left")
    elif plot_type == 'kymin':
        log_plot(omega_df1, 'kymin', 'Gamma_ES/Q_ES', ax1, color='blue', linestyle = 'dotted', marker = 'o')
    
    # fig.suptitle(filepath, fontsize=12)

    if __name__ == '__main__':
        plt.show()



def plot_Canik_ratio(filepath1, canik_ratio, plot_type = 'global'):


    print('filepath 1:', filepath1)
    
    dataframe_dic_1 = omega_dataframes(filepath1)
    omega_df1 = dataframe_dic_1['omega_df']
    

    fig, (ax1,ax2) = plt.subplots(1,2, figsize=(10, 4))
    if plot_type == 'global':
        log_plot(omega_df1, 'n0_global', 'Canik_ratio', ax1, color='blue', linestyle = 'dotted', marker = 'o', label='OM (129015)')
        
        x = np.linspace(1,10000,100)
        y = np.full((1, len(x)), canik_ratio, dtype=float)

        ax1.plot(x,y[0], label = 'Canik')
        ax1.legend(loc="lower right")
    elif plot_type == 'kymin':
        log_plot(omega_df1, 'kymin', 'Gamma_ES/Q_ES', ax1, color='blue', linestyle = 'dotted', marker = 'o')
    
    # fig.suptitle(filepath, fontsize=12)

    if __name__ == '__main__':
        plt.show()




def plot_gamma_omega(filepath, plot_type = 'global'):

    print('filepath:', filepath)

    dataframe_dic = omega_dataframes(filepath)
    omega_df = dataframe_dic['omega_df']

    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10, 4))
    if plot_type == 'global':
        log_plot(omega_df, 'n0_global', 'gamma(kHz)', ax1, color='blue', linestyle = 'dotted', marker = 'o')
        log_plot(omega_df, 'n0_global', 'omega(kHz)', ax2, color='red', linestyle = 'dotted', marker = 'o')
    elif plot_type == 'kymin':
        log_plot(omega_df, 'kymin', 'gamma(cs/a)', ax1, color='blue', linestyle = 'dotted', marker = 'o')
        log_plot(omega_df, 'kymin', 'omega(cs/a)', ax2, color='red', linestyle = 'dotted', marker = 'o')
    
    fig.suptitle(filepath, fontsize=12)

    if __name__ == '__main__':
        plt.show()

    




def plot_omega_mode_structures(omega_df, x_limit1 = 2, x_limit2 = 2):    
    # if 'kymin' in omega_df.columns:
    #     omega_df = omega_df.sort_values(by=['kymin'])

    scanpath_suffix_list = omega_df[['path', 'suffix']].values.tolist()

    for scan_suffix in scanpath_suffix_list:
        path = scan_suffix[0]
        suffix = scan_suffix[1]

        omega_scan_data = omega_df.loc[(omega_df['path'] == path) & (omega_df['suffix'] == suffix)]
        
        print('')
        print(path)
        print('')
        display_omega_df(omega_scan_data)
        
        os.chdir(path)
        plot_mode_structures(suffix, x_limit1, x_limit2)
        
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')





def plot_omega_mode_structures_AUTO_LIMITER(omega_df, perc = .02, limit = 1e-2):    
    # if 'kymin' in omega_df.columns:
    #     omega_df = omega_df.sort_values(by=['kymin'])

    scanpath_suffix_list = omega_df[['path', 'suffix']].values.tolist()

    for scan_suffix in scanpath_suffix_list:
        path = scan_suffix[0]
        suffix = scan_suffix[1]

        omega_scan_data = omega_df.loc[(omega_df['path'] == path) & (omega_df['suffix'] == suffix)]
        
        print('')
        print(path)
        print('')
        display_omega_df(omega_scan_data)
        
        os.chdir(path)
        plot_mode_structures_AUTO_LIMITER(suffix, limit, perc)
        
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')





if __name__ == '__main__':



    # filepath1 = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129038/OM_top_30NE_minus/'
    # filepath2 = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129038/OM_top_30NE_plus/'
    # filepath3 = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129038/Impurities_OM_top/'
    # plot_Gamma_Q_ratio(filepath1, filepath2, filepath3, 'global')


    filepath1 = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129015/OM_top_30NE_minus/'
    filepath2 = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129015/OM_top_30NE_plus/'
    filepath3 = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129015/Impurities_OM_top/'
    plot_Gamma_Q_ratio(filepath1, filepath2, filepath3, 'global')


    # # filepath = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129038/OM_top_30NE_plus/'
    # # plot_gamma_omega(filepath, 'n0_global')
    
    # filepath = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129038/Impurities_OM_top/'
    # plot_gamma_omega(filepath, 'global')
    
    
    
    # path = os.getcwd()
    # plot_gamma_omega(path, 'kymin')

    # filepath = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129015/Impurities_OM_top/'
    # plot_gamma_omega(filepath, 'kymin')
    # plot_gamma_omega(filepath, 'global')

    # filepath = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129015/OM_top_30NE_plus/'
    # plot_gamma_omega(filepath, 'kymin')
    # plot_gamma_omega(filepath, 'global')

    # filepath = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129015/OM_top_30NE_minus/'
    # plot_gamma_omega(filepath, 'kymin')
    # plot_gamma_omega(filepath, 'global')



    # filepath = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129015/Impurities_PE_top/'
    # plot_gamma_omega(filepath, 'kymin')

