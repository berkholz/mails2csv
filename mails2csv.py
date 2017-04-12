# https://pymotw.com/2/imaplib/
# https://gist.github.com/robulouski/7441883
# https://docs.python.org/2/library/imaplib.html
import email
from email.parser import Parser
import imaplib

import sys
import os

# https://docs.python.org/2/library/configparser.html
import ConfigParser

# http://www.tutorialspoint.com/python/python_command_line_arguments.htm
import getopt

# https://docs.python.org/2/library/argparse.html#module-argparse
import argparse

from mailbox import _Mailbox


class Configuration:
    def __init__(self, configfile):
        config = ConfigParser.ConfigParser()
        config.read([os.path.expanduser(configfile)])
        self.mailservername = config.get("mailserver", "servername")
        self.mailserverport = config.getint("mailserver", "serverport")
        self.mailserverusername = config.get("mailserver", "username")
        self.mailserverpassword = config.get("mailserver", "password")
        self.separator = config.get("general", "separator")

    def printSettings(self):
        print self.mailserverusername + "@" + self.mailservername + ":" + str(self.mailserverport)
        print self.separator

################################## main #####################################

# command line arguments
parser = argparse.ArgumentParser(description='Save mail headers as csv.')
parser.add_argument('--configfile', '-c', type=str, help="Config file with settings of the mailserver connection.",
                    default="~/.mails2csv")
parser.add_argument('--imapfolder', '-I', type=str, help="Folder on IMAP server to look mails for.",
                    default="INBOX")
args = parser.parse_args()

# reading mailserver settings from ini file
config = Configuration(args.configfile)
config.printSettings()

mailConnection = imaplib.IMAP4_SSL(config.mailservername)

try:
    mailConnection.login(config.mailserverusername, config.mailserverpassword)
    print "Login success."
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "
    sys.exit(1)

mailConnection.select(args.imapfolder, True)

typ, data = mailConnection.search(None, 'ALL')

# define list of headers to export
# varHeaders = ['Return-path', 'Envelope-to', 'Delivery-date', 'Received', 'To', 'Cc', 'From', 'Subject', 'Mime-Version',
varHeaders = ['Delivery-date', 'Subject', 'To', 'From']

# print out header titles
for header in varHeaders:
    sys.stdout.write(header)
    sys.stdout.write(config.separator)
print

for num in data[0].split():
    typ, data = mailConnection.fetch(num, '(RFC822)')
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1])
            # print all defined headers defined in varHeaders for current mail
            for header in varHeaders:
                sys.stdout.write(msg[header])
                sys.stdout.write(config.separator)
            print

mailConnection.close()
mailConnection.logout()
