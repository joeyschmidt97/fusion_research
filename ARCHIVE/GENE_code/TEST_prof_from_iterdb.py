


# COLLECT PROFILE DATA

from cmath import nan
import numpy as np
import re



def create_gprofs(gene_plotting: bool, plot_impurity: bool, gene_i: str, gene_e: str):
    #This function creates the gene plots from ion, elec, and impurity gene files
    if gene_plotting:
        gprof_i = np.genfromtxt(gene_i)
        gprof_e = np.genfromtxt(gene_e)
        if plot_impurity:
            gprof_imp=np.genfromtxt('profiles_z')
        else:
            gprof_imp=np.empty([1, 1])
    else:
        gprof_i=np.empty([1, 1])
        gprof_e=np.empty([1, 1])
        gprof_imp=np.empty([1, 1])
    
    g_plot_dict = {'gprof_i': gprof_i, 'gprof_e': gprof_e, 'gprof_imp': gprof_imp}

    return g_plot_dict



def get_units(data_linesplit: list, lnum: float):  
    #This function extracts the units and quantity labels from ITERDB file
    keep_going = True
    while keep_going:
        unit_test=re.search('-DEPENDENT VARIABLE LABEL',data_linesplit[lnum])
        
        if unit_test :
            quantity=data_linesplit[lnum].split()[0]
            units=data_linesplit[lnum].split()[1]
            
            if __name__ == "__main__":
            #    print ("Plotting :",quantity)
               pass

        test=re.search('DATA FOLLOW',data_linesplit[lnum])
        if test:
            keep_going = False
        
        lnum += 1
    return quantity, units, lnum
    


def create_rhot_arr(lnum: float, data_linesplit: list, sec_num_lines: float):
    #This function creates the x (rhot) and y (arr) data from ITERDB file
    rhot=np.empty(0)
    lnum0 = lnum
    for j in range(lnum0, lnum0 + sec_num_lines):
        for k in range(6):
            str_temp=data_linesplit[j][1+k*13:1+(k+1)*13]
            if(str_temp):
                temp=np.array(data_linesplit[j][1+k*13:1+(k+1)*13],dtype='float')
                rhot=np.append(rhot,temp)

        lnum += 1

    if __name__ == "__main__":
        # print ("time=",data_linesplit[lnum])
        pass

    lnum += 1
    arr=np.empty(0)
    lnum0 = lnum
    for j in range(lnum0, lnum0 + sec_num_lines):
        for k in range(6):
            str_temp=data_linesplit[j][1+k*13:1+(k+1)*13]
            if(str_temp):
                temp=np.array(data_linesplit[j][1+k*13:1+(k+1)*13],dtype='float')
                arr=np.append(arr,temp)

        lnum += 1
    return rhot, arr, lnum



def pressure_profiles(profile_dict: dict):
    T_e = profile_dict['TE']['arr']
    T_i = profile_dict['TI']['arr']
    n_e = profile_dict['NE']['arr']
    n_i = profile_dict['NM1']['arr']
    rhot = profile_dict['TE']['rhot']
    units = "eV^2 K^-1 m^-3"

    P_e = n_e*T_e
    P_i = n_i*T_i

    profile_dict['PE'] = {'units': units, 'rhot': rhot, 'arr': P_e}
    profile_dict['PI'] = {'units': units, 'rhot': rhot, 'arr': P_i}
    profile_dict['PTOT'] = {'units': units, 'rhot': rhot, 'arr': P_e + P_e}
    


def get_slopes(profile_dict: dict):
    quantities = list(profile_dict.keys())

    for quantity in quantities:
        units = profile_dict[quantity]['units']
        arr = profile_dict[quantity]['arr']
        rhot = profile_dict[quantity]['rhot']

        s_arr = np.diff(arr) / np.diff(rhot)
        rhot = rhot[:-1]

        profile_dict['s_' + quantity] = {
            'units': '(slope)' + units,
            'rhot': rhot,
            'arr': s_arr
        }


def create_profiles(filepath: str, gene_e: str, gene_i: str, gene_plotting:bool = False, plot_impurity:bool = False):
    profile_dict = {} #Create empty dict to store profiles and associated data
    g_plot_dict = create_gprofs(gene_plotting, plot_impurity, gene_i, gene_e) #gene plots dict

    f=open(filepath,'r')
    data_in=f.read()
    data_linesplit=data_in.split('\n')  #split file into newline strings
    f.close()

    #Scans through ITERDB and finds out how many points are there
    for i in range(0, len(data_linesplit)):
        test = re.search(';-# OF X PTS',data_linesplit[i]) #find string that contains number of points
        if test:
            num=int( data_linesplit[i].split()[0] )  #convert number of points into an integer

            if __name__ == "__main__":
                print ("number of points:",num)
                
    lnum = 0
    while (len(data_linesplit)-lnum > 10):
        sec_num_lines = int(num/6)
        if num % 6 != 0:
            sec_num_lines += 1
                
        #Mine data from ITERDB file
        quantity, units, lnum = get_units(data_linesplit, lnum)
        rhot, arr, lnum = create_rhot_arr(lnum, data_linesplit, sec_num_lines)

        #add ITERDB data to profiles dictionary
        profile_dict[quantity] = {'units': units, 'rhot': rhot, 'arr': arr}
        
        if quantity=='VROT':
            vout=np.empty((len(arr),2),dtype='float')
            vout[:,0]=rhot
            vout[:,1]=arr
            f=open(quantity+'.dat','w')
            f.write('#'+filepath+'\n'+'#rhot '+quantity+'\n')
            np.savetxt(f,vout)
            f.close()

    pressure_profiles(profile_dict) #add pressure data to profile dictionaries
    get_slopes(profile_dict) #add slopes to profile dictionary

    return profile_dict, g_plot_dict





def auto_create_profiles(filepath: str, gene_plotting:bool = False, plot_impurity:bool = False, print_output:bool = False):
    import os
    os.chdir(filepath)

    iterdb_exists = False
    e_prof_exists = False
    i_prof_exists = False
    
    for file in os.listdir(filepath):
        if file.endswith(".iterdb"): 
            iterdb_file = file
            iterdb_exists = True
        if file.startswith('profiles_e'):
            gene_e = file
            e_prof_exists = True
        if file.startswith('profiles_i'):
            gene_i = file
            i_prof_exists = True

    if (e_prof_exists and i_prof_exists and iterdb_exists):
        if print_output:
            print('Using the following ITERDB file, profile_e, and profile_i to create profiles:')
            print(iterdb_file)
            print(gene_e)
            print(gene_i)
        profile_dict, g_plot_dict = create_profiles(iterdb_file, gene_e, gene_i, gene_plotting, plot_impurity)
        return profile_dict, g_plot_dict 
    else:
        print('The following files are missing to create the profiles: profiles_e & profiles_i')
        
     
#EXAMPLE CODE FOR CREATING PROFILE DATA
path_discharge = '/global/homes/j/joeschm/st_research/NSTXU_discharges/129015/'
profile_dict, g_plot_dict = auto_create_profiles(path_discharge)
print(profile_dict.keys())




# PLOTTING PROFILES

import matplotlib.pyplot as plt
import sys


#Call this function when you want to plot multiple discharges on the same plots for comparison
#INPUT: multi_profile_dict = {'DISCHARGE#1': {'filename_path': f1, 'gene_e_path': ge1, 'gene_i_path': gi1}, 
# 'DISCHARGE#2': {'filename_path': f2, 'gene_e_path': ge2, 'gene_i_path': gi2}, ... }
def multi_plot_profiles(discharge_path_dict: dict, x_start: float = 0, x_end: float = 1, gene_plotting: bool = False, plot_impurity: bool = False):
    
    discharges = list(discharge_path_dict.keys())

    for discharge in discharges:
        path = discharge_path_dict[discharge]['filepath']
        profile_dict, g_plot_dict = auto_create_profiles(path)

        discharge_path_dict[discharge]['profile_dict'] = profile_dict
        discharge_path_dict[discharge]['g_plot_dict'] = g_plot_dict

    quantities = list(profile_dict.keys())
    
    for quantity in quantities:
        for discharge in discharges:
            profile_dict = discharge_path_dict[discharge]['profile_dict']

            rhot = profile_dict[quantity]['rhot']
            arr = profile_dict[quantity]['arr']
            units = profile_dict[quantity]['units']

            if x_start != 0:
                arr = arr[rhot > x_start]
                rhot = rhot[rhot > x_start]
            if x_end != 1:
                arr = arr[rhot < x_end]
                rhot = rhot[rhot < x_end]
            

            plt.plot(rhot, arr, label=quantity+'('+units+')' + ' - ' + discharge)
            
            plt.xlabel(r'$\rho_{tor}$',size=18)
            if x_start != 0 or x_end != 1: plt.xlim(x_start, x_end)
            plt.legend(loc='lower left')

        plt.show()
    # return multi_profile_dict



#Plotting function (called in main script)
def plot_profiles(profile_dict: dict, g_plots: dict, x_start: float = 0, x_end: float = 1, gene_plotting: bool = False, plot_impurity: bool = False):
    print('Available keys:', list(profile_dict.keys()))
    input_type = input("Enter 'a' for all keys or chose from the available keys to plot (separated by spaces): ")
    
    if input_type == 'a':
        quantities = list(profile_dict.keys())
    else:
        quantities = input_type.split()


    for quantity in quantities:
        units = profile_dict[quantity]['units']
        arr = profile_dict[quantity]['arr']
        rhot = profile_dict[quantity]['rhot']
        gprof_i = g_plots['gprof_i']
        gprof_e = g_plots['gprof_e']
        gprof_imp = g_plots['gprof_imp']

        #if a start x-value > 0 then cut off the data where rhot (x-values) exceed the x start point
        if x_start != 0:
            arr = arr[rhot > x_start]
            rhot = rhot[rhot > x_start]
        if x_end != 1:
            arr = arr[rhot < x_end]
            rhot = rhot[rhot < x_end]
            

        plt.plot(rhot,arr,label=quantity+'('+units+')')
        plt.xlabel(r'$\rho_{tor}$',size=18)
        plt.legend(loc='lower left')
        if x_start != 0 or x_end != 1: plt.xlim(x_start, x_end)
        plt.show()
        
        if gene_plotting and quantity=='TI':
            plt.plot(rhot,arr/1000.0,label=quantity+'('+units+')')
            plt.plot(gprof_i[:,0],gprof_i[:,2],'r.',label='$T_i$ gene')
            plt.legend(loc='lower left')
            if x_start != 0 or x_end != 1: plt.xlim(x_start, x_end)
        if gene_plotting and quantity=='NM1':
            plt.plot(rhot,arr/1.0e19,label=quantity+'('+units+')/1.0e19')
            plt.plot(gprof_i[:,0],gprof_i[:,3],'r.',label='$n_i$ gene')
            plt.legend(loc='lower left')
            if x_start != 0 or x_end != 1: plt.xlim(x_start, x_end)
        if gene_plotting and quantity=='NM2' and plot_impurity:
            plt.plot(rhot,arr/1.0e19,label=quantity+'('+units+')/1.0e19')
            plt.plot(gprof_imp[:,0],gprof_imp[:,3],'r.',label='$n_i$ gene')
            plt.legend(loc='lower left')
            if x_start != 0 or x_end != 1: plt.xlim(x_start, x_end)
        if gene_plotting and quantity=='TE':
            plt.plot(rhot,arr/1000.0,label=quantity+'('+units+')')
            plt.plot(gprof_e[:,0],gprof_e[:,2],'r.',label='$T_e$ gene')
            plt.legend(loc='lower left')
            if x_start != 0 or x_end != 1: plt.xlim(x_start, x_end)
        if gene_plotting and quantity=='NE':
            plt.plot(rhot,arr/1.0e19,label=quantity+'('+units+')/1.0e19')
            plt.plot(gprof_e[:,0],gprof_e[:,3],'r.',label='$n_e$ gene')
            plt.legend(loc='lower left')
            if x_start != 0 or x_end != 1: plt.xlim(x_start, x_end)
        plt.show()



# #Only allow user input for filename and e/i profiles if the script is executed in terminal (name == "__main___")
# if __name__ == "__main__":
#     filename = sys.argv[1]
#     gene_e = sys.argv[2]
#     gene_i = sys.argv[3]

#     print(filename)
#     print(gene_e)
#     print(gene_i)
    
#     #If you want to compare with gene profile files:
#     gene_plotting = True    #set to 0 for no gene plots
#     plot_impurity = False

#     profile_dict, g_plots = create_profiles(filename, gene_e, gene_i, gene_plotting, plot_impurity)
#     plot_profiles(profile_dict, g_plots, gene_plotting, plot_impurity, 0)




#Filepath for 129015
path_discharge = '/global/homes/j/joeschm/st_research/NSTXU_discharges/129015/'
profile_dict, g_plot_dict = auto_create_profiles(path_discharge)

x_start = 0
x_end = 1

plot_profiles(profile_dict, g_plot_dict, x_start, x_end)