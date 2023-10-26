import struct
import numpy as np
from os.path import getsize

from src.utils.file_functions import switch_suffix_file, file_checks, FileError, rescale_list
from src.dict_parameters_data import parameters_filepath_to_dict
from src.filetype_key_lists import field_key_list, field_column_keys



def field_filepath_to_dict(field_filepath:str, time_criteria='all', field_quantities='all'):
    """
    Converts a 'field' file at a given filepath to a field dictionary.
    Returns the field dictionary.
    """

    try:
        file_checks(field_filepath, filetype='field')
        field_dict = create_field_dict(field_filepath, time_criteria, field_quantities)

        return field_dict
    except FileError as e:
        print(e)



def create_field_dict(field_filepath:str, time_criteria='all', field_quantities='all'):
    """
    Reads field data from a binary file and returns a dictionary containing relevant information.

    Args:
    - field_filepath (str): The path to the field binary file.
    - choose_time (str, float, int, list): Specifies the time instance(s) to extract. Options:
        - 'last': Extracts data at the last available time.
        - 'first': Extracts data at the first available time.
        - float, int: Extracts data at the specified time value.
        - list: Extracts data for the specified time range [start_time, end_time].
    - named_field_col (str, list): Specifies the field column(s) to extract. Options:
        - 'all': Extracts all fields.
        - str: Extracts the specified field column (phi OR apar OR bpar).
        - list: Extracts multiple specified field columns (i.e. ['phi', 'bpar']).
    - time_option (str): toggles time between 'ABS' (absolute) or 'REL' (relative) time - doesn't affect output time added to nrg_dict
        - 'ABS': absolute time given by simulation 
        - 'REL': relative time scaled between [0,1]... useful to compare many simulations with different simulation times
    Returns:
    - dict: A dictionary containing field data and relevant information.
    """

    # Initializing the field dictionary with default values
    field_dict = {}

    
    if time_criteria=='all':
        time_criteria = {'bounds': [float('-inf'), float('inf')], 'logic_op_list': ['>', '<']}


    # Extracting parameters from the corresponding parameters file
    parameter_filepath = switch_suffix_file(field_filepath, 'parameters')
    param_dict = parameters_filepath_to_dict(parameter_filepath)


    # Reading binary field data
    with open(field_filepath, 'rb') as file:
        # Extracting parameters from the parameter dictionary
        nx, ny, nz, n_fields, precision, endianness = (
            param_dict['nx0'],
            param_dict['nky0'],
            param_dict['nz0'],
            param_dict['n_fields'],
            param_dict['PRECISION'],
            param_dict['ENDIANNESS']
        )

        # Setting sizes based on precision
        intsize = 4
        realsize = 8 if precision == 'DOUBLE' else 4
        complexsize = 2 * realsize
        entrysize = nx * ny * nz * complexsize
        leapfld = n_fields * (entrysize + 2 * intsize)

        # Creating NumPy dtype for complex numbers based on precision
        complex_dtype = np.dtype(np.complex64) if precision == 'SINGLE' else np.dtype(np.complex128)

        # Setting the format string based on endianness and precision
        format_string = '>' if endianness == 'BIG' else '='
        format_string += 'ifi' if precision == 'SINGLE' else 'idi'
        timeentry = struct.Struct(format_string)
        timeentry_size = timeentry.size


        # Extracting time values from field file
        all_time_values = []
        for _ in range(int(getsize(field_filepath) / (leapfld + timeentry_size))):
            time = float(timeentry.unpack(file.read(timeentry_size))[1])
            file.seek(leapfld, 1)
            all_time_values.append(time)



        # Handling different time extraction options
        if time_criteria['bounds'] == 'last':
            time_index_list = [all_time_values.index(max(all_time_values))]
        elif time_criteria['bounds'] == 'first':
            time_index_list = [all_time_values.index(min(all_time_values))]
        elif isinstance(time_criteria['bounds'], list) and len(time_criteria['bounds']) == 2:
            start_time, end_time = time_criteria['bounds']
            
            time_index_list = [time_ind for time_ind, time in enumerate(all_time_values) if start_time <= time <= end_time]
        else:
            raise ValueError(f'Ensure choose time is given as "last", "first", a float, or a range "1 < time < 2"')


        # Add time values given choose_time value(s)
        field_dict['time'] = [all_time_values[time_ind] for time_ind in time_index_list]
        if field_dict['time'] == []:
            return {}
        
        # Specify which columns of field data are added
        if field_quantities == 'all':
            field_names = field_column_keys #all data [phi, apar, bpar]
        else:
            # specific columns i.e. [phi, bpar] or if string given then wrap into list 
            field_names = [field_quantities] if isinstance(field_quantities, str) else field_quantities


        # cycle through time values
        for time_index in time_index_list:
            # cycle through field names from named_field_col above
            for field_name in field_names:
                ind = field_column_keys.index(field_name) # get index of field name (phi -> 0, apar -> 1, bpar -> 2)
                # calculate offset in field file to retrieve said data
                offset = timeentry_size + time_index * (timeentry_size + leapfld) + ind * (
                            entrysize + 2 * intsize) + intsize
                file.seek(offset)

                data_array = np.fromfile(file, count=nx * ny * nz, dtype=complex_dtype).reshape(nz, ny, nx)

                # Appending reshaped field data into field dict
                field_dict.setdefault(field_name, []).append(data_array)

    field_dict['filepath'] = field_filepath
    field_dict['key_list'] = field_key_list
    return field_dict
