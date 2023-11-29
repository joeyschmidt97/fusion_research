from cmath import nan
import numpy as np
import re


# THIS CODE CREATES PROFILE DATA IN A TIMESERIES GIVEN A FILEPATH AND AN ITERDB FILE

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
               print ("Plotting :",quantity)

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
        print ("time=",data_linesplit[lnum])

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
        
     
# #EXAMPLE CODE FOR CREATING PROFILE DATA
# path_discharge = '/global/homes/j/joeschm/st_research/NSTXU_discharges/129015/'
# profile_dict, g_plot_dict = auto_create_profiles(path_discharge)

# print(profile_dict.keys())
