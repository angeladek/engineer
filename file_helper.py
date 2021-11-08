import os
import glob

# List files in folder
def list_files(folder, wildcard) :
    try:
        if folder[-1] != '/' or folder[-1] != '/':
            folder = folder + '/'
        file_path = folder + wildcard
        file_list = glob.glob(file_path)
        return file_list
    except:
        print('Error listing files')

# Get file name without path
def get_file_name_without_path(full_file_path):
    try:
        return os.path.basename(full_file_path)
    except:
        print('Error getting file name without path')

# Get file path
def get_file_path(full_file_path):
    try:
        return(os.path.split(full_file_path)[0])
    except:
        print('Error getting file path')

# Get file name without path and with extension
def get_file_name_without_path_and_extension(full_file_path):
    try:
        return os.path.splitext(os.path.basename(full_file_path))[0]
    except:
        print('Error file name without path and with extension')

# Get file name without path and with extension
def get_file_extension(full_file_path):
    try:
        return os.path.splitext(os.path.basename(full_file_path))[1]
    except:
        print('Error file extension')

