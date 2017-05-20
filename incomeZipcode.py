import csv
import json

def outputIncomeZipCode():
  schoolDict = {}
  incomeDict = {}
  outputDict = {}

  with open('Schools.csv') as schoolFile:
    schoolCSV = csv.DictReader(schoolFile, delimiter=',')
    for school in schoolCSV:
      schoolName = school.get('FACIL_NAME').replace('\r','')
      schoolName = schoolName.replace('\n','')
      schoolDict[schoolName] = school

  with open('median-income-by-zip.csv') as incomeFile:
    incomeCSV = csv.DictReader(incomeFile, delimiter=',')
    for income in incomeCSV:
      incomeDict[income.get('Zip Code')] = income

  for schoolName in schoolDict.keys():
    schoolZip = schoolDict.get(schoolName).get('ZIPCODE')
    for income in incomeDict.keys():
      incomeZip = incomeDict.get(income).get('Zip Code')
      if str(schoolZip).find(str(incomeZip)) >= 0:
        outputDict[schoolName] = {
              'ZIPCODE': incomeZip,
              'POPULATION': incomeDict.get(income).get('Population'),
              'AVG_HOUSEHOLD_INCOME': incomeDict.get(income).get('Avg. Income/H/hold'),
              'NATIONAL_INCOME_RANK': incomeDict.get(income).get('National Rank')
              }
        break

  with open('zipcode_income.json', 'w') as outputFile:
    json.dump(outputDict, outputFile, sort_keys = True)

def combineIncomeZipData(filename):
  parsedIncomeJson = {}
  parsedSchoolJson = {}

  with open('zipcode_income.json', 'r') as jsonFile:
    jsonString = jsonFile.read()
    parsedIncomeJson = json.loads(jsonString)

  with open(filename, 'r') as fileToCombineWith:
    jsonString = fileToCombineWith.read()
    parsedSchoolJson = json.loads(jsonString)

  for schoolName in parsedSchoolJson.keys():
    for attribute in parsedIncomeJson[schoolName].keys():
      if not attribute in parsedSchoolJson[schoolName].keys(): # only add attributes not found in previous file
        parsedSchoolJson[schoolName][attribute] = parsedIncomeJson[schoolName][attribute]

  with open('combined_zip_output.json', 'w') as outputFile:
    json.dump(parsedSchoolJson, outputFile, sort_keys = True)

def main():
  outputIncomeZipCode()
  combineIncomeZipData('school_facilities_output.json')

if __name__ == "__main__":
  main()
