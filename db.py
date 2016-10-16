# Script to write to the csv database file
# and record data in the various section
# folders.

import sys
import io
import csv

kDefautlOpeningFmt = 'wb'
kDefaultEncoding = 'utf-8'
kHeadingNames = ['title', 'abstract', 'location', 'dates', 'locationDescr', 'projectTypeDescr', 'DetailedDescr',
                 'projectNeed', 'criticalImpacts', 'Benefits', 'cost', 'fundingSrc', 'sponsorAgency']

csv.register_dialect(
    'dialect',
    delimiter = ' ',
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
