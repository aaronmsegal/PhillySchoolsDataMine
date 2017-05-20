import argparse
import csv
import json

parser = argparse.ArgumentParser()
parser.add_argument('infile', help='File to parse')
parser.add_argument('outfile', help='File to print results to')
args = parser.parse_args()

infile_name = args.infile
outfile_name = args.outfile

data = {}

with open(infile_name, 'r') as infile:
    reader = csv.DictReader(infile)
    with open(outfile_name, 'w') as outfile:
        for row in reader:
            school_name = row['FACIL_NAME']
            attributes = dict((key.decode('utf-8-sig').rstrip(),value) for key, value in row.iteritems() if key != 'FACIL_NAME' and key != 'OBJECTID' and key != 'FACIL_TELEPHONE' and key != 'LOCATION_ID' and key != 'AUN' and key != 'FACIL_ADDRESS' and key != 'SCHOOL_NUM' and key != 'FACILNAME_LABEL')
            data[school_name] = attributes
        json.dump(data, outfile, indent=4, sort_keys=True)