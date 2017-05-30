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

with open(masterfile_name, 'r') as masterfile:
    data = json.load(masterfile)

grad_rate_data = {}
wb = load_workbook(infile_name)
grad_rate_by_school_ws = wb['Grad Rate by School']
for row in grad_rate_by_school_ws.rows:
    school_name = row[5].value
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

        grad_rate_data[school_name] = {}
        grad_rate_data[school_name]['total_grads'] = row[7].value
        grad_rate_data[school_name]['total_cohort'] = row[8].value
        grad_rate_data[school_name]['total_grad_rate'] = row[9].value

for school_name in data.keys():
    if school_name in grad_rate_data:
        for attribute in grad_rate_data[school_name].keys():
            data[school_name][attribute] = grad_rate_data[school_name][attribute]
    else:
        data[school_name]['total_grads'] = '?'
        data[school_name]['total_cohort'] = '?'
        data[school_name]['total_grad_rate'] = '?'

with open(masterfile_name, 'w') as masterfile:
    json.dump(data, masterfile, indent=4, sort_keys=True)
