import os
from GP_file_functions_V4 import FileError, string_to_list, file_checks


def count_files_in_dir(directory: str, filetype: str) -> int:
    """
    Count the number of files in a directory that have a specific file type.

    Parameters:
    - directory (str): The path to the directory to search in.
    - filetype (str): The file type (parameters, omega, nrg, etc.) to count.

    Returns:
    - int: The number of files in the specified directory that match the given file type.
    """
    # Check if the provided directory exists
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory does not exist: {directory}")
    
    # Check if the provided path is a directory
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"The path given is not a directory: {directory}")

    filetype_count = 0
    
    # Iterate through the files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Check if the current item is a file and if its name starts with the specified file type
        if os.path.isfile(file_path) and filename.startswith(filetype):
            filetype_count += 1

    return filetype_count




import os

def single_path_find_buried_files(input_filepath: str, filetype: str, max_depth: int = 2, current_depth: int = 0) -> list:
    """
    Recursively searches for files with a specified filetype ('parameters/omega/nrg') within a directory and its subdirectories.

    Parameters:
    - filepath (str): The base directory path to start the search.
    - filetype (str): The target filetype (e.g., 'parameters/omega/nrg') to search for.
    - max_depth (int, optional): The maximum depth to search in subdirectories. Default is 2.
    - current_depth (int, optional): Internal parameter to keep track of the current depth during recursive calls.

    Returns:
    - list: A list of filepaths that match the specified filetype.
    """
    # Initialize an empty list to store the filepaths of the 'parameters/omega/nrg' files
    filetype_files = []

    if not os.path.exists(input_filepath):
        raise FileNotFoundError(f"The directory does not exist: {input_filepath}")

    if not isinstance(input_filepath, str):
        raise TypeError("filepath must be a string")

    # Check if the base filepath is a 'parameters/omega/nrg' file and append it to the list
    if filetype in os.path.basename(input_filepath):
        filetype_files.append(input_filepath)
        return filetype_files

    # Count the number of 'parameters/omega/nrg' files in the base filepath
    filetype_count = count_files_in_dir(input_filepath, filetype)

    # If there are no 'parameters/omega/nrg' files and the current depth is less than the maximum depth, continue the search
    if filetype_count == 0 and current_depth <= max_depth:
        for dirname in os.listdir(input_filepath):
            directory = os.path.join(input_filepath, dirname)

            # Check if the directory name does not contain certain substrings, making it not skippable
            dir_not_skippable = all(substr not in dirname for substr in ['X_', 'in_par'])
            if os.path.isdir(directory) and dir_not_skippable:
                filetype_files.extend(single_path_find_buried_files(directory, filetype, max_depth, current_depth + 1))

    # If there is one or more 'parameters/omega/nrg' files, loop through each file in the base filepath
    elif filetype_count > 0:
        for filename in os.listdir(input_filepath):
            new_filepath = os.path.join(input_filepath, filename)
            try:
                single_file = (filetype_count == 1 and filename.startswith(filetype))
                multi_files = (filetype_count > 1 and filename.startswith(filetype + '_'))

                if single_file or multi_files:
                    filetype_files.append(new_filepath)
            except:
                pass
    
    if not filetype_files:
        raise FileNotFoundError(f"No files of type '{filetype}' were found at a depth of {max_depth} for given filepath.")

    return filetype_files



def find_buried_filetypes(base_filepath_list:list, filetype:str, max_depth=2, current_depth=0):
    """
    Recursively searches for a certain filetype ('parameters/omega/nrg' used in code comment example) in a directory and its subdirectories up to a specified maximum depth.
    Returns a list of filepaths for all files found.
    If no files are found at the maximum depth, prints an error message and stops the search.
    """
    base_filepath_list = string_to_list(base_filepath_list)
    # Initialize an empty list to store the filepaths of the 'parameters/omega/nrg' files
    filetype_files = []

    for base_filepath in base_filepath_list:
        filetype_files.extend(single_path_find_buried_files(base_filepath, filetype, max_depth, current_depth))

    return filetype_files




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
        raise FileError(f"No files of type {filetype} were found at a depth of {max_depth}. Please refine search.")

    # Return the list of 'parameters/omega/nrg' filepaths
    return filetype_files
