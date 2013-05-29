#!/usr/bin/env python
# try this with this randomly selected url: https://sites.google.com/site/nhcollier/home
from os import remove
from sys import exit, argv, stderr
from optparse import OptionParser
from codecs import open
from urllib import urlopen
from re import findall, sub

ENCODING = "utf-8"
DELIMITER = '\\t'

def process_url(url_address, email_patterns, phone_patterns):
    emails = []
    phone_numbers = []
    source = urlopen(url_address)
    for line in source:
        line = line.lower()
        for item in email_patterns:
            pattern = item[0]
            dots = item[1]
            matches = findall(pattern,line)
            if matches:
                for m in matches:
                    user = m[0]
                    domains = sub(dots,'.',m[1])
                    email = user + '@' + domains
                    emails.append(email)
        for pattern in phone_patterns:
            matches = findall(pattern,line)
            if matches:
                for m in matches:
                    phone_numbers.append(m)
    for item in emails:
        print item
    for item in phone_numbers:
        print item


def get_patterns(input_file):
    patterns = []
    input_patterns = open(input_file, 'r', ENCODING)
    for line in input_patterns:
        patterns.append(line.strip())
    input_patterns.close()
    return patterns

def get_email_patterns(input_file, delim=DELIMITER):
    patterns = []
    users = []
    ats = []
    domains = []
    dots = []
#    extra_pattern = '<script>\ ?obfuscate\(.([a-zA-Z0-9\.\-]+).,.([a-zA-Z0-9\.\-]+).\)'
#    patterns.append(extra_pattern)

    input_patterns = open(input_file, 'r', ENCODING)
    for line in input_patterns:
        if line.split(DELIMITER)[0] == 'USER':
            users.append(line.split(DELIMITER)[1].strip())
        if line.split(DELIMITER)[0] == 'DOMAIN':
            domains.append(line.split(DELIMITER)[1].strip())
        if line.split(DELIMITER)[0] == 'AT':
            ats.append(line.split(DELIMITER)[1].strip())
        if line.split(DELIMITER)[0] == 'DOT':
            dots.append(line.split(DELIMITER)[1].strip())
    for user in users:
        for at in ats:
            for domain in domains:
                for dot in dots:
                    pattern = user + at + '((?:' + domain + ')(?:' + dot + '(?:' + domain + '))+)'
                    patterns.append((pattern.lower(), dot))
    input_patterns.close()
    return patterns


def main():
    usage = 'usage: %prog [options] <email_patterns> <phone_patterns> <url>\n'
    usage += '\nthe url must be given completely, as in: http://www.site.com'
    parser = OptionParser(usage = usage)
    parser.add_option("-e", "--encoding", dest = "encoding", default = "utf-8",
                  help = "sets the encoding for the input and output file")
    options, arguments = parser.parse_args()
    if len(arguments) != 3:
        parser.error("incorrect number of arguments")
    if options.encoding:
        ENCODING = options.encoding
    emails_file = arguments[0]
    phones_file = arguments[1]
    url = arguments[2]
    process_url(url, get_email_patterns(emails_file), get_patterns(phones_file))

if __name__ == '__main__':
    main()
