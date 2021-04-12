import logging
import time
import os
from utils import get_email_address, get_email_password, get_email_server, get_log_to_file, get_log_file_name, get_log_level, get_sleep_time, get_printer_name
from reading_emails_scripts import get_mail_attachments, get_unseen_emails

attachment_count = 0
received_messages = False

if __name__ == "__main__":

    #First starting logger
    if get_log_to_file():
        print('Starting Mail to Print Service. Events are logged to ' + get_log_file_name())
        logging.basicConfig(filename=get_log_file_name(), format='%(levelname)s (%(asctime)s): %(message)s', datefmt='%d.%m.%Y %H:%M:%S', level=get_log_level())
    else:
        logging.basicConfig(format='%(levelname)s (%(asctime)s): %(message)s', datefmt='%d.%m.%Y %H:%M:%S', level=get_log_level())
        logging.warning('Logging to a file is disabled. Instead, it\'s printed to the console.')
    
    logging.info('Started Mail to Print Service')

    #Loading rest of the environment
    email_address = get_email_address()
    logging.info('Loaded email address: ' + email_address)
    password = get_email_password()
    server = get_email_server()
    logging.debug('Loaded mail server address: ' + server)
    sleep_time = get_sleep_time()
    logging.debug('Loaded sleep time: ' + str(sleep_time) + ' sec')
    printer_name = get_printer_name()
    logging.info('Loaded printer name: ' + printer_name)

    while(True):
        received_messages = False
        logging.debug('Deleting all files in ./attachment-cache/')
        for pdf in os.listdir('./attachment-cache/'):
            os.remove(os.path.join('./attachment-cache/', pdf))

        logging.debug('Checking E-mails')
        messages = get_unseen_emails(email_address, password, server)

        if messages:
            for message_id, message in enumerate(messages):
                attachment_count = 0
                received_messages = True
                logging.debug('Checking for attachments with ending \'.pdf\'.')
                attachments_pdf = get_mail_attachments(message,
                                                lambda x: x.endswith('.pdf'))
                for attachment_id, attachment in enumerate(attachments_pdf):
                    if attachment:
                        attachment_count = attachment_count + 1
                        with open('./attachment-cache/{}'.format(attachment[0]), 'wb') as file:
                            file.write(attachment[1])
                        logging.info('Message #' + str(message_id) + ' has a PDF attachment (' + str(attachment_id) + ')')

                logging.debug('Checking for attachments with ending \'.PDF\'.')
                attachments_PDF = get_mail_attachments(message,
                                lambda x: x.endswith('.PDF'))
                for attachment_id, attachment in enumerate(attachments_PDF):
                    if attachment:
                        with open('./attachment-cache/{}'.format(attachment[0]), 'wb') as file:
                            file.write(attachment[1])
                        logging.info('Message #' + str(message_id) + ' has a PDF attachment (' + str(attachment_count + attachment_id) + ')')
        
        if received_messages:
            num_files = len([f for f in os.listdir('./attachment-cache/')if os.path.isfile(os.path.join('./attachment-cache/', f))])
            logging.info('Printing ' + str(num_files) + ' files')

            files = os.listdir('./attachment-cache/')

            for pdf in files:
                os.system('lp -d ' + printer_name + ' ./attachment-cache/' + pdf)
        
        logging.debug('Going to sleep for ' + str(sleep_time) + ' seconds')
        time.sleep(sleep_time)