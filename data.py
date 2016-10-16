# This package takes care of data
# collection.

import sys
import os
import io
import re
import bswrapper
from urllib2 import urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup
from db import writeLine, kDB, kHeadingNames

# Konstants
kMetaTableName = "vertical listing"
kTableData = "td"

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

# Removes links that, instead of pointing to
# individual project pages, point to images.
# or pdf files
def removeImageLinks(urlList):
    for eachLink in urlList:
        if re.search(".jpg", eachLink) or re.search(".pdf", eachLink) or re.search(".xlsx", eachLink):
            urlList.remove(eachLink)

# Takes in a single url and extract and
# stores all the "important" data about
# the given project.
def extractAndLogData(url):
    html = bswrapper.fetchHTML(url)
    bsobj = bswrapper.generateBeautifulSoupObject(html)
    if bsobj is None:
        print "Could not create BeautifulSoup Object. Abort"
        return
    
    title = bswrapper.extractHeading(bsobj)
    if title is not None:
        metadata = extractMetadata(bsobj)
        print metadata
    
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
    
def main():
    initDB(kDB, kHeadingNames)
    urls = getAllProjectURLS()
    removeImageLinks(urls)
    for each in urls:
        extractAndLogData(each)

if __name__ == "__main__":
    main()
