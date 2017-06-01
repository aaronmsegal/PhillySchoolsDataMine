import xml.etree.ElementTree
import json
import sys

def parseXML():
    tree = xml.etree.ElementTree.parse('browseschoolsdata.xml')
    schoolsDict = {}
    schools = tree.findall('school')
    for school in schools:
        schoolAttrDict = {}
        # Load Attributes
        name = school.find('name').text
        schoolType = school.find('type').text
        gsID = school.find('gsId').text
        gsRatingRaw = school.find('gsRating')
        if gsRatingRaw is not None:
            gsRating = gsRatingRaw.text
        else:
            gsRating = "?"
        parentRatingRaw = school.find('parentRating')
        if parentRatingRaw is not None:
            parentRating = parentRatingRaw.text
        else:
            parentRating = "?"
        # Build dictionary
        schoolAttrDict['name'] = name
        schoolAttrDict['gs_id'] = gsID
        schoolAttrDict['type'] = schoolType
        schoolAttrDict['gs_rating'] = gsRating
        schoolAttrDict['parent_rating'] = parentRating
        cleanedName = name.lower().strip().replace(" ", "_")
        schoolsDict[cleanedName] = schoolAttrDict
    # Return JSON
    return json.dumps(schoolsDict)

def combineJsonFiles(filename, internalJsonString):
    # Load External JSON
    with open(filename, 'r') as externalFile:
        externalJsonString = externalFile.read()
        externalJson = json.loads(externalJsonString)
    # Load JSON
    internalJson = json.loads(internalJsonString)
    # Loop through files
    for schoolName in externalJson.keys():
        if schoolName not in internalJson.keys():
            externalJson[schoolName]['name'] = '?'
            externalJson[schoolName]['gs_id'] = '?'
            externalJson[schoolName]['type'] = '?'
            externalJson[schoolName]['gs_rating'] = '?'
            externalJson[schoolName]['parent_rating'] = '?'
        else:
            for attribute in internalJson.get(schoolName, {}).keys():
                if not attribute in externalJson[schoolName].keys(): # only add attributes not found in previous file
                    externalJson[schoolName][attribute] = internalJson[schoolName][attribute]
    # Write new file
    with open('GreatSchools_Combined.json', 'w') as outputFile:
        json.dump(externalJson, outputFile, sort_keys = True, indent = 4, ensure_ascii = False)

def main():
    externalFile = sys.argv[1]
    ratingsJson = parseXML()
    combineJsonFiles(externalFile, ratingsJson)

if __name__ == "__main__":
    main()
