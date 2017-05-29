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
        gsRatingRaw = school.find('gsRating')
        if gsRatingRaw is not None:
            gsRating = gsRatingRaw.text
        else:
            gsRating = "No GreatSchools Rating"
        parentRatingRaw = school.find('parentRating')
        if parentRatingRaw is not None:
            parentRating = parentRatingRaw.text
        else:
            parentRating = "No Parent Rating"
        # Build dictionary
        schoolAttrDict['name'] = name
        schoolAttrDict['type'] = schoolType
        schoolAttrDict['gsRating'] = gsRating
        schoolAttrDict['parentRating'] = parentRating
        cleanedName = name.lower().strip()
        schoolsDict[cleanedName] = schoolAttrDict
        # Print Attributes
        #print name
        #print "GS Rating: " + gsRating
        #print "Parent Rating " + parentRating
        #print ""
    # Print JSON
    return json.dumps(schoolsDict)

def combineJsonFiles(filename, internalJsonString):

    with open(filename, 'r') as externalFile:
        externalJsonString = externalFile.read()
        externalJson = json.loads(externalJsonString)

    internalJson = json.loads(internalJsonString)
    for schoolName in internalJson.keys():
        for attribute in externalJson.get(schoolName, {}).keys():
            if not attribute in internalJson[schoolName].keys(): # only add attributes not found in previous file
                internalJson[schoolName][attribute] = externalJson[schoolName][attribute]

    with open('combined.json', 'w') as outputFile:
        json.dump(internalJson, outputFile, sort_keys = True)

def main():
    externalFile = sys.argv[1]
    ratingsJson = parseXML()
    combineJsonFiles(externalFile, ratingsJson)

if __name__ == "__main__":
    main()
