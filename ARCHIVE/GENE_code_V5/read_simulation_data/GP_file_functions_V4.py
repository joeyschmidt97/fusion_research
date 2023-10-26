import os


def suffix_from_filename(filename:str):
    # function gets the suffix for a given file
    if '_' in filename:
        suffix = filename[-4:]
    else:
        suffix = '.dat'
    return suffix



def switch_suffix_file(old_filepath:str , filetype:str):

    check_exists = os.path.exists(old_filepath)
    check_is_file = os.path.isfile(old_filepath)
    
    if not (check_exists and check_is_file):
        raise FileError(f"The file path does not exist or is not a file: {old_filepath}")
    
    old_directory = os.path.dirname(old_filepath)
    old_filename = os.path.basename(old_filepath)
    suffix = suffix_from_filename(old_filename)

    # If suffix has a '.dat', no change is needed, otherwise prepend an underscore
    mod_suffix = suffix if '.dat' in suffix else '_' + suffix
    new_filepath = os.path.join(old_directory, filetype + mod_suffix)

    # Check that the filepath exists, is a file, and starts with the given filetype (i.e. parameters)
    file_checks(new_filepath , filetype)

    return new_filepath



class FileError(Exception):
    pass

def file_checks(filepath:str , filetype:str):
    check_exists = os.path.exists(filepath)
    check_is_file = os.path.isfile(filepath)
    
    if not (check_exists and check_is_file):
        raise FileError(f"The file path does not exist or is not a file: {filepath}")

    # Get the filename and directory path
    filename = os.path.basename(filepath)
    check_filetype = filename.startswith(filetype)

    if not check_filetype:
        raise FileError(f"The filename does not start with '{filetype}': {filepath}")
    


def string_to_list(string):
    string_list = []
    if isinstance(string, str):
        string_list.append(string)
    elif isinstance(string, list):
        string_list = string
    else:
        raise ValueError(f"Given input {string} is a {type(string)} not a string or list type. Please try again.")

    return string_list



# def rescale_list(input_list:list, resized_max:float, resized_min:float):

#     max_value = max(input_list)
#     min_value = min(input_list)

#     if min_value==max_value:
#         normalized_list = [1]*len(input_list)
#     else:
#         normalized_list = [(val - min_value) / (max_value - min_value) for val in input_list]
    
#     resized_list = [((resized_max - resized_min) * val + resized_min) for val in normalized_list]

#     return resized_list