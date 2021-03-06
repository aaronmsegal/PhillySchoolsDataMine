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

school_summary_data = {}
wb = load_workbook(infile_name)
summary_by_school_ws = wb['Summary by School-5']
current_county = ''
for row in summary_by_school_ws.rows:
    if row[0].value is not None:
        current_county = row[0].value.strip()
    school_name = row[4].value
    if school_name is not None and current_county == 'Philadelphia':
        school_name = school_name.lower().strip().replace(' ', '_')
        school_name = school_name.replace('_cs', '_charter_school')
        school_name = school_name.replace('_hs', '_high_school')
        school_name = school_name.replace('_ms', '_middle_school')
        school_name = school_name.replace('_el_', '_elementary_')
        school_name = school_name.replace('_intrmd_', '_intermediate_')
        school_name = re.sub('_sch$', '_school', school_name)
        school_name = school_name.replace('_cs-', '_charter_school_at')
        school_name = school_name.replace('_chs', '_charter_high_school')

        school_summary_data[school_name] = {}
        school_summary_data[school_name]['enrollment'] = row[5].value
        school_summary_data[school_name]['male_dropouts'] = row[6].value
        school_summary_data[school_name]['female_dropouts'] = row[7].value
        school_summary_data[school_name]['dropouts'] = row[8].value
        school_summary_data[school_name]['dropout_rate'] = row[9].value

for school_name in data.keys():
    if school_name in school_summary_data:
        for attribute in school_summary_data[school_name].keys():
            data[school_name][attribute] = school_summary_data[school_name][attribute]
    else:
        data[school_name]['enrollment'] = '?'
        data[school_name]['male_dropouts'] = '?'
        data[school_name]['female_dropouts'] = '?'
        data[school_name]['dropouts'] = '?'
        data[school_name]['dropout_rate'] = '?'

with open(masterfile_name, 'w') as masterfile:
    json.dump(data, masterfile, indent=4, sort_keys=True)
