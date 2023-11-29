import os

from GENE_sim_reader.src.utils.file_functions import string_to_list, file_checks


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



def find_buried_filetypes(input_filepath, filetype: str, max_depth: int = 3):
    """
    Finds files of a specific type buried within a directory structure up to a specified depth.

    Parameters:
    - input_filepath (str): The base filepath or a comma-separated string of filepaths to search.
    - filetype (str): The file type to search for.
    - max_depth (int, optional): The maximum depth to search within the directory structure (default is 3).

    Returns:
    - List[str]: A list of filepaths for the found files of the specified type.

    Raises:
    - FileNotFoundError: If the specified directory does not exist or if no matching files are found.
    - TypeError: If the input_filepath is not a string.

    Example:
    ```python
    result = find_buried_filetypes('/path/to/search', 'omega', max_depth=2)
    print(result)
    ```

    In this example, it searches for files with names containing 'omega' within the specified depth limit.
    """
    
    # Initialize an empty list to store the filepaths of the 'parameters/omega/nrg' files
    filetype_files = []

    # Convert the input_filepath to a list if it's a comma-separated string
    input_filepath_list = string_to_list(input_filepath)

    for path in input_filepath_list:
        # Check if the directory exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"The directory does not exist: {path}")

        # Check if the path is a string
        if not isinstance(path, str):
            raise TypeError(f"Filepath must be a string: {path}")

        # Check if the base filepath is a 'parameters/omega/nrg' file and append it to the list
        if filetype in os.path.basename(path):
            filetype_files.append(path)

        # Walk through the directory structure
        for root, dirs, files in os.walk(path):
            # Exclude directories with specified prefixes
            dirs[:] = [d for d in dirs if not any(d.startswith(prefix) for prefix in ['X_', 'in_par'])]

            # Calculate the depth of the current directory from the starting directory
            current_depth = root[len(path):].count(os.sep)

            # Check if the current depth is within the specified limit
            if current_depth <= max_depth:
                for file in files:
                    
                    #change filetype to be added (parameters vs parameters_) if multiple filetypes are found
                    #this is only necessary for parameters files which can be input "parameters" or output "parameters_"
                    if count_files_in_dir(root, filetype) > 1:
                        modifier = '_'
                    else:
                        modifier = ''
                    
                    # Check if the file starts with the specified filetype
                    if file.startswith(filetype + modifier):
                        filetype_path = os.path.join(root, file)
                        filetype_files.append(filetype_path)

    # Raise an error if no matching files are found
    if not filetype_files:
        raise FileNotFoundError(f"No files of type '{filetype}' were found at a depth of {max_depth} for the given filepath.")
    
    filetype_files.sort()

    # Return the list of matching filepaths
    return filetype_files


