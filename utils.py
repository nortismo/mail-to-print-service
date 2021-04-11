import os
from dotenv import load_dotenv

def read_mail_details():
    load_dotenv()

    USER_EMAIL = os.getenv("USER_EMAIL")
    USER_PASSWORD = os.getenv("USER_PASSWORD")
    EMAIL_SERVER = os.getenv("EMAIL_SERVER")
    if USER_EMAIL and USER_PASSWORD and EMAIL_SERVER:
        return USER_EMAIL, USER_PASSWORD, EMAIL_SERVER
    else:
        raise ValueError('Please add a .env file and write the credentials it it, refer to the sample')