from email import message_from_bytes
from imaplib import IMAP4_SSL

def get_unseen_emails(email_address, password, server):
    with IMAP4_SSL(server) as mail_connection:
        mail_connection.login(email_address, password)
        mail_connection.list()
        mail_connection.select('INBOX')
        (retcode, messages) = mail_connection.search(None,
            '(OR (UNSEEN) (FROM your.email@gmail.com))')
        if retcode == 'OK' and messages[0]:
            for index, num in enumerate(messages[0].split()):
                typ, data = mail_connection.fetch(num, '(RFC822)')
                message = message_from_bytes(data[0][1])
                typ, data = mail_connection.store(num, '+FLAGS', '\\Seen')
                yield message

def get_mail_attachments(message, condition_check):
    for part in message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if not part.get('Content-Disposition'):
            continue
        file_name = part.get_filename()
        if condition_check(file_name):
            yield part.get_filename(), part.get_payload(decode=1)