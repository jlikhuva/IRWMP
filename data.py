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

# URLS to various sections in the project list.
URLS = [
    "http://bairwmp.org/projects",
    "http://bairwmp.org/projects/folder_tabular_view?b_start:int=100&-C=",
    "http://bairwmp.org/projects/folder_tabular_view?b_start:int=200&-C=",
    "http://bairwmp.org/projects/folder_tabular_view?b_start:int=300&-C="
]

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


# Takes in a single url and extract and
# stores all the "important" data about
# the given project.
def extractAndLogData(url, index, writer):
    html = bswrapper.fetchHTML(url)
    bsobj = bswrapper.generateBeautifulSoupObject(html)
    if bsobj is None:
        print "Could not create BeautifulSoup Object. Abort"
        index -= 1 #This method sucks. Change it.
        return

    title = bswrapper.extractHeading(bsobj) # should log this
    if title is None:
        index -= 1
        return
    else:
        csvString = []
        addToken(csvString, str(index))
        addToken(csvString, title)

        abstract = extractAbstract(bsobj) # should log this in abstract.txt
        if abstract is None:
            index -= 1
            return
        addToken(csvString, abstract)
        '''
        Extract individual metadatum, removing whitespace and commas.
        '''
        metadata = extractMetadata(bsobj)
        if metadata is None:
            index -= 1
            return

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

        projectTypeDescr = ""
        addToken(csvString, projectTypeDescr)

        detailedDescr = ""
        addToken(csvString, detailedDescr)

        projectNeed = ""
        addToken(csvString, projectNeed)

        criticalImpacts = ""
        addToken(csvString, criticalImpacts)

        benefits = ""
        addToken(csvString, benefits)

        cost = ""
        addToken(csvString, cost)

        fundingSrc = ""
        addToken(csvString, fundingSrc)

        sponsorAgencies = metadata[1].replace(",", "\n").strip()
        addToken(csvString, sponsorAgencies)

        print "Writing CSV Rows"
        writeData(csvString, writer)
        # bswrapper.addProjectNameToProjectList(title.strip())

def writeData(data, csvWriter):
    csvWriter.writerow(data)


def addToken(csvString, token):
    #token.replace("\"", "") # Remove quotations
    token +=" "
    csvString.append(token)

def extractMetadata(bsobj):
    metadatalist = []
    table = bsobj.find("table", {"class":kMetaTableName})
    if table is None:
        print "We seem to have a sub-folder"
        return

    data = table.findAll(kTableData)
    for each in data:
        metadatalist.append(each.get_text())
    return metadatalist

def extractAbstract(bsobj):
    abstractArea = bsobj.find("div", {"class":bswrapper.kFieldClass})
    if abstractArea is None:
        print "The document has no abstract section"
        return
    abstractText = abstractArea.findAll(bswrapper.kParagraph);
    if abstractText is None:
        print "No abstract text found" #The empty string is not None

    if len(abstractText) == 0:
        abst = bsobj.find(bswrapper.kParagraph, {"class":"documentDescription"})
        if abst == None:
            print "abstract encoded differently"
            return
        return abst.get_text()

    return abstractText[kFirstElem].get_text()
    
def main():
    initDB(kDB, kHeadingNames)
    urls = getAllProjectURLS()
    # removeImageLinks(urls)
    index = 0
    f = io.open(kDB, "ab")
    writer = db.csv.writer(f,dialect="dialect", encoding = db.kDefaultEncoding)
    for each in urls:
        extractAndLogData(each, index,writer)
        index += 1
    f.close()

if __name__ == "__main__":
    main()
