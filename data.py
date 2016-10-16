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
from db import writeLine

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
        if re.search(".jpg", eachLink) or re.search(".pdf", eachLink):
            print eachLink
            urlList.remove(eachLink)

def main():
    urls = getAllProjectURLS()
    removeImageLinks(urls)

if __name__ == "__main__":
    main()
