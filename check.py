#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import argparse
import glob
import fileinput
import random
import string
import re

__stamp = ''.join(random.choice(string.ascii_uppercase + string.digits)
                  for _ in range(32))

test_pattern = r"^\s*/\*(.+)\*/\s*$"
test_format_str = "DBG_HELPER {}_{}"

dbg_pattern = r".*\(DBG_HELPER (.+?)\)"
dbg_format_str = "dbg(DBG_PRINT, \"({}){}\\n\");"
dbg_str_pattern = r".*dbg\(DBG_PRINT, \"\(DBG_HELPER (.+?)\).*\)"


def dbg(inf):
    index = 0
    files = glob.glob(inf)
    print "Start preprocess {} files:".format(len(files))
    print files
    if not files:
        print "Finished!"
        return
    for line in fileinput.input(files, inplace=True):
        m = re.match(test_pattern, line)
        if m:
            tmp = m.group(1).strip()
        if not m or not tmp.startswith("NEED CHECK"):
            print line,
        else:
            if tmp[10:1] == ":":
                restStr = tmp[10:]
            else:
                restStr = ''
            leading = line.find("/*")
            test_str = test_format_str.format(__stamp, index)
            dbg_str = dbg_format_str.format(test_str, restStr)
            print ' ' * leading + dbg_str
            index += 1
    print "Finished!"


def check(check, c, tag):
    dbg_map = set()
    count = 0
    with open(check, 'r') as f:
        for line in f:
            m = re.match(dbg_pattern, line)
            if m:
                dbg_map.add(m.group(1))
    print "Found {} ouput dbg message in record".format(len(dbg_map))
    files = glob.glob(c)
    print "Start matching %d files:".format(len(files))
    print files
    for line in fileinput.input(files, inplace=True):
        m = re.match(dbg_str_pattern, line)
        if m:
            tmp = m.group(1)
            if tmp in dbg_map:
                print line.replace("DBG_HELPER " + tmp, tag),
                dbg_map.remove(tmp)
            else:
                print line,
                count += 1
        else:
            print line,
    print "Task finished!"
    print "{} unmatched dbg message in weenix record".format(len(dbg_map))
    print "C files still have {} unmatched dbg message".format(count)


if __name__ == '__main__':
    usage = """
    %(prog)s [--help|-h]
    %(prog)s --preprocess=<files>
    %(prog)s --check=<record> --file=<cfiles> --tag=<tag>
    """
    parser = argparse.ArgumentParser(description='process', usage=usage)

    parser.add_argument('-p', '--preprocess', dest='prefile',
                        help='files that are needed to be preprocessed')
    parser.add_argument('-c', '--check', dest='weenixRecord',
                        help='weenix record log ')
    parser.add_argument('-f', '--file', dest='cfile',
                        help='c files')
    parser.add_argument('-t', '--tag', dest='tag',
                        help='grading tag')
    args = parser.parse_args()

    if args.prefile:
        dbg(args.prefile)
    elif args.weenixRecord and args.cfile and args.tag:
        check(args.weenixRecord, args.cfile, args.tag)
    else:
        parser.parse_args(["-h"])
