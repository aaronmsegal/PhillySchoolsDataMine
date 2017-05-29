import json

def writeToArff(filename):
  parsedCombinedJson = {}
  # get dictionaries of all schools from output file
  with open(filename, 'r') as jsonFile:
    jsonString = jsonFile.read()
    parsedCombinedJson = json.loads(jsonString)

  values = parsedCombinedJson.values() # gets a list of attr:value dictionaries
  attrList = values[0].keys() # gets just the attribute names, note it might not be sorted

  with open('schools.arff', 'w') as arffFile:
    # write comments if we want to

    # write relation
    arffFile.write('@relation schools\n\n')

    # write attributes
    for attr in attrList:
      line = '@attribute ' + attr + "\n"
      arffFile.write(line)

    # write data
    arffFile.write('@data\n')
    for school in parsedCombinedJson:
      for i in range(len(attrList)):
        attr = attrList[i]
        attrValue = parsedCombinedJson[school][attr]
        line = attrValue + ', '
        if i == len(attrList)-1:
          line = attrValue + '\n\n'
        arffFile.write(line)

def main():
  writeToArff('combined_zip_output.json')

if __name__ == "__main__":
  main()