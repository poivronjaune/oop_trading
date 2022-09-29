# Utilty functions
import os
from datetime import datetime, timedelta
from dateutil import parser

def create_storage_folder_and_return_full_file_name(file_path, file_name):
    """Function (Utility):
        Create folder if non existent and return full path and filename
    Params:
        file_path: required parameter
        file_name: required parameter
    """
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file_name = os.path.join(file_path, file_name)
    return file_name

def extract_date(date_param):
    '''Function (Utility):
        Extract the date from a parameter, trying to automatically detect the date format
    Params:
        date_param: required parameter, a string that contains a date
    '''
    try:
        date_val = parser.parse(date_param)
    except Exception:
        date_val = None

    if isinstance(date_param, datetime):
        date_val = date_param

    return date_val    