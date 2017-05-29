from openpyxl import load_workbook
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('infile', help='File to parse')
parser.add_argument('masterfile', help='File containing all JSON data')
args = parser.parse_args()

infile_name = args.infile
masterfile_name = args.masterfile

with open(masterfile_name, 'rw') as masterfile:
    data = json.load(masterfile)

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
        school_name = school_name.replace('_el_sch', '_elementary_school')
        school_name = school_name.replace('_intrmd_sch', '_intermediate_school')

        if school_name not in data:
            data[school_name] = {}

        data[school_name]['enrollment'] = row[5].value
        data[school_name]['male_dropouts'] = row[6].value
        data[school_name]['female_dropouts'] = row[7].value
        data[school_name]['dropouts'] = row[8].value
        data[school_name]['dropout_rate'] = row[9].value

with open(masterfile_name, 'w') as masterfile:
    json.dump(data, masterfile, indent=4, sort_keys=True)
