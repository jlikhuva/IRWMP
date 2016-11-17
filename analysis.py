# Data classification.
# Part of this work is base off
# of Brandon Rose's awesome
# Tuturial http://brandonrose.org/clustering

import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer as ss
import nltk
import re, os, codecs, sklearn, mpld3, csv, hashlib
import db, data
from difflib import SequenceMatcher as sm
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from shapely.geometry import Point, mapping
from fiona import collection
import plotly.graph_objs as go
import plotly.plotly as py
import shapefile

'''
Global data objects that we
use throughout this module. They
are mostly data containers.
'''
kFundedProjects = "FundedProjects.csv"
latLongVector = []
essenceVector = []  #
locations = []
sponsorAgencies = []
stemmer = ss('english')

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
        if (curr_ratio > ratio):
            curClosest = each
            ratio = curr_ratio
    if ratio > 0.76:
        return curClosest


def xcx():
    projects = createDictionary(db.kDB)
    fundedProjects = createDictionary(kFundedProjects)

    allProjectKeys = projects.keys()
    ls = fundedProjects.keys()
    inboth = []

    for each in allProjectKeys:
        nearestMatch = getNearestMatchIn(each, ls)
        if nearestMatch is not None:
            # print nearestMatch + " : " + each
            inboth.append(nearestMatch)


def createProjectVectors():
    readerHandle = db.createReader(db.kDB)
    next(readerHandle[0])
    for row in readerHandle[0]:
        curVect = row[0] + row[1] + row[6] + row[7] + row[8] + row[12]
        essenceVector.append(curVect)
        latLongVector.append(row[3])
        locations.append(row[2])
        sponsorAgencies.append(row[12])
    db.closeDB(readerHandle[1])


def createProposedProjectsPlots():
    print "Not yet implemented"


'''
The next two functions are courtesy of
http://brandonrose.org/clustering#Stopwords,-stemming,-and-tokenizing
'''


def tokenizeAndStem(text):
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def justTokenize(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


def removeStopWords():
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords += ["water", "project", "county", "agency", "climate change",
                  "regional", "california", "bay area"]


def generateWordCloud():
    # print sponsorAgencies
    strlist = " ".join(sponsorAgencies)
    wcl = WordCloud().generate(strlist)
    plt.imshow(wcl)
    plt.axis("off")
    plt.show();


def map():
    lats = []
    longs = []
    schema = {'geometry': 'Point', 'properties': {'name': 'str'}}
    with collection("trial.shp", "w", "ESRI Shapefile", schema) as output:
        for each in latLongVector:
            ls = each.split("|");
            if len(ls) is not 2:
                continue
            lat = tofloat(ls[0])
            if lat is None:
                continue
            longi = tofloat(ls[1])
            if longi is None:
                continue
            point = Point(longi, lat)
            output.write({
                'properties': {
                    'name': "Example"
                },
                'geometry': mapping(point)
            })


def tofloat(strfloat):
    try:
        return float(strfloat)
    except:
        return None


def showShapefile():
    sf = shapefile.Reader("./trial.cpg")
    plt.figure()

    for shape in sf.shapes():
        x = [i[0] for i in shape.points[:]]
        y = [i[1] for i in shape.points[:]]
        plt.plot(x, y)
    plt.show()


def createSponsorAgencyCount():
    dict = {}
    for eachAgency in sponsorAgencies:
        if eachAgency in dict:
            dict[eachAgency] = dict[eachAgency] + 1
        else:
            dict[eachAgency] = 1
    return dict



def tt():
    trace = go.Scatter(
                        x=[1, 2, 3],
                       y=[1, 2, 3],
                       marker=dict(color=[ 'red', 'blue', 'green'],
                       size = [30, 80, 200]),
                       mode = 'markers'
                       )
    py.iplot([trace])


def main():
    # tt()
    createProjectVectors()
    # createProposedProjectsPlots()
    # map()
    # showShapefile()
    generateWordCloud()
    # stemsDict = {}
    # tokensDict = {}
    # stems = []
    # tokens = []

    # id = 1
    for text in essenceVector:
        d = tokenizeAndStem(text)
        t = justTokenize(text)
        stems.extend(d)
        tokens.extend(t)
        # id += 1
        # removeStopWords()
        # print essenceVector
    print stems
    print "\n\n"
    print tokens


if __name__ == "__main__":
    main()
