# Get diff/abs value from plot_mode_structure.py



def get_diff_abs_value(filepath, suffix):
    import os
    import subprocess
    os.chdir(filepath)

    # Get the full path to the script
    script_path = os.path.abspath('/global/homes/j/joeschm/ifs_scripts/plot_mode_structures.py')
    result = subprocess.run(['python', script_path, suffix, '-e'], stdout=subprocess.PIPE)  # Run the script with the specified arguments

    # Get the stdout as a string
    output = result.stdout.decode('utf-8')

    # Find the line that contains the "diff/abs" value
    diff_abs_line = [line for line in output.split('\n') if 'diff/abs' in line][0]
    diff_abs_value = float(diff_abs_line.split()[-1])   # Extract the numerical value from the line

    return diff_abs_value





















# from src.utils.file_functions import switch_suffix_file
# # from src.utils.find_buried_filetypes import single_path_find_buried_files

# from src.dict_parameters_data import parameters_filepath_to_dict

# import struct
# import numpy as np
# from os.path import getsize, join


# def read_field_file(filepath, desired_time):
    
#     parameter_filepath = switch_suffix_file(filepath, 'parameters')
#     param_dict = parameters_filepath_to_dict(parameter_filepath)

#     file = open(filepath, 'rb')


#     nx = param_dict['nx0']
#     ny = param_dict['nky0']
#     nz = param_dict['nz0']
#     n_fields = param_dict['n_fields']
#     precision = param_dict['PRECISION']
#     endianness = param_dict['ENDIANNESS']



#     intsize = 4
#     realsize = 8 if precision == 'DOUBLE' else 4
#     complexsize = 2*realsize
#     entrysize = nx*ny*nz*complexsize
#     # jumps in bytes in field/mom files
#     leapfld = n_fields*(entrysize + 2*intsize)

#     complex_dtype = np.dtype(np.complex64) if precision == 'SINGLE' else np.dtype(np.complex128)


#     format_string = '>' if endianness == 'BIG' else '='
#     format_string += 'ifi' if precision == 'SINGLE' else 'idi'

#     timeentry = struct.Struct(format_string)
#     timeentry_size = timeentry.size



#     time_values = []
#     for _ in range(int(getsize(filepath)/(leapfld + timeentry_size))):
#         time = float(timeentry.unpack(file.read(timeentry_size))[1])
#         file.seek(leapfld, 1)
#         time_values.append(time)


#     time_index = time_values.index(desired_time)
#     # print(time_values[-1])
#     # print(time_index, time_values)

#     for i in range(n_fields):
#         offset = timeentry_size + time_index*(timeentry_size + leapfld) + i*(entrysize + 2*intsize) + intsize 
#         file.seek(offset)

#         if i == 0:
#             phi_data = np.fromfile(file, count=nx * ny * nz, dtype=complex_dtype).reshape(nz, ny, nx)
#         elif i == 1:
#             apar_data = np.fromfile(file, count=nx * ny * nz, dtype=complex_dtype).reshape(nz, ny, nx)
#         elif i == 2:
#             bpar_data = np.fromfile(file, count=nx * ny * nz, dtype=complex_dtype).reshape(nz, ny, nx)


#     return phi_data, apar_data, bpar_data, time_values

