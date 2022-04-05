import csv
import datetime
import re
from country_list import countries_for_language
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.common.by import By
import seleniumWebScraperOptions as ws

counter = 0
allArticles = []
allMetaData = []
possibleTypes = ["Programmes", "News"]
possibleBBCSite = ["BBC News", "BBC Radio", "BBC Radio One", "BBC Radio 4", "BBC World Service", "BBC News Channel",
                   "BBC Parliament"]
countries = dict(countries_for_language('en'))


class articleData:
    def __init__(self, title, summary, contents):
        self.title = title
        self.summary = summary
        self.contents = contents


class articleMetadata:
    def __init__(self, link, AType, publisher, publishDate, imageSrc, imageAlt):
        self.link = link
        self.type = AType
        self.publisher = publisher
        self.publishDate = publishDate
        self.imageSrc = imageSrc
        self.imageAlt = imageAlt


def getArticleContents(driver, link):
    driver.get(link)
    articleContents: list = []

    # Printing the whole body text
    # "/html/body/div[1]/div/main/div[5]/div/div[1]/article/div[2]/div"
    try:
        allTextContentsStr = driver.find_element(by=By.XPATH, value="/html/body/div[1]/div/main/"
                                                                    "div[5]/div/div[1]/article").text
        allTextContents: list = allTextContentsStr.split('\n')
        for index, contents in enumerate(allTextContents):
            if contents == "More on this story":
                break
            else:
                articleContents.append(contents)
    except Exception as e:
        errorCaught = 0
        # just something so that news articles that have videos in them (which break the content collector) are ignored

    return articleContents


def runNextPageLoop(driver, userQuery, extraDiv):
    nextWrap = extraDiv.findAll("div", attrs={"class": "ssrcss-1ocoo3l-Wrap e42f8511"})
    nextWrapWithWidth = nextWrap[-1].find("div", attrs={"class": "ssrcss-1un9fz5-WrapWithWidth e42f8510"})
    nextStyledContainer = nextWrapWithWidth.find("div", attrs={"class": "ssrcss-knt0go-StyledContainer e1mcsnoz0"})
    paginationDiv = nextStyledContainer.find("nav", attrs={"class": "ssrcss-1kgye0g-Pagination e1w4tz4u0"})
    clusterDiv = paginationDiv.find("div", attrs={"class": "ssrcss-i7uuy0-Cluster e1ihwmse1"})
    clusterItemsDiv = clusterDiv.find("div", attrs={"class": "ssrcss-1xizsqg-ClusterItems e1ihwmse0"})
    numberedPagesDiv = clusterItemsDiv.find("div", {"class": "ssrcss-1izxn3x-NumberedPagesButtonsContainer e4i2y2x4"})
    clusterItemsList = numberedPagesDiv.find("ol", {"class": "ssrcss-1g16blr-ClusterItems e1ihwmse0"})

    allItemsInList = clusterItemsList.findAll("div", {"class": "ssrcss-3vkeha-StyledButtonContent e1b2sq421"})
    lastItemLi = allItemsInList[-1]
    lastItemNum = int(lastItemLi.text)

    for integer in range(lastItemNum):
        integer += 1
        if integer == 0:
            continue
        indexStr = str(integer)
        nextUrl = "https://www.bbc.co.uk/search?q=" + userQuery + "&page=" + indexStr
        print("Moving to page: ", indexStr)
        getData(driver, nextUrl, userQuery, nextPageCollected=True)


def getData(driver, url, userQuery, nextPageCollected):
    global articleType, articleLink, articlePublished, articleLocation, articleTitle, articleSummary, imgSrc, imgAlt
    articlePublished = None
    articleLocation = None
    articleType = None

    driver.implicitly_wait(1)
    driver.get(url)
    try:
        soup = Soup(driver.page_source, "lxml")
        mainContentID = soup.find(id="main-content")
        extraDiv = mainContentID.find("div")
        styledContainerClass = extraDiv.find("div", attrs={"class": "ssrcss-1v7bxtk-StyledContainer enjd40x0"})
        wrapClass = styledContainerClass.find("div", attrs={"class": "ssrcss-1ocoo3l-Wrap e42f8511"})
        wrapWithWidthClass = wrapClass.find("div", attrs={"class": "ssrcss-1un9fz5-WrapWithWidth e42f8510"})
        listOfArticlesUL = wrapWithWidthClass.find("ul", attrs={"class": "ssrcss-1020bd1-Stack e1y4nx260"})

        for index, article in enumerate(listOfArticlesUL):
            duplicateArticle = False
            # in list element on BBC News page
            eachLIClass = article.find("div", {"class": "ssrcss-11rb3jo-Promo ett16tt0"})
            articleSelectionLI = eachLIClass.find("div",
                                                  {"class": "ssrcss-dirbxo-PromoSwitchLayoutAtBreakpoints e3z3r3u0"})
            for items in articleSelectionLI:
                # gets content (1) and image container (2) in this loop

                for element in items:
                    # get each bit of data from 1 and 2
                    # first two ifs are for content!

                    if element == items.find("div", {"class": "ssrcss-1f3bvyz-Stack e1y4nx260"}):
                        # this contains link, title and summary of article

                        articleTitle = element.find("p", {"class": "ssrcss-6arcww-PromoHeadline e1f5wbog4"})
                        articleSummary = element.find("p", {"class": "ssrcss-1q0x1qg-Paragraph eq5iqo00"})
                        articleLink = element.find("a", {"class": "ssrcss-atl1po-PromoLink e1f5wbog0"})
                        articleLink = articleLink['href']

                    elif element == items.find("div", {"class": "ssrcss-wdw1q-Stack e1y4nx260"}):
                        # this contains metadata - time since publication, type of article and publisher
                        metaData = element.find("dl", {"class": "ssrcss-vzegzu-MetadataStrip e1ojgjhb2"})
                        articleList = metaData.findAll("span", {"class": "ssrcss-8g95ls-MetadataSnippet ecn1o5v2"})
                        for i in articleList:
                            testText = str(i.text)
                            if testText in possibleTypes:
                                articleType = testText
                            elif testText in possibleBBCSite or testText in countries.values():
                                articleLocation = testText
                            else:
                                articlePublished = testText

                        if articleType is None:
                            articleType = "Unknown"
                        if articleLocation is None:
                            articleLocation = "Unknown"
                        if articlePublished is None:
                            if articleType == "Programmes":
                                articlePublished = "Check BBC for Programme release"
                                # Programmes don't have a specified date on BBC Website,
                                # usually because they have multiple episodes
                            else:
                                articlePublished = "Unknown"

                    elif element == items.find("div", {"class": "ssrcss-17h6w1t-PromoImageContainerInner ehnfhlg2"}):
                        # this contains the image data
                        imgClass = element.find("img", {"class": "ssrcss-1drmwog-Image ee0ct7c0"})
                        imgSrc = imgClass['src']
                        imgAlt = imgClass['alt']
                    else:
                        print("Unknown error at element: ", element)

            if articleType == "News":
                articleConList = getArticleContents(driver, articleLink)
                articleConStr = str(articleConList)
                articleCon1 = re.sub("[\\[[]", "", articleConStr)
                articleCon2 = re.sub("'", "", articleCon1)
                articleCon3 = re.sub(",", "", articleCon2)
                articleCon4 = re.sub('"', "", articleCon3)
                articleContents: str = re.sub("[[]", "", articleCon4)
            else:
                articleContents = "Unknown"

            # article contents retrieved, now appending to list
            newArticle = articleData(articleTitle.text, articleSummary.text, articleContents)
            newMetadata = articleMetadata(articleLink, articleType, articleLocation, articlePublished, imgSrc, imgAlt)
            for val in allArticles:
                if val.title == newArticle.title:
                    duplicateArticle = True
                    break
            if duplicateArticle:
                continue
            else:
                allArticles.append(newArticle)
                allMetaData.append(newMetadata)

        if not nextPageCollected:
            nextPageCollected = True
            runNextPageLoop(driver, userQuery, extraDiv)
    except Exception as error:
        print("Some errors while webscraping!")
        print(error)


def webScrape(userQuery):
    url = "https://www.bbc.co.uk/search?q=" + userQuery
    driver = ws.chromeDriverSetup()
    # WebDriver Chrome
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # #<- test this later to see if user doesnt have to manually download chromedriver

    getData(driver, url, userQuery, nextPageCollected=False)
    driver.close()  # close the driver!
    csvName = 'articlesData-' + userQuery + '.csv'  #
    metaCSVName = 'articlesMetadata-' + userQuery + '.csv'  #
    with open(csvName, 'w', encoding="utf-8") as ad:
        reader = csv.writer(ad, delimiter=",")
        reader.writerow(["title", "summary", "contents"])
        # writes all the articles found to articlesData.csv
        for article in allArticles:
            reader.writerow([article.title, article.summary, article.contents])
        userQString = "with userQuery: " + userQuery
        finalRow = ["lastUpdated: ", datetime.datetime.now(), userQString]
        reader.writerow(finalRow)

    with open(metaCSVName, 'w', encoding="utf-8") as amd:
        reader = csv.writer(amd, delimiter=",")
        reader.writerow(["link", "type", "publisher", "published", "imageSource", "imageAlt"])
        for meta in allMetaData:
            reader.writerow([meta.link, meta.type, meta.publisher, meta.publishDate, meta.imageSrc, meta.imageAlt])
        userQString = "with userQuery: " + userQuery
        reader.writerow(["lastUpdated: ", datetime.datetime.now(), userQString])

    print("Articles scraped and appended to ", csvName, ", metaData stored in ", metaCSVName)


if __name__ == '__main__':
    print("Input topic to extract articles on: ")
    userQuery = input("> ")
    webScrape(userQuery)
