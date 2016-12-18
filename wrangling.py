import db
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go

'''
Constants and variable used when
examining the funded projects database.
'''
kFundedProjectsName = 'FundedProjects.csv'
sponsorsDict = {}
projectLeadersDict = {}
countyDict = {}

proposedProjectsSponsorsDict = {}


def compileFundedSponsorsDict(reader):
    for row in reader:
        if row[1] in sponsorsDict:
            sponsorsDict[row[1]] += 1
        else:
            sponsorsDict[row[1]] = 1

        if row[2] in projectLeadersDict:
            projectLeadersDict[row[2]] += 1
        else:
            projectLeadersDict[row[2]] = 1

        if row[3]:
            if row[3] in countyDict:
                countyDict[row[3]] += 1
            else:
                countyDict[row[3]] = 1


def compileProposedProjectsDicts(reader):
    for row in reader:
        if row[12]:
            if row[12] in proposedProjectsSponsorsDict:
                proposedProjectsSponsorsDict[row[12]] += 1
            else:
                proposedProjectsSponsorsDict[row[12]] = 1


def plot():
    # iplotPlotPie(sponsorsDict, "Sponsors of funded Projects.")
    # iplotPlotPie(projectLeadersDict, "Funded Projects Project Leaders.")
    # iplotPlotPie(countyDict, "Counties of funded projects.")
    iplotPlotPie(proposedProjectsSponsorsDict, "Sponsors of proposed Projects.")


def iplotPlotPie(dict, title):
    fig = {
        'data': [
            {
                'labels': dict.keys(),
                'values': dict.values(),
                'type': 'pie'
            }
        ],
        'layout': {'title': title}
    }
    py.plot(fig)


# def iplotPlotBubble(dict, title):
# def iplotBar(dict, title):


def getRandomIntList(low, high, size):
    return np.random.randint(low, high, size)






def main():
    csvHandle1 = db.createReader(kFundedProjectsName)
    csvHandle2 = db.createReader(db.kDB)
    # compileFundedSponsorsDict(csvHandle1[0])
    compileProposedProjectsDicts(csvHandle2[0])
    # print getRandomIntList(0, 400, 400)
    plot()
    db.closeDB(csvHandle1[1])
    db.closeDB(csvHandle2[1])


if __name__ == "__main__":
    main()
