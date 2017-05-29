from openpyxl import load_workbook
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('infile', help='File to parse')
parser.add_argument('masterfile', help='File containing all JSON data')
args = parser.parse_args()

infile_name = args.infile
masterfile_name = args.masterfile

with open(masterfile_name, 'r') as masterfile:
    data = json.load(masterfile)

wb = load_workbook(infile_name)
grad_rate_by_school_ws = wb['Grad Rate by School']
for row in grad_rate_by_school_ws.rows:
    school_name = row[5].value
    if school_name is not None:
        school_name = school_name.lower().strip().replace(' ', '_')
        school_name = school_name.replace('_cs', '_charter_school')
        school_name = school_name.replace('_hs', '_high_school')
        school_name = school_name.replace('_ms', '_middle_school')
        school_name = school_name.replace('_el_sch', '_elementary_school')
        school_name = school_name.replace('_intrmd_sch', '_intermediate_school')

        if school_name not in data:
            data[school_name] = {}

        data[school_name]['total_grads'] = row[7].value
        data[school_name]['total_cohort'] = row[8].value
        data[school_name]['total_grad_rate'] = row[9].value

with open(masterfile_name, 'w') as masterfile:
    json.dump(data, masterfile, indent=4, sort_keys=True)
