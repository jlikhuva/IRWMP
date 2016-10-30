# Script to write to the csv database file
# and record data in the various section
# folders.

import sys
import io
import unicodecsv as csv

kDefautlOpeningFmt = 'wb'
kDefautlReadingFmt = 'rb'
kDefaultEncoding = 'utf-8'
kDB = "database.csv"
kHeadingNames = [
    'Index',
    'Title',
    'Abstract',
    'Locations',  # Counties and subregions
    'Location (lat/long)',
    'Start Date',
    'End Date',
    'Location Description',
    'Project Type Description',
    'Detailed Description',
    'Project Need',
    'Critical Impacts',
    'Benefits',
    # 'Cost',
    # 'Funding Source',
    'Sponsor Agency',
    'Drinking Water Supply',
    'Water Quality Improvement',
    'Water Reuse/Recycling',
    'Stormwater Improvements',
    'Groundwater Benefits',
    'Infiltration',
    'Habitat Protection and Restoration',
    'Flood Protection'
]

csv.register_dialect(
    'dialect',
    delimiter=',',
    quotechar='"',
    doublequote=False,
    skipinitialspace=True,
    lineterminator='\r\n',
    escapechar='\\',
    quoting=csv.QUOTE_ALL
)

'''
Routines to standardize reading from
and writing to this db
These functions return a list
with ls[0] as the reader/writer and
ls[1] as the open file handle that
one can close by calling closeDB(ls[1])
'''
def createReader(dbname):
    dbname = io.open(dbname, kDefautlReadingFmt)
    reader = csv.reader(dbname, dialect="dialect", encoding=kDefaultEncoding)
    ls = [reader, dbname]
    return ls

def createWriter(dbname):
    dbname = io.open(dbname, kDefautlOpeningFmt)
    writer = csv.writer(dbname, dialect="dialect", encoding=kDefaultEncoding)
    ls = [writer, dbname]
    return ls

def closeDB(dbname):
    dbname.close()

'''
Writes a single row into the CSV database.
csvFile   -- The "database"
dataArray -- A single row of data.
Message   -- A string to be printed to the console.
'''
def writeLine(csvFile, dataArray, message):
    print message
    csvWriter = createWriter(kDB)
    csvWriter[0].writerow(dataArray)
    csvWriter[1].close()