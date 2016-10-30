import bswrapper, io, db

kLocalHTMLFile = "FundedProjects.htm"

def main():
    with io.open(kLocalHTMLFile, db.kDefautlReadingFmt) as htm:
        bsobject = bswrapper.generateBeautifulSoupObject(htm)

if __name__ == "__main__":
    main()