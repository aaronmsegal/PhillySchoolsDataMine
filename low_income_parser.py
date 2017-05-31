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

lip_school_data = {}
wb = load_workbook(infile_name)
lip_by_school_ws = wb['1415 LIP by School']
current_county = ''
for row in lip_by_school_ws.rows:
    school_name = row[4].value
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

        lip_school_data[school_name] = {}
        lip_school_data[school_name]['enrollment'] = row[5].value
        lip_school_data[school_name]['low_income_enrollment'] = row[6].value
        lip_school_data[school_name]['percent_low_income_enrollment'] = row[7].value

for school_name in data.keys():
    if school_name in lip_school_data:
        for attribute in lip_school_data[school_name].keys():
            data[school_name][attribute] = lip_school_data[school_name][attribute]
    else:
        data[school_name]['enrollment'] = '?'
        data[school_name]['low_income_enrollment'] = '?'
        data[school_name]['percent_low_income_enrollment'] = '?'

with open(masterfile_name, 'w') as masterfile:
    json.dump(data, masterfile, indent=4, sort_keys=True)
