from openpyxl import load_workbook
import argparse
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument('infile', help='File to parse')
parser.add_argument('masterfile', help='File containing all JSON data')
args = parser.parse_args()

infile_name = args.infile
masterfile_name = args.masterfile

with open(masterfile_name, 'rw') as masterfile:
    data = json.load(masterfile)

wb = load_workbook(infile_name)
lep_by_school_ws = wb['Page1-1']
for row in lep_by_school_ws.rows:
    school_name = row[3].value
    if school_name is not None:
        school_name = school_name.lower().strip().replace(' ', '_')
        school_name = school_name.replace('_cs', '_charter_school')
        school_name = school_name.replace('_hs', '_high_school')
        school_name = school_name.replace('_ms', '_middle_school')
        school_name = school_name.replace('_el_', '_elementary_')
        school_name = school_name.replace('_intrmd_', '_intermediate_')
        school_name = re.sub('_sch$', '_school', school_name)
        school_name = school_name.replace('_cs-', '_charter_school_at')
        school_name = school_name.replace('_chs', '_charter_high_school')

        if school_name not in data:
            data[school_name] = {}
        data[school_name]['lep_students'] = row[4].value

with open(masterfile_name, 'w') as masterfile:
    json.dump(data, masterfile, indent=4, sort_keys=True)
