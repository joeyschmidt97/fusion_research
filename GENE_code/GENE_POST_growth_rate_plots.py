#!/usr/bin/env python3

import os
from GENE_POST_all_sim_data import simulations_to_data
from GENE_POST_omega_data import omega_to_Hz


def compare_growth_rates(filepath_list):
    return 1


def plot_growth_rates(filepath):
    kymin_values = []
    omega_values = []
    simulation_list = simulations_to_data(filepath)

    for simulation_dict in simulation_list:
        filepath = simulation_dict['filepath']
        parameter_dict_list = simulation_dict['parameters']
        omega_dict_list = simulation_dict['omegas']

        print(filepath)
        

        for parameter_dict in parameter_dict_list:
            print(parameter_dict['kymin'], parameter_dict['filename'])

        for omega_dict in omega_dict_list:
            omega_dict = omega_to_Hz(omega_dict)
            print(omega_dict['kymin'], omega_dict['gamma (kHz)'], omega_dict['omega (kHz)'], omega_dict['filename'])
        


if __name__=="__main__":
    filepath = os.getcwd()
    plot_growth_rates(filepath)