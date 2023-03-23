import sys
import os

sys.path.insert(1, '/global/u1/j/joeschm/jojo_github/ST_research/coding_tools')
from scanfile_tools_V2 import path_to_scanfile_info, display_scanfile_info, scanfile_mode_structures
from omega_to_df_plotting_V2 import omega_dataframes, display_omega_df, plot_gamma_omega, plot_omega_mode_structures, plot_omega_mode_structures_AUTO_LIMITER


def print_omega_data(filepath, scanfile_outputs, criteria_list):

    dataframes = omega_dataframes(filepath, scanfile_outputs, criteria_list)
    omega_df = dataframes['omega_df']
    no_omega_df = dataframes['no_omega_df']


    if omega_df.empty:
        ref_df = no_omega_df
    else:
        ref_df = omega_df

    i_dens_grad = ref_df['omn1'].to_list()
    i_dens_grad = float(i_dens_grad[0])
    e_dens_grad = ref_df['omn2'].to_list()
    e_dens_grad = float(e_dens_grad[0])
    c_dens_grad = ref_df['omn3'].to_list()
    c_dens_grad = float(c_dens_grad[0])

    # i_dens = no_omega_df['dens1'].to_list()
    # i_dens = float(i_dens[0])
    # e_dens = no_omega_df['dens2'].to_list()
    # e_dens = float(e_dens[0])
    # c_dens = no_omega_df['dens3'].to_list()
    # c_dens = float(c_dens[0])

    # i_charge = no_omega_df['charge1'].to_list()
    # i_charge = float(i_charge[0])
    # e_charge = no_omega_df['charge2'].to_list()
    # e_charge = float(e_charge[0])
    # c_charge = no_omega_df['charge3'].to_list()
    # c_charge = float(c_charge[0])

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('current directory:', filepath)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('ion dens grad:', i_dens_grad)
    print('electron dens grad:', e_dens_grad)
    print('carbon dens grad:', c_dens_grad)

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('ion dens grad (30 perc +):', i_dens_grad*1.3)
    print('electron dens grad (30 perc +):', e_dens_grad*1.3)
    print('carbon dens grad (30 perc +):', c_dens_grad*1.3)

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('ion dens grad (30 perc -):', i_dens_grad*0.7)
    print('electron dens grad (30 perc -):', e_dens_grad*0.7)
    print('carbon dens grad (30 perc -):', c_dens_grad*0.7)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # print('grad quasi', i_dens_grad*i_dens*i_charge + e_dens_grad*e_dens*e_charge + c_dens_grad*c_dens*c_charge)


    drop_list = ['path', 'nz0', 'gamma(kHz)', 'gamma(cs/a)', 'omega(kHz)', 'omega(cs/a)', 'omn1' , 'omn3', 'Gamma_ES', 'Q_ES']

    if __name__ == '__main__':
        print('omega runs')
        print(omega_df.drop(drop_list, axis=1))

        print('no omega runs')
        print(no_omega_df.drop(drop_list, axis=1))
    else:
        print('omega runs')
        display(omega_df.drop(drop_list, axis=1))

if __name__ == '__main__':
    cwd = os.getcwd()

    criteria_list = []
    scanfile_outputs = ['nz0', 'kymin', 'omn1', 'omn2', 'omn3', 'x0']

    print_omega_data(cwd, scanfile_outputs, criteria_list)
