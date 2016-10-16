'''
Collects data from 121 archived projects carried
out by the BayArea Integrated Water Management plan.
The module also organizes the data into groups and
stores them.
'''
import sys
import os
import io
from urllib2 import urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup

# Constants used when collecting links.
kBaseUrl = "http://bairwmp.org/projects/archived-projects-2013-plan-update/folder_tabular_view?b_start:int=0&-C"
kSecondPageUrl = "http://bairwmp.org/projects/archived-projects-2013-plan-update/folder_tabular_view?b_start:int=100&-C="
kTableEntryClass = "contenttype-irwmpproject"
kTableClassName = "listing"
kTableHref = "href"
kHtmlLink = "a"

# Constants used when storing data
kProjectNames = "projectNames.txt"
kAbstractName = "abstract.txt"
kProjectTypeDescr = "projectTypeDescription.txt"
kFunctionalAreas = "functionalAreas.txt"
kSponsorAgencies = "sponsorAgencies.txt"
kParticipants = "participatingOrganizations.txt"


'''
Fetches the html text stored at url. url
is expected to be a valid location. If not
this procedure ruturns None. The caller must test
to ensure that the returned object is not None.
'''
def fetchHTML(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    return html

'''
provided html is valid html text, this procedure 
converts it to a beautiful soup object that is easy
to parse. None is returned if an excetion is raised. As
such, the caller needs to check that the returned object
is not None.
'''
def generateBeautifulSoupObject(html):
    try:
        bsObject = BeautifulSoup(html, 'html.parser') #from the bs4 3rd part library
    except AttributeError as e:
        return None
    return bsObject

'''
This routine takes the beautiful soup object generated above
and gathers from it links to the listed projects. The links are packaged
into a list that is returned to the caller.
'''

#This is how a single url element looks like in html.
'''
<tr class="even"> |class= "odd" if odd|
  <td>
    <span
      class="contenttype-irwmpproject">
        <img width="16"
          height="16" src="http://bairwmp.org/proj.gif" alt="Project" />
            <a href="http://bairwmp.org/projects/archived-projects-2013-plan-update/mount-diablo-state-park-comprehensive-stock-pond"
            class="state-published" title="">Mount Diablo State Park:  Comprehensive Stock Pond Evaluation and Sedimentation Remediation</a>
    </span>
  </td>
  <td>Project</td>
</tr>
'''
def getProjectUrls(bsObject):
    listOfLinks = []
    table = bsObject.find('table', {'class': kTableClassName})
    linkWrappers = table.findAll(kHtmlLink)
    for eachWrapper in linkWrappers:
        listOfLinks.append(eachWrapper.get(kTableHref))
    return listOfLinks

'''
This routine takes in a list of 
valid URLs. It then proceeds to 
collect the needed data from the pages
pointed to by the locators.
'''
def scrapeEachProjectPage(urlList):
    for eachUrl in urlList:
        html = fetchHTML(eachUrl)
        bSoupObject = generateBeautifulSoupObject(html)
        extractAndStoreDataFromProjectPage(bSoupObject)
        

'''
This dictionary provides a way to compactly locate
the position of the data we want to extract from the
list of data objects returned by findAll.
'''
dataPositions = {
    "kAbstractPos" : 0,
    "kProjectDescr" : 9,
    "kFuncAreasPos" : 10,
    "kElemOfLarger": 12,
    "kReduceWaterSupply": 19,
    "kAdjToDisadvComm" : 20,
    "kDisadvCommPartic" : 21,
    "kSponsorAgency" : 41,
    "kParticipatingOrgs" : 42
}

'''
Helper routine that does the actual scraping.
'''
def extractAndStoreDataFromProjectPage(bsObject):
    #    |PART 1|
    title = extractHeading(bsObject)
    allText = extractAllText(bsObject)

    '''
    Since we have all the data that we want, we can go ahead and extract
    the pieces that we're interested in. To know exactly where our pieces
    of interest lie, we manually examine using the commented out code below.
    This works only b/c the data we're dealing with is small enough. With a 
    larger data set, it'd be better to examine the data to find patterns that 
    can aid us in extracting data. But, at the moment, and with our current trove,
    this strategy works.
    '''
    '''
    f = open(title+".txt", "w")
    i = 0
    for each in allText:
        if each:
            try:
                f.write(str(i))
                f.write(each)
            except:
                f.write("Error")
            i+=1
    f.close()
    '''
    abstract = allText[dataPositions["kAbstractPos"]]
    projectTypeDescr = allText[dataPositions["kProjectDescr"]]
    functionalAreas = allText[dataPositions["kFuncAreasPos"]]
    elemOfLarger = allText[dataPositions["kElemOfLarger"]]
    sponsorAgency = allText[dataPositions["kSponsorAgency"]]
    participatingOrgs = allText[dataPositions["kParticipatingOrgs"]]
    adjToDisadvComm = allText[dataPositions["kAdjToDisadvComm"]]
    disadvCommParticipation = allText[dataPositions["kDisadvCommPartic"]]
    reduceWaterSupply = allText[dataPositions["kReduceWaterSupply"]]

    addProjectNameToProjectList(title)
    createThisProjectsDirectory(title)
    storeThisProjectsAbstract(abstract, title)
    storeThisProjectsDescription(projectTypeDescr, title)
    storeThisProjectsFunctionalAreas(functionalAreas, title)
    storeThisProjectsSponsorAgencies(sponsorAgency, title)
    storeThisProjectsParticipatingOrgs(participatingOrgs, title)
    
    # The data set that we have has a LOT of 'noise', that is, a lot
    # of would be useful data that is missing. At a point in time when
    # we are dealing with documents in which that data is present, the routines
    # below are to be implemented to collect that data.
    '''
    #    |PART 2|
    detailedDescr = getDetailedDescr(bsObject)
    parentProject = getParentProject(bsObject)
    relatedDocs = getRelatedDocs(bsObject)
    applicableWaterBodies = getApplicableH20Bodies(bsObject)
    projectNeed = getProjectNeed(bsObject)
    impactsIfNotImpl = getImpactsIfNotImpl(bsObject);
    benefits = getProjectBenefits(bsObject)

    #   |PART 2.2|
    reduceWaterSupply = reduceWaterSupply(bsOject)
    disadvatagedCommunity = disadvantagedCommunity(bsObject)

    '''
    '''|Climate Change|'''
    '''adaptationToClimateChange = getAdaptationToClimateChange(bsObject)
    reducingGreenhouseGases = getMitigation(bsObject)
    impacts = getClimateChangeImpacts(bsObject)
    '''
    '''
    # |COSTS|
    costVector = getCostInfo(bsObject)
    stateWidePriorities = getStateWidePriorities(bsObject)
    califWPRMS = getCaliWPRMS(bsObject)
    eligibilityCriteria = getEligibilityCriteria(bsObject)
    prop84 = getMultipleBenefits(bsObject)
    prop1E = getStormWaterFloodManagement(bsObject)
    benefitsAndImpacts = getExpBenefitsAndImpacts(bsObject)

    # |PROJECT TEAM|
    contacts = getContacts(bsObject)
    investigators = getInvestigators(bsObject)
    sponsorAgency = getSponsorAgency(bsObject)
    participants = getParticipatingOrganizations(bsObject)

    # |Files|
    projectBenefitsFile = getProjectBenefitsFile(bsObject)
    '''
kProjectHeadingClass = "documentFirstHeading"
kProjectHeadingSizeDesc = "h1"
def extractHeading(bsobj):
    heading = bsobj.findAll(kProjectHeadingSizeDesc, {"class" : kProjectHeadingClass})
    try:
        return heading[0].get_text()
    except:
        print "Error parsing page, you might need to log in"
        return None
    
kFieldClass = "field"
def extractAllText(bsObject):
    textList = []
    fieldWrapper = bsObject.findAll("div", {"class" : kFieldClass})
    for paragraph in fieldWrapper:
        textList.append(paragraph.get_text())
    return textList

def addProjectNameToProjectList(title):
    try:
        f = open(kProjectNames, "a")
        f.write(title)
        f.write("\n")
    except:
        pass #ignoring errors for now
    f.close()

def generatePathFromCur(dirName):
    return "./"+dirName

def createThisProjectsDirectory(dirName):
    path = generatePathFromCur(dirName)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            sys.exit("Failed to create directory: " + dirName)
            
def storeThisProjectsAbstract(abstractText, where):
    path = generatePathFromCur(where)
    with io.open(os.path.join(path, kAbstractName), "w", encoding='utf-8') as abstractFile:
        try:
            abstractFile.write(abstractText)
        except:
            abstractFile.write("Encoding scheme error. Need to find way around this") # Ignore errors arising from encoding schemes
        abstractFile.close()
        
def storeThisProjectsDescription(descriptionText, where):
    path = generatePathFromCur(where)
    with io.open(os.path.join(path, kProjectTypeDescr), "w", encoding='utf-8') as descriptionFile:
        try:
            descriptionFile.write(descriptionText)
        except:
            pass
        descriptionFile.close()
        
def storeThisProjectsFunctionalAreas(funcAreasText, where):
    path = generatePathFromCur(where)
    with io.open(os.path.join(path, kFunctionalAreas), "w", encoding='utf-8') as funcAreasFile:
        try:
            funcAreasFile.write(funcAreasText)
        except:
            pass
        funcAreasFile.close()
        
def storeThisProjectsSponsorAgencies(sponsorAgenciesText, where):
    path = generatePathFromCur(where)
    with io.open(os.path.join(path, kSponsorAgencies), "w", encoding='utf-8') as sponsorAgenciesFile:
        try:
            sponsorAgenciesFile.write(sponsorAgenciesText)
        except:
            pass
        sponsorAgenciesFile.close()
        
def storeThisProjectsParticipatingOrgs(participantsText, where):
    path = generatePathFromCur(where)
    with io.open(os.path.join(path, kParticipants), "w", encoding='utf-8') as participantsFile:
        try:
            participantsFile.write(participantsText)
        except:
            pass
        participantsFile.close()
         
def main():
   firstPageHtml = fetchHTML(kBaseUrl)
   secondPageHtml = fetchHTML(kSecondPageUrl)
   firstPageBsObject = generateBeautifulSoupObject(firstPageHtml)
   secondPageBsObject = generateBeautifulSoupObject(secondPageHtml)
   urlList = getProjectUrls(firstPageBsObject) + getProjectUrls(secondPageBsObject)
   scrapeEachProjectPage(urlList)

if __name__ == "__main__":
    main()
