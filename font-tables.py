#!/usr/bin/env python
# -*- coding: utf-8 -*-



import sys
import os.path
import hashlib
from fontTools import ttLib

# TODO: check that requested file paths exist
# TODO: expand Python objects within the table values


def main(fontpaths):
    """The main function creates a YAML formatted report on the OpenType tables in one
    or more fonts included in the fontpaths function parameter."""

    for fontpath in fontpaths:

        # create a fonttools TTFont object using the fontpath
        tt = ttLib.TTFont(fontpath)
        print("Processing " + fontpath + "...")

        # define the outfile path
        basename = os.path.basename(fontpath)
        outfilepath = basename + "-TABLES.yaml"

        # read the font data and create a SHA1 hash digest for the report
        fontdata = read_bin(fontpath)
        hash_digest = hashlib.sha1(fontdata).hexdigest()

        # report strings for file name and SHA1 digest
        report_header_string = "FILE: " + fontpath + "\n"
        report_header_string += "SHA1: " + hash_digest + "\n\n"

        # open outfile write stream, create file, write name + SHA1 header
        with open(outfilepath, "w") as writer:
            writer.write(report_header_string)

        # iterate through the OpenType tables, write table fields in a newline delimited format with YAML syntax
        for table in tt.keys():
            if len(tt[table].__dict__) > 0:
                table_string = table + ": {\n"
                for field in tt[table].__dict__.keys():
                    table_string = table_string + (" "*4) + field + ": " + str(tt[table].__dict__[field]) + ',\n'
                table_string += "}\n\n"
                with open(outfilepath, 'a') as appender:
                            appender.write(table_string)
                print("[✓] " + table)
            else:
                print("[E] " + table)  # indicate missing table data in standard output, do not write to YAML file
        print(fontpath + " table report is available in " + outfilepath + "\n")



def read_bin(filepath):
    """read_bin function reads filepath parameter as binary data and returns raw binary to calling code"""
    try:
        with open(filepath, 'rb') as bin_reader:
            data = bin_reader.read()
            return data
    except Exception as e:
        sys.stderr.write("Error: Unable to read file " + filepath + ". " + str(e))


if __name__ == '__main__':
    main(sys.argv[1:])
