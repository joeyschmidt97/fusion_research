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
    



# def path_to_name_dir_suffix(filepath:str):

#     filename = os.path.basename(filepath)
#     directory = os.path.dirname(filepath)
#     suffix = suffix_from_filename(filename)

#     return filename, directory, suffix



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
    


def count_files_in_dir(directory:str , filetype:str):

    check_is_dir = os.path.isdir(directory)
    if not check_is_dir:
        raise FileError(f"The file path given is not a directory: {directory}")

    count = 0
    for filename in os.listdir(directory):
        if filename.startswith(filetype) and os.path.isfile(os.path.join(directory, filename)):
            count += 1
    return count




def string_to_list(string):
    string_list = []
    if isinstance(string, str):
        string_list.append(string)
    elif isinstance(string, list):
        string_list = string
    else:
        raise FileError(f"Given input {string} is a {type(string)} not a string or list type. Please try again.")

    return string_list



def find_buried_filetype_files(base_filepath_list:list, filetype:str, max_depth=2, current_depth=0):
    """
    Recursively searches for a certain filetype ('parameters/omega/nrg' used in code comment example) in a directory and its subdirectories up to a specified maximum depth.
    Returns a list of filepaths for all files found.
    If no files are found at the maximum depth, prints an error message and stops the search.
    """
    base_filepath_list = string_to_list(base_filepath_list)
    # Initialize an empty list to store the filepaths of the 'parameters/omega/nrg' files
    filetype_files = []

    for base_filepath in base_filepath_list:

        check_exists = os.path.exists(base_filepath)
        if not check_exists:
            raise FileError(f"The file path does not exist: {base_filepath}")


        # Check if the base filepath is a 'parameters/omega/nrg' file
        if filetype in os.path.basename(base_filepath):
            filetype_files.append(base_filepath)
        
        # if path is not already a 'parameters/omega/nrg' file then continue searching
        else:
            # Count the number of 'parameters/omega/nrg' files in the base filepath
            filetype_count = count_files_in_dir(base_filepath, filetype)
            
            # If there are no 'parameters/omega/nrg' files and the current depth is less than the maximum depth, continue the search
            if filetype_count == 0 and current_depth < max_depth:
                # Get a list of directories in the base filepath
                dirlist = os.listdir(base_filepath)
                dirlist.sort()

                # Loop through each directory in the list
                for dirname in dirlist:
                    directory = os.path.join(base_filepath, dirname)
                    # Check if the directory is a subdirectory and does not contain 'X_' or 'in_par'
                    if os.path.isdir(directory) and ('X_' or 'in_par') not in dirname:
                        # Recursively call the function to search the subdirectory and add them to the list (ends search when max depth reached)
                        filetype_files += find_buried_filetype_files(directory, filetype, max_depth, current_depth+1)
                        
            # If there is one or more 'parameters/omega/nrg' files, loop through each file in the base filepath
            elif filetype_count > 0:
                filelist = os.listdir(base_filepath)
                filelist.sort()

                for filename in filelist:
                    filepath = os.path.join(base_filepath, filename)
                    
                    # If there is one 'parameters/omega/nrg' file, check if it is the right filetpye then add to list
                    if filetype_count == 1:
                        try:
                            file_checks(filepath, filetype)
                            filetype_files.append(filepath)
                        except:
                            pass

                    # If there are multiple 'parameters/omega/nrg' files, check only onlys with filetpye + '_' (skips pesky parameters.dat files)
                    if filetype_count > 1:
                        try:
                            file_checks(filepath, filetype + '_')
                            filetype_files.append(filepath)
                        except:
                            pass


    if len(filetype_files) == 0:
        raise FileError(f"No files of type {filetype} were found at a depth of {max_depth}. Please try search again.")

    # Return the list of 'parameters/omega/nrg' filepaths
    return filetype_files



def rescale_list(input_list:list, resized_max:float, resized_min:float):

    max_value = max(input_list)
    min_value = min(input_list)

    if min_value==max_value:
        normalized_list = [1]*len(input_list)
    else:
        normalized_list = [(val - min_value) / (max_value - min_value) for val in input_list]
    
    resized_list = [((resized_max - resized_min) * val + resized_min) for val in normalized_list]

    return resized_list