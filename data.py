# This package takes care of data
# collection.

import sys
import os
import io
import db
import bswrapper
from urllib2 import urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup
from db import writeLine, kDB, kHeadingNames

# Konstants
kMetaTableName = "vertical listing"
kTableData = "td"
kFirstElem = 0
kCriticalImpacts = "Discuss critical impacts that will occur if the proposal is not implemented:"

# URLS to various sections in the project list.
URLS = [
    "http://bairwmp.org/projects",
    "http://bairwmp.org/projects/folder_tabular_view?b_start:int=100&-C=",
    "http://bairwmp.org/projects/folder_tabular_view?b_start:int=200&-C=",
    "http://bairwmp.org/projects/folder_tabular_view?b_start:int=300&-C="
]


def extractAndLogData(url, index, writer):
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
        addToken(csvString, str(index))

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

        location = metadata[2].strip() + " | " + metadata[3]
        location = location.replace(",", ";").strip()
        addToken(csvString, location)

        locationLatLong = metadata[6].replace(",", " |").strip()
        addToken(csvString, locationLatLong)

        startDate = metadata[7]
        endDate = metadata[8]
        addToken(csvString, startDate)
        addToken(csvString, endDate)

        locationDescr = metadata[9].replace(",", "").strip()
        addToken(csvString, locationDescr)

        '''
        Gather data from the main body
        '''
        projectTypeDescr = splitJoin(extractProjectTypeDescr(bsobj))
        projectTypeDescr = nonAsciiRemove(projectTypeDescr)
        # print projectTypeDescr
        addToken(csvString, projectTypeDescr)

        detailedDescr = splitJoin(extractDetailedDescr(bsobj))
        detailedDescr = nonAsciiRemove(detailedDescr)
        # print detailedDescr
        addToken(csvString, detailedDescr)

        projectNeed = splitJoin(extractProjectNeed(bsobj))
        projectNeed = nonAsciiRemove(projectNeed)
        # print  projectNeed
        addToken(csvString, projectNeed)

        criticalImpacts = splitJoin(extractCriticalImpacts(bsobj))
        criticalImpacts = nonAsciiRemove(criticalImpacts)
        # print criticalImpacts
        addToken(csvString, criticalImpacts)

        benefits = splitJoin(extractProjectBenefits(bsobj))
        benefits = nonAsciiRemove(benefits)
        # print benefits
        addToken(csvString, benefits)

        cost = " "  # extractCost(bsobj)
        addToken(csvString, cost)

        fundingSrc = ""
        addToken(csvString, fundingSrc)

        sponsorAgencies = metadata[1].replace(",", "\n").strip()
        addToken(csvString, sponsorAgencies)

        projectTypeList = extractProjectTypeList(bsobj)

        writeData(csvString, writer)


def extractProjectNeed(bsobj):
    label = bsobj.find(text="Project Need:")
    return label.find_parent('div').get_text().strip()


def extractCriticalImpacts(bsobj):
    label = bsobj.find(text=kCriticalImpacts)
    return label.find_parent('div').get_text().strip()


def extractProjectBenefits(bsobj):
    label = bsobj.find(text="Project Benefits:")
    return label.find_parent('div').get_text().strip()


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
    label = bsobj.find(text="Detailed description:")
    return label.find_parent('div').get_text().strip()


def extractProjectTypeDescr(bsobj):
    label = bsobj.find(text="Project Type Description:")
    return label.find_parent('div').get_text().strip()


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
        print "The document has no abstract section"
        return
    abstractText = abstractArea.findAll(bswrapper.kParagraph);
    if abstractText is None:
        print "No abstract text found"  # The empty string is not None

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
    csvString.append(token)


def splitJoin(str):
    return " ".join(str.split())


def nonAsciiRemove(str):
    return ''.join([i if ord(i) < 128 else ' ' for i in str])


def main():
    initDB(kDB, kHeadingNames)
    urls = getAllProjectURLS()
    index = 0
    f = io.open(kDB, "ab")
    writer = db.csv.writer(f, dialect="dialect", encoding=db.kDefaultEncoding)
    for each in urls:
        if extractAndLogData(each, index, writer) is None:
            index += 1
        else:
            pass
    f.close()


if __name__ == "__main__":
    main()
