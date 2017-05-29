import json

def writeToArff():
  parsedCombinedJson = {}
  # get dictionaries of all schools from output file
  with open('combined_zip_output.json', 'r') as jsonFile:
    jsonString = jsonFile.read()
    parsedCombinedJson = json.loads(jsonString)

  values = parsedCombinedJson.values() # gets a list of attr:value dictionaries
  attrList = values[0].keys() # gets just the attribute names, note it might not be sorted

  #print type(attrList)
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
      print school
      for i in range(len(attrList)):
        attr = attrList[i]
        print attr
        attrValue = parsedCombinedJson[school][attr]
        print attrValue
        line = attrValue + ', '
        if i == len(attrList)-1:
          line = attrValue + '\n\n'
        arffFile.write(line)

def main():
  writeToArff()

if __name__ == "__main__":
  main()