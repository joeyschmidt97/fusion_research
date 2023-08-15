import os


def suffix_from_filename(filename:str):
    # function gets the suffix for a given file
    if '_' in filename:
        suffix = filename[-4:]
    else:
        suffix = '.dat'
    return suffix


def file_check(filepath:str , filetype:str):
    # checks that a file is the cited filetype, is a file, and is non-empty
    filename = os.path.basename(filepath)

    check_filetype = filename.startswith(filetype)
    check_is_file = os.path.isfile(filepath)
    check_nonempty = (os.stat(filepath).st_size != 0)

    check = (check_filetype and check_is_file and check_nonempty)
    # returns True or False
    return check


def count_files_in_dir(directory:str , filetype:str):
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
        print('Given input', string, 'is not a string or list type. Please try again')

    return string_list



def find_filetype_files(base_filepath_list:list, filetype:str, max_depth=2, current_depth=0):
    """
    Recursively searches for a certain filetype ('parameter' used in code comment example) in a directory and its subdirectories up to a specified maximum depth.
    Returns a list of filepaths for all files found.
    If no files are found at the maximum depth, prints an error message and stops the search.
    """
    base_filepath_list = string_to_list(base_filepath_list)
    # Initialize an empty list to store the filepaths of the 'parameter' files
    filetype_files = []

    for base_filepath in base_filepath_list:
        # Check if the base filepath is a 'parameters' file
        if filetype in os.path.basename(base_filepath):
            filetype_files.append(base_filepath)
        
        # if path is not already a 'parameter' file then continue searching
        else:
            # Count the number of 'parameter' files in the base filepath
            filetype_count = count_files_in_dir(base_filepath, filetype)
            
            # If there are no 'parameters' files and the current depth is less than the maximum depth, continue the search
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
                        filetype_files += find_filetype_files(directory, filetype, max_depth, current_depth+1)
                        
            # If there is one or more 'parameters' files, loop through each file in the base filepath
            elif filetype_count > 0:
                filelist = os.listdir(base_filepath)
                filelist.sort()

                for filename in filelist:
                    filepath = os.path.join(base_filepath, filename)
                    # If there is one 'parameters' file, check if the file is a 'parameters' file then add to list
                    if filetype_count == 1:
                        if file_check(filepath , filetype):
                            filetype_files.append(filepath)
                    # If there is more than one 'parameter' file, check if the file is a 'parameters_' file then add to list
                    elif filetype_count > 1:
                        if file_check(filepath , filetype + '_'):
                            filetype_files.append(filepath)

    # Return the list of 'parameter' filepaths
    return filetype_files
