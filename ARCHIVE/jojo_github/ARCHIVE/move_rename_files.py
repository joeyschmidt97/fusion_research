import os
import sys
import shutil

sys.path.insert(1, '/global/u1/j/joeschm/jojo_github/ST_research/coding_tools')
from omega_to_df_plotting_V2 import omega_dataframes






def last_suffix_in_target(target_path):    
    file_list = os.listdir(target_path)
    file_list.sort()

    suffix_list = []

    if file_list: #if list is not empty
        for file in file_list:
            if file.startswith("parameters_"):
                suffix = file[-4:]
                suffix_list.append(suffix)
    else:
        suffix_list.append('0000')

    last_suffix = suffix_list[-1]
            
    
    return last_suffix




def next_suffix(suffix):
    next_suffix_int = int(suffix) + 1
    next_suffix = str(next_suffix_int)

    if len(next_suffix) == 1:
        next_suffix = '000' + next_suffix
    elif len(next_suffix) == 2:
        next_suffix = '00' + next_suffix
    elif len(next_suffix) == 3:
        next_suffix = '0' + next_suffix

    return next_suffix



def navigate_and_rename(source, suffix):
    for item in os.listdir(source):
        s = os.path.join(source, item)
        if os.path.isdir(s):
            navigate_and_rename(s)
        elif s.endswith(suffix):
            shutil.copy(s, os.path.join(source, "newname.html"))    




if __name__ == '__main__':

    # current_path = os.getcwd()

    current_path = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129038/COMBINED_DATA/COMBINED_OM_top_30NE_plus'


    target_path = current_path + '/all_scans'
    if not os.path.exists(target_path): os.mkdir(target_path)

    temp_path = current_path + '/all_scans/temp_data'
    if not os.path.exists(temp_path): os.mkdir(temp_path)

    target_path = current_path + '/all_scans/scanfiles0000'
    if not os.path.exists(target_path): os.mkdir(target_path)




    # GET ALL SCANFILES PATHS AND SUFFICES
    # GO INTO SCANFILE AND TARGET ALL FILES WITH SUFFIX END 

    # COPY ALL RELEVANT FILES TO A TEMP FOLDER
    # GET NEXT SUFFIX FROM TARGET FOLDER
    # RENAME ALL FILES TO END WITH NEXT SUFFIX
    # MOVE FILES TO SCANFILES0000

    
    
    # MOVE FILES TO SCANFILES0000

    # GET ALL SCANFILES PATHS AND SUFFICES
    
    criteria_list = []
    scanfile_outputs = ['kymin', 'x0']

    dataframes = omega_dataframes(current_path, scanfile_outputs, criteria_list)
    omega_df = dataframes['omega_df']
    omega_df = omega_df.sort_values(by=['kymin'])

    omega_df = omega_df.drop_duplicates(subset=['kymin'], keep='first')


    drop_list = ['path', 'gamma(kHz)', 'gamma(cs/a)', 'omega(kHz)', 'omega(cs/a)', 'Gamma_ES', 'Q_ES', 'Gamma_ES/Q_ES', 'Canik_ratio']
    print(omega_df.drop(drop_list, axis=1))




    scanpath_suffix_list = omega_df[['path', 'suffix']].values.tolist()


    # scanpath_suffix_list = scanpath_suffix_list[-4:]
    # print('scanfile suffix list', scanpath_suffix_list)


    kymin_list = omega_df['kymin'].values.tolist()
    print('scanlist:', kymin_list)
    print('scan_dim:', len(kymin_list))
    print('diagdir = ', target_path)
    print('par_in_dir = ', target_path + '/in_par')

    for scan_suffix in scanpath_suffix_list:
    
        # GO INTO SCANFILE AND TARGET ALL FILES WITH SUFFIX END 

        scanfile_path = scan_suffix[0]
        suffix = scan_suffix[1]

        os.chdir(scanfile_path)    
        file_list = os.listdir(scanfile_path)
        file_list.sort()

        # print(scanfile_path, suffix)

        last_suff = last_suffix_in_target(target_path)
        next_suff = next_suffix(last_suff)
        # print(next_suff)

        for file in file_list:
            if file.endswith(suffix):
                
                # COPY ALL RELEVANT FILES TO A TEMP FOLDER

                shutil.copyfile(scanfile_path + file, temp_path + '/' + file)

                # GET NEXT SUFFIX FROM TARGET FOLDER
            
                # RENAME ALL FILES TO END WITH NEXT SUFFIX
                file_no_suffix = file[:-4]
                file_new_suffix = file_no_suffix + next_suff
                # print(file_new_suffix)

                # os.rename(temp_path + file, target_path + file_new_suffix)

                os.rename(temp_path + '/' + file, target_path + '/' + file_new_suffix)


                






    
    

        



