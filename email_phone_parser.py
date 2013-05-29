#!/usr/bin/env python
# try this with this randomly selected url: https://sites.google.com/site/nhcollier/home
from os import remove
from sys import exit, argv, stderr
from optparse import OptionParser
from codecs import open
from urllib import urlopen
from re import findall, I

ENCODING = "utf-8"


def process_url(url_address, email_patterns, phone_patterns):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    source = urlopen(url_address)
    for line in source:
        for pattern in email_patterns:
            I
            matches = findall(pattern, line)
            print matches
            for m in matches:
                email = '%s@%s.%s' % m
                res.append(email)
        for pattern in phone_patterns:
            matches = findall(pattern, line)
            for m in matches:
                tel = '%s-%s-%s' % m
                res.append(tel)
    print res
    for item in res:
        print item


def get_patterns(input_file):
    patterns = []
    input_patterns = open(input_file, 'r', ENCODING)
    for line in input_patterns:
        patterns.append(line)
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
    process_url(url, get_patterns(emails_file), get_patterns(phones_file))

if __name__ == '__main__':
    main()
