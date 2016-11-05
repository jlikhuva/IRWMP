# Data classification.
# Part of this work is base off
# of Brandon Rose's awesome
# Tuturial http://brandonrose.org/clustering

import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer as ss
import re, os, codecs, sklearn, mpld3, csv, hashlib
import db, data
from difflib import SequenceMatcher as sm

'''
Global data objects that we
use throughout this module. They
are mostly data containers.
'''
kFundedProjects = "FundedProjects.csv"

'''
Creates a dictionary by reading the csv file
identified by dbname.
'''
def createDictionary(dbname):
    dictToReturn = {}

    readerHandle = db.createReader(dbname)
    for row in readerHandle[0]:
        # print row
        dictToReturn[row[0]] = row[1:]

    db.closeDB(readerHandle[1])
    return dictToReturn


def getNearestMatchIn(word, list):
    curClosest = None
    ratio = 0.0
    for each in list:
        curr_ratio = sm(None, word, each).ratio()
        if(curr_ratio > ratio):
            curClosest = each
            ratio = curr_ratio
    if ratio > 0.76:
        return curClosest

def main():
    projects = createDictionary(db.kDB)
    fundedProjects = createDictionary(kFundedProjects)

    allProjectKeys = projects.keys()
    ls = fundedProjects.keys()
    inboth = []

    for each in allProjectKeys:
        nearestMatch = getNearestMatchIn(each, ls)
        if nearestMatch  is not None:
            print nearestMatch + " : " + each
            # inboth.append(nearestMatch)
    # print inboth

if __name__ == "__main__":
    main()
