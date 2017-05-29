import argparse
import csv
import json

def clean(toClean):
    return toClean.strip().lower().replace(' ', '_')

parser = argparse.ArgumentParser()
parser.add_argument('csv', help='File to parse')
parser.add_argument('json', help='File to add to')
args = parser.parse_args()

csv_name = args.csv
json_name = args.json

schools = {}

with open(csv_name, 'r') as csvFile:
    schoolCSV = csv.DictReader(csvFile)
    for school in schoolCSV:
        schoolName = school.get('School')
        school.pop('School')
        school.pop('Rpt Type Long ')
        school.pop('City')
        school.pop('Street Address')
        school.pop('State')
        school.pop('Zip Code')
        school.pop('Phone Number')
        school.pop('Fax Number')
        school.pop('Website')

        cleanedSchoolDict = {}
        for key in school:
            value = school.get(key)
            if (value != 'Not Applicable'
                and  value != 'Data Suppressed'
                and value != 'Insufficient Sample'
                and value != 'N/A'):
                cleanedSchoolDict[clean(key)] = value

        schools[clean(schoolName)] = cleanedSchoolDict

with open(json_name, 'r+') as jsonFile:
    jsonString = jsonFile.read()
    schoolsJson = json.loads(jsonString)
    for schoolName in schoolsJson.keys():
        if schoolName in schools:
            for attribute in schools.get(schoolName).keys():
                if not (attribute in schoolsJson.get(schoolName).keys()): # only add attributes not found in previous file
                    schoolsJson[schoolName][attribute] = schools.get(schoolName).get(attribute)

    jsonFile.seek(0)
    json.dump(schoolsJson, jsonFile, sort_keys = True, indent = 4, ensure_ascii = False)
    jsonFile.truncate()
