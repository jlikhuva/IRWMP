# This package takes care of data
# collection.
import sys
import os
import io
import re
import db
import bswrapper
from urllib2 import urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup
# import progressbar as pb
# from  progressbar import Bar, Percentage
from db import writeLine, kDB, kHeadingNames
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

# from concurrent.futures import ProcessPoolExecutor
# import concurrent.futures
# import time

# Konstants
kMetaTableName = "vertical listing"
kTableData = "td"
kFirstElem = 0
kCriticalImpacts = "Discuss critical impacts that will occur if the proposal is not implemented:"
kErrLogFile = "errors.txt"
ProjectList = []

# URLS to various sections in the project list.
URLS = [
    "http://bairwmp.org/projects",
    "http://bairwmp.org/projects/folder_tabular_view?b_start:int=100&-C=",
    "http://bairwmp.org/projects/folder_tabular_view?b_start:int=200&-C=",
    "http://bairwmp.org/projects/folder_tabular_view?b_start:int=300&-C="
]


def extractAndLogData(url, writer):
    html = bswrapper.fetchHTML(url)
    bsobj = bswrapper.generateBeautifulSoupObject(html)
    if bsobj is None:
        print "Could not create BeautifulSoup Object. Abort"
        return 0

    title = bswrapper.extractHeading(bsobj)  # should log this
    if title is None:
        return 0
    else:
        csvString = []
        # addToken(csvString, str(index))

        title = nonAsciiRemove(splitJoin(title))
        addToken(csvString, title)

        abstract = extractAbstract(bsobj)  # should log this in abstract.txt
        if abstract is None:
            return 0
        abstract = nonAsciiRemove(splitJoin(abstract))
        addToken(csvString, abstract.strip())

        '''
        Extract individual metadatum, removing whitespace and commas.
        '''
        metadata = extractMetadata(bsobj)
        if metadata is None:
            return 0

        # location = '''metadata[2].strip() + " | " + '''metadata[3]
        location = metadata[3]
        location = location.replace(",", ";").strip()
        location = nonAsciiRemove(splitJoin(location))
        addToken(csvString, location)

        locationLatLong = nonAsciiRemove(metadata[6].replace(",", " |").strip())
        addToken(csvString, locationLatLong)

        startDate = metadata[7]
        endDate = metadata[8]
        addToken(csvString, startDate)
        addToken(csvString, endDate)

        locationDescr = metadata[9].replace(",", "").strip()
        locationDescr = nonAsciiRemove(splitJoin(locationDescr))
        addToken(csvString, locationDescr)

        '''
        Gather data from the main body
        '''
        projectTypeDescr = splitJoin(extractProjectTypeDescr(bsobj))
        projectTypeDescr = nonAsciiRemove(projectTypeDescr)
        addToken(csvString, projectTypeDescr)

        detailedDescr = splitJoin(extractDetailedDescr(bsobj))
        detailedDescr = nonAsciiRemove(detailedDescr)
        addToken(csvString, detailedDescr)

        projectNeed = splitJoin(extractProjectNeed(bsobj))
        projectNeed = nonAsciiRemove(projectNeed)
        addToken(csvString, projectNeed)

        criticalImpacts = splitJoin(extractCriticalImpacts(bsobj))
        criticalImpacts = nonAsciiRemove(criticalImpacts)
        addToken(csvString, criticalImpacts)

        benefits = splitJoin(extractProjectBenefits(bsobj))
        benefits = nonAsciiRemove(benefits)
        addToken(csvString, benefits)

        # cost = " "  # extractCost(bsobj)
        # addToken(csvString, cost)

        # fundingSrc = ""
        # addToken(csvString, fundingSrc)

        sponsorAgencies = metadata[1].replace(",", "\n").strip()
        addToken(csvString, sponsorAgencies)

        projectTypeList = extractProjectTypeList(bsobj)
        csvString = csvString + getProjectTypeBitset(projectTypeList)
        writeData(csvString, writer)


def getProjectTypeBitset(list):
    # 'Drinking Water Supply?',
    # 'Water Quality Improvement?',
    # 'Water Reuse/Recycling?',
    # 'Stormwater Improvements?',
    # 'Groundwater Benefits?',
    # 'Infiltration?',
    # 'Habitat Protection and Restoration?',
    # 'Flood Protection?'
    bitset = [0, 0, 0, 0, 0, 0, 0, 0]
    for each in list:
        list.remove(each)
        each = nonAsciiRemove(each)
        list.append(each)
    if db.kHeadingNames[13] in list:
        bitset[0] = 1
    if db.kHeadingNames[14] in list:
        bitset[1] = 1
    if db.kHeadingNames[15] in list:
        bitset[2] = 1
    if db.kHeadingNames[16] in list:
        bitset[3] = 1
    if db.kHeadingNames[17] in list:
        bitset[4] = 1
    if db.kHeadingNames[18] in list:
        bitset[5] = 1
    if db.kHeadingNames[19] in list:
        bitset[6] = 1
    if db.kHeadingNames[20] in list:
        bitset[7] = 1
    return bitset


def extractProjectNeed(bsobj):
    titleStr = 'Project Need:'
    label = bsobj.find(text=titleStr)
    text = label.find_parent('div').get_text().strip()
    return text[len(titleStr):]


def extractCriticalImpacts(bsobj):
    label = bsobj.find(text=kCriticalImpacts)
    return label.find_parent('div').get_text().strip()[len(kCriticalImpacts):]


def extractProjectBenefits(bsobj):
    titleStr = "Project Benefits:"
    subtitles = ['i. Water Supply (conservation, recycled water, groundwater recharge, surface storage, etc.)',
                 'ii. Water Quality',
                 'iii. Flood and Stormwater Management',
                 'iv. Resource Stewardship (watershed management, habitat protection and restoration, recreation, open space, etc.)']
    label = bsobj.find(text=titleStr)
    str = label.find_parent('div').get_text().strip()[len(titleStr):]
    for each in subtitles:
        str = re.sub(each, "", str)
    return str


def extractCost(bsobj):
    label = bsobj.find(text="Capital Costs")
    print label.find_parent('div').get_text().strip


def extractProjectTypeList(bsobj):
    items = []
    wrapperList = bsobj.findAll('input', {'checked': 'checked'})
    for each in wrapperList:
        items.append(each.find_parent('div').get_text().strip())
    return items


def extractDetailedDescr(bsobj):
    titleStr = "Detailed description:"
    label = bsobj.find(text=titleStr)
    return label.find_parent('div').get_text().strip()[len(titleStr):]


def extractProjectTypeDescr(bsobj):
    titleStr = "Project Type Description:"
    label = bsobj.find(text=titleStr)
    return label.find_parent('div').get_text().strip()[len(titleStr):]


def extractMetadata(bsobj):
    metadatalist = []
    table = bsobj.find("table", {"class": kMetaTableName})
    if table is None:
        print "We seem to have a sub-folder"
        return

    data = table.findAll(kTableData)
    for each in data:
        metadatalist.append(each.get_text())
    return metadatalist


def extractAbstract(bsobj):
    abstractArea = bsobj.find("div", {"class": bswrapper.kFieldClass})
    if abstractArea is None:
        "The document has no abstract section"
        return
    abstractText = abstractArea.findAll(bswrapper.kParagraph)
    if abstractText is None:
        print "No abstract text found"  # The empty string is not None
        return

    if len(abstractText) == 0:
        abst = bsobj.find(bswrapper.kParagraph, {"class": "documentDescription"})
        if abst is None:
            print "abstract encoded differently"
            return
        return abst.get_text()

    return abstractText[kFirstElem].get_text()


# Returns a list of all the URLS to individual projects.
def getAllProjectURLS():
    urlList = []
    for each in URLS:
        html = bswrapper.fetchHTML(each)
        bsObject = bswrapper.generateBeautifulSoupObject(html)
        urlList += bswrapper.getProjectUrls(bsObject)
    return urlList


# Initializes the .csv file by writing the headers.
def initDB(dbName, headers):
    writeLine(dbName, headers, "Writing CSV headers")


def writeData(data, csvWriter):
    csvWriter.writerow(data)


def addToken(csvString, token):
    token = token.replace(",", "")
    token += " "
    csvString.append(token.lower())


def splitJoin(str):
    return " ".join(str.split())


def nonAsciiRemove(str):
    return ''.join([i if ord(i) < 128 else '' for i in str])


def extractLinks_Recursive():
    urlList = []
    for each in URLS:
        html = bswrapper.fetchHTML(each)
        bsobj = bswrapper.generateBeautifulSoupObject(html)
        ls = bsobj.findAll("tr", {"class": "even"})
        ls += bsobj.findAll("tr", {"class": "odd"})

        if len(ls) == 0 or ls is None:
            continue

        for wrapper in ls:
            sls = wrapper.findAll("td")

            url = sls[0].find("a").get("href")
            title = sls[0].get_text().strip()
            secondEntry = sls[1].get_text()
            # print title
            # print url
            # print "Project Type is " + secondEntry
            if secondEntry == "Project":
                # print"I'm adding it"
                urlList.append(url)
                ProjectList.append(title)
            elif secondEntry == "Folder":
                URLS.append(url)
    return urlList


def main():
    initDB(kDB, kHeadingNames)
    urls = extractLinks_Recursive()  # getAllProjectURLS()

    index = 0
    # f = io.open(kDB, "ab")
    # errfile = io.open(kErrLogFile, "w")
    ls = db.createWriter(kDB, db.kDefaultAppendFmt)

    #
    # with ThreadPoolExecutor(max_workers = 5) as executor:
    #     futureResults = {executor.submit(extractAndLogData, url, ls[0]):url for url in urls}

    for each in urls:
        if extractAndLogData(each, ls[0]) is None:
            index += 1
        else:
            pass
        # print  index
    ls[1].close()
    # errfile.close()


if __name__ == "__main__":
    main()
