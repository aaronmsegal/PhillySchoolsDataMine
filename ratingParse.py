import argparse
import csv
import json
import re

valueSets = {}

def clean(toClean):
    return toClean.strip().lower().replace(' ', '_')

def castAndCleanMagic(key, value):
    if 'out of' in value:
        value = value.split('out of')
        value[0] = re.sub('\D', '', value[0])
        value[1] = re.sub('\D', '', value[1])
        value = float(value[0]) / float(value[1])
    else:
        try:
            value = float(value)
        except ValueError:
            if value != '?':
                global valueSets
                if key not in valueSets:
                    valueSets[key]=set()
                valueSets[key].add(value)
    return value


parser = argparse.ArgumentParser()
parser.add_argument('csv', help='File to parse')
parser.add_argument('json', help='File to add to')
args = parser.parse_args()

csv_name = args.csv
json_name = args.json

schools = {}

with open(csv_name, 'r') as csvFile:
    schoolCSV = csv.DictReader(csvFile, delimiter=',')
    for school in schoolCSV:
        schoolName = school.get('School')

        ignoreList = list(['School', 'Rpt Type Long ', 'City', 'Street Address',
            'State', 'Zip Code', 'Phone Number', 'Fax Number', 'Website',
            'Back On Track Pts Poss', 'OSS Pts Earn', 'Back On Track Pts Earn',
            'Clim City Rank ', 'Stay on Track Pts Poss', 'K-2 Rdg Pts Earn',
            'Ach Peer Rank ', 'Ach Score ', 'CC City Rank ', 'CC Peer Rank ',
            'CC Score ', 'Clim Score ', 'Overall Score ', 'Prog Score ',
            'SRC School ID '])

        for i in ignoreList:
            school.pop(i)

        cleanedSchoolDict = {}
        for key in school:
            value = school.get(key)
            if (not value
                or value == 'Not Applicable'
                or  value == 'Data Suppressed'
                or value == 'Insufficient Sample'
                or value == 'Data Not Available'
                or value == 'Insufficient Data'
                or value == 'N/A'):
                value = '?'
            cleanedSchoolDict[clean(key)] = castAndCleanMagic(key, value)

        schools[clean(schoolName)] = cleanedSchoolDict

emptySchool = {}
sampleSchool = schools.itervalues().next()
for k in sampleSchool:
    emptySchool[k]='?'

schoolsJson = None
with open(json_name, 'r') as jsonFile:
    jsonString = jsonFile.read()
    schoolsJson = json.loads(jsonString)
    for schoolName in schoolsJson.keys():
        if schoolName in schools:
            for attribute in schools.get(schoolName).keys():
                if not (attribute in schoolsJson.get(schoolName).keys()): # only add attributes not found in previous file
                    schoolsJson[schoolName][attribute] = schools.get(schoolName).get(attribute)
        else:
            schoolsJson[schoolName] = emptySchool


    with open('output.json', 'w') as outFile:
        json.dump(schoolsJson, outFile, sort_keys = True, indent = 4, ensure_ascii = False)

with open('valueSets.json', 'w') as setFile:
    for key in valueSets:
        valueSets[key] = list(valueSets[key])
    json.dump(valueSets, setFile, sort_keys = True, indent = 4, ensure_ascii = False)
