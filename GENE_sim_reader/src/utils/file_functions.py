import os

def suffix_from_filename(filename: str) -> str:
    """
    Extracts the suffix for a given filename.

    Parameters:
    - filename (str): The name of the file.

    Returns:
    - str: The extracted suffix.
    """
    if '_' in filename:
        suffix = filename[-4:]
    else:
        suffix = '.dat'
    return suffix


def switch_suffix_file(old_filepath: str, filetype: str) -> str:
    """
    Switches the suffix of a file path based on the provided file type.

    Parameters:
    - old_filepath (str): The original file path.
    - filetype (str): The desired file type.

    Returns:
    - str: The new file path with the updated suffix.
    """

    check_exists = os.path.exists(old_filepath)
    check_is_file = os.path.isfile(old_filepath)
    
    if not (check_exists and check_is_file):
        raise FileError(f"The file path does not exist or is not a file: {old_filepath}")
    
    old_directory = os.path.dirname(old_filepath)
    old_filename = os.path.basename(old_filepath)
    suffix = suffix_from_filename(old_filename)

    # If suffix has a '.dat', no change is needed; otherwise, prepend an underscore
    mod_suffix = suffix if '.dat' in suffix else '_' + suffix
    new_filepath = os.path.join(old_directory, filetype + mod_suffix)

    # Check that the new filepath exists, is a file, and starts with the given filetype (i.e., parameters)
    file_checks(new_filepath, filetype)

    return new_filepath


class FileError(Exception):
    """
    Custom exception class for file-related errors.
    """
    pass


def file_checks(filepath: str, filetype: str):
    """
    Performs checks on the file path to ensure its existence, is a file, and filename starts with 'filetype'.

    Parameters:
    - filepath (str): The file path to be checked.
    - filetype (str): The expected file type.

    Raises:
    - FileError: If the file path doesn't exist, is not a file, or if the filename doesn't start with the specified filetype.
    """
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
    """
    Converts a string or a list to a list.

    Parameters:
    - string: str or list
        The input string or list.

    Returns:
    - list
        A list containing the elements of the input string or list.
    """
    string_list = []

    # Check if the input is a string
    if isinstance(string, str):
        string_list.append(string)
    # Check if the input is already a list
    elif isinstance(string, list):
        string_list = string
    else:
        # Raise an error for invalid input types
        raise ValueError(f"Given input {string} is a {type(string)} not a string or list type. Please try again.")

    return string_list



def rescale_list(input_list: list, resized_max: float, resized_min: float):
    """
    Rescales a list of values to a new range defined by resized_max and resized_min.

    Parameters:
    - input_list: list
        The input list of values to be rescaled.
    - resized_max: float
        The maximum value of the new range.
    - resized_min: float
        The minimum value of the new range.

    Returns:
    - list
        A list containing the rescaled values.
    """
    max_value = max(input_list)
    min_value = min(input_list)

    # Check if all values in the input list are the same
    if min_value == max_value:
        normalized_list = [1] * len(input_list)
    else:
        # Normalize values to the range [0, 1]
        normalized_list = [(val - min_value) / (max_value - min_value) for val in input_list]

    # Rescale normalized values to the new range
    resized_list = [((resized_max - resized_min) * val + resized_min) for val in normalized_list]

    return resized_list
