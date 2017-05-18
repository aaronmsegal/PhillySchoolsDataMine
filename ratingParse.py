import csv
import json

schools = {}

with open('2014_2015_SCHOOL_PROGRESS_REPORT.csv') as schoolFile:
  schoolCSV = csv.DictReader(schoolFile, delimiter=',')
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
            cleanedSchoolDict[key] = value

    schools[schoolName] = cleanedSchoolDict

with open('ratings.json', 'w') as outfile:
    json.dump(schools, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
