import os
import logging
from dotenv import load_dotenv

def get_email_address():
    load_dotenv()
    email_address = os.getenv("USER_EMAIL")
    if email_address:
        return email_address
    else:
        raise ValueError('Please add your email address in the .env file')

def get_email_password():
    load_dotenv()
    email_password = os.getenv("USER_PASSWORD")
    if email_password:
        return email_password
    else:
        raise ValueError('Please add your email password in the .env file')

def get_email_server():
    load_dotenv()
    email_server = os.getenv("EMAIL_SERVER")
    if email_server:
        return email_server
    else:
        raise ValueError('Please add your email server in the .env file')

def get_log_to_file():
    load_dotenv()
    log_to_file = os.getenv("LOG_TO_FILE")
    if log_to_file:
        return True if log_to_file == 'True' or log_to_file == 'true' else False
    else:
        raise ValueError('Please add set \'LOG_TO_FILE\' to True or False in the file .env.')

def get_log_file_name():
    load_dotenv()
    log_file_name = os.getenv("LOG_FILE")
    if log_file_name:
        return log_file_name
    else:
        raise ValueError('Please add a name for the logfile in the .env file')

def get_log_level():
    load_dotenv()
    log_level_string = os.getenv("LOG_LEVEL")
    if log_level_string:
        if log_level_string == 'CRITICAL': return logging.CRITICAL 
        if log_level_string == 'ERROR': return logging.ERROR 
        if log_level_string == 'WARNING': return logging.WARNING 
        if log_level_string == 'INFO': return logging.INFO 
        if log_level_string == 'DEBUG': return logging.DEBUG 
        print('wrong')
    else:
        raise ValueError('Please add the log level in the .env file')

def get_sleep_time():
    load_dotenv()
    sleep_time = os.getenv("SLEEP_TIME")
    if sleep_time:
        return int(sleep_time)
    else:
        raise ValueError('Please set the option \'SLEEP_TIME\' in the .env file')

def get_printer_name():
    load_dotenv()
    printer_name = os.getenv("PRINTER_NAME")
    if printer_name:
        return printer_name
    else:
        raise ValueError('Please add a printer name in the .env file')