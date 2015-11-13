#!/usr/bin/env python
# -*- coding: utf-8 -*-



import sys
import os.path
import hashlib
from fontTools import ttLib

# TODO: check that requested file paths exist
# TODO: expand Python objects within the table values


def main(fontpaths):

    for fontpath in fontpaths:
        tt = ttLib.TTFont(fontpath)
        print("Processing " + fontpath + "...")

        basename = os.path.basename(fontpath)
        outfilepath = basename + "-TABLES.yaml"

        fontdata = read_bin(fontpath)
        hash_digest = hashlib.sha1(fontdata).hexdigest()

        report_header_string = "FILE: " + fontpath + "\n"
        report_header_string += "SHA1: " + hash_digest + "\n---\n\n"

        with open(outfilepath, "w") as writer:
            writer.write(report_header_string)

        for table in tt.keys():
            if len(tt[table].__dict__) > 0:
                table_string = "# " + table + "\n"
                for field in tt[table].__dict__.keys():
                    table_string = table_string + field + ": " + str(tt[table].__dict__[field]) + '\n'
                table_string += "\n\n"
                with open(outfilepath, 'a') as appender:
                            appender.write(table_string)
                print("[✓] " + table)
            else:
                print("[E] " + table)
                table_string = "# " + table + "\n"
                table_string += "--EMPTY--\n\n"
                with open(outfilepath, 'a') as appender:
                            appender.write(table_string)
        print(fontpath + " table report is available in " + outfilepath + "\n")



def read_bin(filepath):
    try:
        with open(filepath, 'rb') as bin_reader:
            data = bin_reader.read()
            return data
    except Exception as e:
        sys.stderr.write("Error: Unable to read file " + filepath + ". " + str(e))


if __name__ == '__main__':
    main(sys.argv[1:])
