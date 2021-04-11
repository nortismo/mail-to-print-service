import logging
import time
import os
from utils import read_mail_details
from reading_emails_scripts import get_mail_attachments, get_unseen_emails

#TODO: Put sleep time and logging settings to env
sleep_s = 30
attachment_count = 0
received_messages = False
log_to_file = True
log_level = logging.INFO

if __name__ == "__main__":

    if log_to_file:
        #TODO: Make log file name configurable
        logging.basicConfig(filename='myMailPrinter.log', format='%(levelname)s (%(asctime)s): %(message)s', datefmt='%d.%m.%Y %H:%M:%S', level=log_level)
    else:
        logging.basicConfig(format='%(levelname)s (%(asctime)s): %(message)s', datefmt='%d.%m.%Y %H:%M:%S', level=log_level)
    logging.info('Started Mail to Print Service')

    logging.debug('Read mail server details from .env')
    email_address, password, server = read_mail_details()

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
                #TODO: Put printer name into env
                os.system('lp -d HP_Color_LaserJet_MFP_M281fdw_605953_ ./attachment-cache/' + pdf)
        
        logging.debug('Going to sleep for ' + str(sleep_s) + ' seconds')
        time.sleep(sleep_s)