# Data classification.
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer as ss
import re, os, codecs, sklearn, mpld3, csv
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
   print "Hello there, nothing here yet."

if __name__ == "__main__":
    main()
