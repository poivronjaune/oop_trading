# Utilty functions
import os

def create_storage_folder_and_return_full_file_name(file_path, file_name):
    """Method:
        Create folder if non existent and return full path and filename
    Params:
        file_path: required parameter
        file_name: required parameter
    """
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file_name = os.path.join(file_path, file_name)
    return file_name