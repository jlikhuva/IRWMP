# Script to write to the csv database file
# and record data in the various section
# folders.

import sys
import io
import csv

kDefautlOpeningFmt = 'wb'
kDefaultEncoding = 'utf-8'
kDB = "database.csv"
kHeadingNames = [
    'Title',
    'Abstract',
    'Locations', # Counties and subregions
    'Location (lat/long)',
    'Start Date',
    'End Date',
    'Location Descr',
    'Project TypeDescr',
    'Detailed Descr',
    'Project Need',
    'Critical Impacts',
    'Benefits',
    'Cost',
    'Funding Src',
    'Sponsor Agency'
]

csv.register_dialect(
    'dialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = False,
    skipinitialspace = True,
    lineterminator = '\n',
    quoting = csv.QUOTE_MINIMAL
)
'''
Writes a single row into the CSV database.
csvFile   -- The "database"
dataArray -- A single row of data.
Message   -- A string to be printed to the console.
'''
def writeLine(csvFile, dataArray, message):
    print message
    f = io.open(csvFile, kDefautlOpeningFmt)
    csvWriter = csv.writer(f,dialect="dialect")
    csvWriter.writerow(dataArray)
    f.close()
    print "all [OK]"
