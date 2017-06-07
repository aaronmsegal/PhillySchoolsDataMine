import xml.etree.ElementTree
import json
import sys
import re, math
from collections import Counter

WORD = re.compile(r'\w+')

def parseXML():
    tree = xml.etree.ElementTree.parse('raw_greatSchools_schoolRatings.xml')
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
        cleanedName = cleanedName.replace('_cs','_charter_school')
        schoolsDict[cleanedName] = schoolAttrDict
    # Return JSON
    with open('ratingsDump.json', 'w') as file:
        file.write(json.dumps(schoolsDict, sort_keys=True))

def compareSchoolNames(katSchool, jonSchool):
    # split name into list of words that make up the name
    #name1List = katSchool.split('_')
    #name2List = jonSchool.split('_')
    v1 = text_to_vector(katSchool)
    v2 = text_to_vector(jonSchool)
    #print v1
    #print v2
    cos = get_cosine(v1,v2)
    return cos

    # somehow assign weights to words...

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     text =  re.sub('[^a-zA-Z0-9*_]', '', text)
     words = text.split('_')
     return Counter(words)

def testCosine(filename1, filename2):
    with open(filename1, 'r') as katFile:
        katJsonString = katFile.read()
        katJson = json.loads(katJsonString)

    with open(filename2, 'r') as jonFile:
        jonJsonString = jonFile.read()
        jonJson = json.loads(jonJsonString)

    for katSchoolName in katJson.keys():
        for jonSchoolName in jonJson.keys():
            cosVal = compareSchoolNames(katSchoolName, jonSchoolName)
            if cosVal >= 0.77:
                print katSchoolName
                print jonSchoolName
                print cosVal

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
    #externalFile = sys.argv[1]
    #ratingsJson = parseXML()
    #combineJsonFiles(externalFile, ratingsJson)
    testCosine('step1_schoolFacilities.json','ratingsDump.json')

if __name__ == "__main__":
    main()
