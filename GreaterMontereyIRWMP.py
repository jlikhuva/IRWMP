'''
Data collection for the
Greater Monterey County IRWMP.
'''
import requests
from bs4 import BeautifulSoup as bs4
from bswrapper import fetchHTML, generateBeautifulSoupObject
import os
import io
import re


def main():
    gm = greaterMonterey()
    gm.downloadMinutes()


'''
For printing colored text.
'''


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


'''
Error Handling class.
'''


class errorHandler:
    def EXIT_DOWNLOAD_ERROR(self, html):
        print bcolors.FAIL + "Fatal error: Could not fetch data at '" + html + "'"
        os._exit(1)

    def DOWNLOAD_ERROR(self, link):
        print bcolors.WARNING + "Could not download file at '" + link + "'"

    def EXIT_BS4_ERROR(self):
        print bcolors.FAIL + "Fatal error: Could not generate an BeautifulSoup object"
        os._exit(1)

    def EXIT_HTML_PARSE_ERROR():
        pass


class greaterMonterey():
    kCompletedProjectsURL = "http://www.greatermontereyirwmp.org/projects/completed/"
    kOngoingProjectsURL = "http://www.greatermontereyirwmp.org/projects/implementation/"
    kProposedProjectsURL = "http://www.greatermontereyirwmp.org/projects/proposed/"
    kMinutesURL = "http://www.greatermontereyirwmp.org/documents/minutes/"
    kMinutesDirName = "./Monterey-Minutes"
    errorHandler = errorHandler()

    def downloadMinutes(self):
        minutesUrlList = self.getMinutesUrls()
        for url in minutesUrlList:
            self.downloadAndSave(url)
            # print url
        print "Done downloading and saving Pdfs."

    '''
    Returns the list of links to the pdf files.
    '''

    def getMinutesUrls(self):
        list_of_links = []
        html = fetchHTML(self.kMinutesURL)
        if html is None:
            errorHandler.EXIT_DOWNLOAD_ERROR(html)
        bsobject = generateBeautifulSoupObject(html)
        if bsobject is None:
            errorHandler.EXIT_BS4_ERROR()

        list_div_name = "entry-content"
        href = "href"
        html_link = "a"
        urls = bsobject.find('div', {'class': list_div_name})
        link_wrappers = urls.findAll(html_link)
        for each in link_wrappers:
            link = each.get(href)
            list_of_links.append(link)
        return list_of_links

    def downloadAndSave(self, url):
        if self.isFirstFile():
            self.createMinutesDir()
        dest_file_name = self.extractName(url)
        raw_file_data = ""
        try:
            raw_file_data = requests.get(url)
        except:
            url = "http://www.greatermontereyirwmp.org/" + url
            raw_file_data = requests.get(url)

        path_to_file = os.path.join(self.kMinutesDirName, dest_file_name)
        with io.open(path_to_file, "wb") as dest_file:
            try:
                dest_file.write(raw_file_data.content)
            except IOError:
                print "could not write data to '" + dest_file_name + "'"
                return
                # print "Saved file at '" + url + "' at '" + path_to_file + "'"

    def isFirstFile(self):
        return not os.path.exists(self.kMinutesDirName)

    def createMinutesDir(self):
        os.makedirs(self.kMinutesDirName)

    def extractName(self, url):
        full_name = url[url.rfind("/") + 1:]
        return re.sub("RWMG-Meeting-Minutes-", "", full_name)

    def scrapeCompleted(self):
        pass

    def scrapeOngoing(self):
        pass

    def scrapeProposed(self):
        pass


if __name__ == "__main__":
    main()
