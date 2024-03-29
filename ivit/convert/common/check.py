import logging, os

MAIN_PATH = "./ivit/convert"

def check_model(path:str, filetype:str):
    # Check model is exist
    if os.path.exists(path):
        logging.info('-----The {} is converted.'.format(filetype))
        return True
    else:
        logging.error('-----The {} fails to convert.'.format(filetype))
        return False