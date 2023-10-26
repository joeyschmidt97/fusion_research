#!/usr/bin/env python3

import os
import sys
sys.path.insert(1, '/global/u1/j/joeschm/fusion_research/GENE_code_V3')
from GP_simulation_data_V3 import species_value_from_simulation, load_simulation_filepath
from GP_parameter_data_V3 import parameter_filepath_to_dict
from GP_nrg_data_V3 import nrg_filepath_to_dict





#------------------------------------------------------------------------------------------------
# Function to collect MTM data in a dict organized by kymin values-------------------------------
#------------------------------------------------------------------------------------------------

def extract_data_points(simulation_dict_list: list, species: str = 'e',  cutoff_value = None) -> dict:
    """
    Extract relevant data points from a list of simulation dictionaries based on unique kymin values.
    Args:
        simulation_dict_list (list): A list of dictionaries each representing a simulation.
        species (str, optional): The species for which data points are to be extracted. Defaults to 'e'.
    Returns:
        dict: Dictionary organized by kymin containing extracted data points and reference values.
    """
    
    kymin_data_points_dict = {}
    
    # Collect a list of unique kymin values from the simulation dictionary list
    kymin_list = collect_kymin_list(simulation_dict_list)

    for kymin in kymin_list:
        # Lists to store extracted data points
        coll_list = []
        beta_list = []
        omt_list = []
        ratio_QEM_QES_list = []

        # Dictionary to store the reference point values
        ref_point_dict = {}

        # Iterate over each simulation to extract relevant data
        for simulation_dict in simulation_dict_list:
            # Filter simulations by kymin
            if kymin == simulation_dict['parameters_dict']['kymin']:
                # Extract parameter values from simulation
                coll = simulation_dict['parameters_dict']['coll']
                beta = simulation_dict['parameters_dict']['beta']
                omt_name = species_value_from_simulation(simulation_dict, 'omt', species)
                omt = simulation_dict['parameters_dict'][omt_name]

                # Extract Q_EM and Q_ES values from nrg dict
                Q_EM_name = species_value_from_simulation(simulation_dict, 'Q_EM', species)
                Q_ES_name = species_value_from_simulation(simulation_dict, 'Q_ES', species)
                Q_EM = simulation_dict['nrg_dict'][Q_EM_name][-1]
                Q_ES = simulation_dict['nrg_dict'][Q_ES_name][-1]

                # Extract the reference point for the current simulation
                ref_point_dict = collect_ref_point(simulation_dict, species, ref_point_dict)

                # Add the datapoints to the lists 
                coll_list.append(coll)
                beta_list.append(beta)
                omt_list.append(omt)
                ratio_QEM_QES_list.append(Q_EM/Q_ES)


        if (cutoff_value!=None) and (isinstance(cutoff_value, float) or isinstance(cutoff_value, int)) and (cutoff_value > 0):

            # if all(ratio_Q > cutoff_value for ratio_Q in ratio_QEM_QES_list):
            #     # Scaling marker sizes based on the ratio of Q_EM/Q_ES values if all values are above the cutoff
            #     max_Q_ratio = max(ratio_QEM_QES_list)
            #     min_Q_ratio = min(ratio_QEM_QES_list)
            #     max_size = cutoff_value
            #     min_size = 1

            #     norm_Q_ratio_list = [(val - min_Q_ratio) / (max_Q_ratio - min_Q_ratio) for val in ratio_QEM_QES_list]
            #     ratio_QEM_QES_list = [((max_size - min_size) * val + min_size) for val in norm_Q_ratio_list]
            # else:
            
            for i, Q_ratio in enumerate(ratio_QEM_QES_list):
                if Q_ratio > cutoff_value:
                    ratio_QEM_QES_list[i] = cutoff_value
        elif (cutoff_value==None):
            pass
        else:
            print('Please specify "cutoff_value" as a float value above 0')
            break



        # Store the extracted data points for the current kymin in the result dictionary
        kymin_data_points_dict[kymin] = {
            'coll': coll_list, 
            'beta': beta_list, 
            'omt': omt_list, 
            'Q_EM/Q_ES': ratio_QEM_QES_list, 
            'reference_point': ref_point_dict
        }

    return kymin_data_points_dict


#------------------------------------------------------------------------------------------------
# Function to collect kymin data points from simulation dict-------------------------------------
#------------------------------------------------------------------------------------------------

def collect_kymin_list(simulation_dict_list: list) -> list:
    """
    Extract a sorted list of unique 'kymin' values from a list of simulation dictionaries.
    Args:
        simulation_dict_list (list): A list of dictionaries each representing a simulation.
    Returns:
        list: A sorted list of unique 'kymin' values.
    """
    
    kymin_list = []

    # Iterate over each simulation dictionary
    for simulation_dict in simulation_dict_list:
        # Extract the 'kymin' value
        kymin = simulation_dict['parameters_dict']['kymin']

        # If the 'kymin' value is not already in the list, add it
        if kymin not in kymin_list:
            kymin_list.append(kymin)

    # Sort the list of 'kymin' values
    kymin_list.sort()

    return kymin_list


#------------------------------------------------------------------------------------------------
# Function(s) to collect reference data points from submitted parameter scan---------------------
#------------------------------------------------------------------------------------------------

def extract_value_from_string(value_str: str) -> float:
    """
    Extract float value from a string based on the predefined format.
    Args:
    - value_str (str): The input string, e.g., "value=123.45  !scan:123.45*perc(0)"
    Returns:
    - float: Extracted float value from the string.
    """
    # Split the string by '!scan:', take the last part, then split by '*' and take the first part, and finally strip to convert to float
    
    return float(value_str.split('!scan:')[-1].split('*')[0].strip())


def collect_ref_point(simulation_dict: dict, species: str, ref_point_dict: dict) -> dict:
    """
    Collect reference points from a simulation dictionary. 
    Args:
    - simulation_dict (dict): Dictionary containing simulation parameters.
    - species (str): The species for which the reference point is to be collected.
    - ref_point_dict (dict): Dictionary containing existing reference points (can be empty).
    Returns:
    - dict: Updated reference point dictionary.
    """
    # Get the file path for the parameters from the simulation dictionary
    scanfile_path = simulation_dict['input_directory']
    parameter_filepath = os.path.join(scanfile_path, 'parameters')
    
    # Convert the parameter file to a dictionary
    param_dict = parameter_filepath_to_dict(parameter_filepath)
    
    # Get the name associated with 'omt' for the given species from the simulation dictionary
    omt_name = species_value_from_simulation(simulation_dict, 'omt', species)
    
    # Keys for the parameters that we are interested in
    ref_keys = ['coll', 'beta', omt_name]
    
    # Extract the float values associated with these keys
    ref_list = [extract_value_from_string(param_dict[key]) for key in ref_keys]
    
    # Check if the reference values match with the given reference dictionary (if it's populated)
    if ref_point_dict and ref_list == [ref_point_dict['coll'], ref_point_dict['beta'], ref_point_dict['omt']]:
        get_Q_ratio = False
    else:
        get_Q_ratio = True

    # If required, compute the Q ratio and update the reference dictionary
    if get_Q_ratio:
        # Load the file path associated with 'nrg' from the simulation dictionary
        nrg_filepath = load_simulation_filepath(simulation_dict, 'nrg')
        
        # Get the number of species from the simulation dictionary
        n_spec = simulation_dict['parameters_dict']['n_spec']
        
        # Convert the nrg file to a dictionary
        nrg_dict = nrg_filepath_to_dict(nrg_filepath, n_spec)
        
        # Get the names associated with 'Q_EM' and 'Q_ES' for the given species from the simulation dictionary
        Q_EM_name = species_value_from_simulation(simulation_dict, 'Q_EM', species)
        Q_ES_name = species_value_from_simulation(simulation_dict, 'Q_ES', species)
        
        # Update the reference point dictionary with the new values
        ref_point_dict.update({
            'coll': ref_list[0],
            'beta': ref_list[1],
            'omt': ref_list[2],
            'Q_EM/Q_ES': nrg_dict[Q_EM_name][-1] / nrg_dict[Q_ES_name][-1]
        })

    return ref_point_dict




def dist_3D_from_reference_point(kymin_data_points_dict:dict):

    coll_list = kymin_data_points_dict['coll']
    beta_list = kymin_data_points_dict['beta']
    omt_list = kymin_data_points_dict['omt']
    ratio_Q_EM_Q_ES = kymin_data_points_dict['Q_EM/Q_ES']

    rescale_ratio_Q_EM_Q_ES = []
    for ratio_Q in ratio_Q_EM_Q_ES:
        if ratio_Q > 1:
            ratio_Q = 2

        rescale_ratio_Q_EM_Q_ES.append(ratio_Q)

    ratio_Q_EM_Q_ES = rescale_ratio_Q_EM_Q_ES
    
    # Extracting reference point values
    reference_point = kymin_data_points_dict['reference_point']
    ref_coll, ref_beta, ref_omt = reference_point['coll'], reference_point['beta'], reference_point['omt']
        
    # Calculating 3D distances
    distances = []
    for coll, beta, omt in zip(coll_list, beta_list, omt_list):
        distance = ((coll - ref_coll)**2 + (beta - ref_beta)**2 + (omt - ref_omt)**2)**0.5
        distances.append(distance)
    


    # Add distances to dict
    kymin_data_points_dict['3D_distances'] = distances

    return kymin_data_points_dict

