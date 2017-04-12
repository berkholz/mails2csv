# mails2csv

This project ist for reading mails from an imap server via TLS and converting their headers into a csv format and printing to standard out.

## setup mails2csv

### define headers to export
First you have to define the header fields to export. Find this section in the python code:
```python
# varHeaders = ['Return-path', 'Envelope-to', 'Delivery-date', 'Received', 'To', 'Cc', 'From', 'Subject', 'Mime-Version',
   varHeaders = ['Delivery-date', 'Subject', 'To', 'From']
```

The line which is commented out gives you a brief overview of possible headers. Change the varHeaders variable beneath for your needs and save the python file.

### create mailserver configuration

Copy the .mails2csv-dist file as .mails2csv to your home directory. Under Unix it would be ~/.mails2csv and for Windows it would be %HOMEPATH%\.mails2csv .

You can use a different file as configuration file while setting the command line option *-c* or *--configfile*.

## running mails2csv

To list all available command line option call mails2csv with option *-h*:
```python
mails2csv.py -h
```

As default IMAP folder the INBOX folder is used. To use a different folder you have to call mails2csv with option *-I*:
```python
mails2csv.py -I Sent
# or different child folder
mails2csv.py -I INBOX.subfolder
```

To use a config file other than the default ~/.mails2csv you have to use the option *-c* or *--configfile*:
```python
mails2csv.py -c D:\mail2csv.conf
```

