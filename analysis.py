# Data classification.
# Part of this work is base off
# of Brandon Rose's awesome
# Tuturial http://brandonrose.org/clustering

import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer as ss
import re, os, codecs, sklearn, mpld3, csv, hashlib
import db

'''
Global data objects that we
use throughout this module. They
are mostly data containers.
'''

'''
Returns a list of all the
data stored at the column
whose heading is specified
by the given index
'''


def getColumnData(pandasObject, colName):
    return pandasObject[0:4]


def main():
    headings = []
    projects = {}
    readerHandle = db.createReader(db.kDB)
    for row in readerHandle[0]:
        headings.append(row[0])
        # titleHash = hashlib.sha256(row[0])
        # print titleHash
        # th2 = hashlib.sha256(row[0])
        # print titleHash.equals(th2)
        projects[row[0]] = row[1:]
        break

    # print len(headings)
    print projects
    db.closeDB(readerHandle[1])


main()
