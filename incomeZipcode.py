import csv
import json

def outputIncomeZipCode(filename):
  schoolDict = {}
  incomeDict = {}
  outputDict = {}

  with open(filename) as schoolFile:
    jsonString = schoolFile.read()
    schoolDict = json.loads(jsonString)

  with open('median-income-by-zip.csv') as incomeFile:
    incomeCSV = csv.DictReader(incomeFile, delimiter=',')
    for income in incomeCSV:
      incomeDict[income.get('Zip Code')] = income

  for schoolName in schoolDict.keys():
    schoolZip = schoolDict.get(schoolName).get('zipcode')
    for income in incomeDict.keys():
      incomeZip = incomeDict.get(income).get('Zip Code')
      if str(schoolZip).find(str(incomeZip)) >= 0:
        outputDict[schoolName] = {
              'zipcode': incomeZip,
              'population': incomeDict.get(income).get('Population'),
              'avg_household_income': incomeDict.get(income).get('Avg. Income/H/hold'),
              'national_income_rank': incomeDict.get(income).get('National Rank')
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
  outputIncomeZipCode('school_data.json')
  combineIncomeZipData('school_data.json')

if __name__ == "__main__":
  main()
