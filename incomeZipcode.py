import csv
import json

def discretize(number):
  bins = ''
  if 0 <= number < 10000:
    bins = '0 - 9,999'
  elif 10000 <= number < 20000:
    bins = '10,000 - 19,999'
  elif 20000 <= number < 30000:
    bins = '20,000 - 29,999'
  elif 30000 <= number < 40000:
    bins = '30,000 - 39,999'
  elif 40000 <= number < 50000:
    bins = '40,000 - 49,999'
  elif 50000 <= number < 60000:
    bins = '50,000 - 59,999'
  elif 60000 <= number < 70000:
    bins = '60,000 - 69,999'
  elif 70000 <= number < 80000:
    bins = '70,000 - 79,999'
  elif 80000 <= number < 90000:
    bins = '80,000 - 89,999'
  elif 90000 <= number < 100000:
    bins = '90,000 - 99,999'
  else:
    bins = '> 100,000'
  return bins

def zip_data_to_json(jsonFile):
  schoolDict = {}
  incomeDict = {}
  outputDict = {}

  with open(jsonFile) as schoolFile:
    jsonString = schoolFile.read()
    schoolDict = json.loads(jsonString)

  csvFile = 'median-income-by-zip.csv'

  with open(csvFile) as incomeFile:
    incomeCSV = csv.DictReader(incomeFile, delimiter=',')
    for income in incomeCSV:
      incomeDict[income.get('Zip Code')] = income

  for schoolName in schoolDict.keys():
    schoolZip = schoolDict.get(schoolName).get('zipcode')
    for income in incomeDict.keys():
      incomeZip = incomeDict.get(income).get('Zip Code')
      if str(schoolZip).find(str(incomeZip)) >= 0:

        population = int(incomeDict.get(income).get('Population'))
        avg_household_income = int(incomeDict.get(income).get('Avg. Income/H/hold'))
        national_income_rank = int(incomeDict.get(income).get('National Rank'))

        outputDict[schoolName] = {
              'zipcode': incomeZip,
              'population': population,
              'avg_household_income': avg_household_income,
              'national_income_rank': national_income_rank
              }
        break

  out = 'zipcode_income_no_disc.json'

  with open(out, 'w') as outputFile:
    json.dump(outputDict, outputFile, sort_keys = True)

def combine_with_zip_json(jsonFile):
  parsedIncomeJson = {}
  parsedSchoolJson = {}

  zipJson = 'zipcode_income_no_disc.json'

  with open(zipJson, 'r') as file:
    jsonString = file.read()
    parsedIncomeJson = json.loads(jsonString)

  with open(jsonFile, 'r') as fileToCombineWith:
    jsonString = fileToCombineWith.read()
    parsedSchoolJson = json.loads(jsonString)

  for schoolName in parsedSchoolJson.keys():
    for attribute in parsedIncomeJson[schoolName].keys():
      if not attribute in parsedSchoolJson[schoolName].keys(): # only add attributes not found in previous file
        parsedSchoolJson[schoolName][attribute] = parsedIncomeJson[schoolName][attribute]

  out = 'combined_zip_output_no_disc.json'

  with open(out, 'w') as outputFile:
    json.dump(parsedSchoolJson, outputFile, sort_keys = True)

def main():
  zip_data_to_json('school_data_v2.json')
  combine_with_zip_json('school_data_v2.json')

if __name__ == "__main__":
  main()
