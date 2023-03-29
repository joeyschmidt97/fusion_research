#!/usr/bin/env python3

import os
import re
import pandas as pd


def species_dataframe(lines, line, i, species_df):
    column_names = line.split()
    df = pd.DataFrame(columns=column_names)

    for temp_line in lines[i+1:-1]:
        if '---' in temp_line:
            break

        values = temp_line.split()
        values_df = pd.DataFrame(values).T
        values_df.columns = column_names
        df = pd.concat([df, values_df], axis=0, ignore_index=True)

    if re.search(r'\bz\b', line):
        df.drop('indx' , axis=1, inplace=True)
        species_df = df
    else:
        df.drop('Z' , axis=1, inplace=True)
        species_df = pd.concat([species_df, df], axis=1)
    
    return species_df


def data_2_dict(line, info_dict):
    if ':' in line:
        parts = line.split(":")  # split the text using ":" as delimiter
    elif '=' in line:
        parts = line.split("=")

    two_columns = False
    if len(parts) == 3:
        center = parts[1]
        if all(element == center[0] for element in center):
            parts.remove(center)
        else:
            center_split = center.split()
            parts[1:2] = center_split
            two_columns = True


    if two_columns:
        key1 = parts[0].strip()  
        value1 = parts[1].strip()
        try:
            value1 = float(value1)
        except:
            pass

        key2 = parts[2].strip()  
        value2 = parts[3].strip()
        try:
            value2 = float(value2)
        except:
            pass

        # Add key-value pairs to dictionary
        info_dict[key1] = value1
        info_dict[key2] = value2

    else:
        key = parts[0].strip()  
        value = parts[-1].strip()

        try:
            value = float(value)
        except:
            pass

        # Add key-value pair to dictionary
        info_dict[key] = value


def out_neo_data_2_dict():
    # Check if file exists
    if os.path.isfile('out.neo.run'):
        
        info_dict = {}
        species_df = pd.DataFrame()

        # Open file and read lines
        with open('out.neo.run', 'r') as f:
            lines = f.readlines()

        # Loop through lines
        for i, line in enumerate(lines):
            if re.search(r'\bz\b', line) or re.search(r'\bZ\b', line):        
                species_df = species_dataframe(lines, line, i, species_df)

            elif (':' in line) or ('=' in line):
                data_2_dict(line, info_dict)
            else:
                continue


        species_list = species_df.to_dict('records')
        for spec in species_list:
            for key, value in spec.items():
                try:
                    spec[key] = float(value)
                except:
                    pass
        
        info_dict['species'] = species_list

        # Print resulting dictionary
        return info_dict

    else:
        print('File not found.')


if __name__ == '__main__':
    info_dict = out_neo_data_2_dict()
    print(info_dict)
