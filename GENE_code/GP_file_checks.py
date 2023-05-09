import os


def suffix_from_filename(filename):
    # function gets the suffix for a given file
    if '_' in filename:
        suffix = filename[-4:]
    else:
        suffix = '.dat'
    return suffix



def file_check(filepath , filetype):
    # checks that a file is the cited filetype, is a file, and is non-empty
    filename = os.path.basename(filepath)

    check_filetype = filename.startswith(filetype)
    check_file = os.path.isfile(filepath)
    check_nonempty = (os.stat(filepath).st_size != 0)

    check = (check_filetype and check_file and check_nonempty)

    return check