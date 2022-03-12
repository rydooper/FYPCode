import re

from bs4 import BeautifulSoup as Soup
from selenium.webdriver.common.by import By

counter = 0
allArticles = []
allMetaData = []


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


def getArticleContents(driver, soup, link):
    driver.get(link)
    articleContents: list = []

    # Printing the whole body text
    allTextContentsStr = driver.find_element(by=By.XPATH, value="/html/body/div/div/main/div/div/div").text
    allTextContents: list = allTextContentsStr.split('\n')
    for index, contents in enumerate(allTextContents):
        if contents == "More on this story":
            break
        else:
            articleContents.append(contents)
    # allText = soup.findAll("div", {"class": "ssrcss-uf6wea-RichTextComponentWrapper e1xue1li86"})
    # print(allText)
    # print(soup.get_text())

    return articleContents


def getData(driver, url, userQuery):
    global articleTitle, articleSummary, articleLink, articlePublished, articleType, articleLocation, imgSrc, imgAlt

    driver.implicitly_wait(1)
    driver.get(url)

    soup = Soup(driver.page_source, "lxml")
    mainContentID = soup.find(id="main-content")
    styledContainerClass = mainContentID.find("div", attrs={"class": "ssrcss-1v7bxtk-StyledContainer enjd40x0"})
    wrapClass = styledContainerClass.find("div", attrs={"class": "ssrcss-1ocoo3l-Wrap e42f8511"})
    wrapWithWidthClass = wrapClass.find("div", attrs={"class": "ssrcss-1un9fz5-WrapWithWidth e42f8510"})
    listOfArticlesUL = wrapWithWidthClass.find("ul", attrs={"class": "ssrcss-v19xcd-Stack e1y4nx260"})

    for index, article in enumerate(listOfArticlesUL):
        duplicateArticle = False
        # in list element on BBC News page
        eachLIClass = article.find("div", {"class": "ssrcss-11rb3jo-Promo ett16tt0"})
        articleSelectionLI = eachLIClass.find("div", {"class": "ssrcss-dirbxo-PromoSwitchLayoutAtBreakpoints e3z3r3u0"})
        for items in articleSelectionLI:
            # gets content (1) and image container (2) in this loop

            for element in items:
                # get each bit of data from 1 and 2
                # first two ifs are for content!

                if element == items.find("div", {"class": "ssrcss-1cbga70-Stack e1y4nx260"}):
                    # this contains link, title and summary of article
                    articleTitle = element.find("p", {"class": "ssrcss-6arcww-PromoHeadline e1f5wbog4"})
                    articleSummary = element.find("p", {"class": "ssrcss-1q0x1qg-Paragraph eq5iqo00"})
                    articleLink = element.find("a", {"class": "ssrcss-atl1po-PromoLink e1f5wbog0"})
                    articleLink = articleLink['href']

                elif element == items.find("div", {"class": "ssrcss-1tha3dg-Stack e1y4nx260"}):
                    # this contains metadata - time since publication, type of article and publisher
                    metaData = element.find("dl", {"class": "ssrcss-vzegzu-MetadataStrip e1ojgjhb2"})
                    articleList = metaData.findAll("span", {"class": "ssrcss-8g95ls-MetadataSnippet ecn1o5v2"})
                    try:
                        articlePublished = articleList[0].text
                        articleType = articleList[1].text
                        articleLocation = articleList[2].text
                    except IndexError:
                        if articlePublished is None:
                            articlePublished = "Unknown"
                        elif articleType is None:
                            articleType = "Unknown"
                        elif articleLocation is None:
                            articleLocation = "Unknown"

                elif element == items.find("div", {"class": "ssrcss-17h6w1t-PromoImageContainerInner ehnfhlg2"}):
                    # this contains the image data
                    imgClass = element.find("img", {"class": "ssrcss-1drmwog-Image ee0ct7c0"})
                    imgSrc = imgClass['src']
                    imgAlt = imgClass['alt']
                else:
                    print("unknown error at element: ", element)

        if articleType == "News":
            articleConList = getArticleContents(driver, soup, articleLink)
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

    print(url)

    listFind = driver.find_element_by_xpath("/html/body/div[1]/div/main/div[1]/div[4]/div/div/nav/div/div/div[3]/div/ol")
    # wrapSelect = sectionSelect.find("div", {"class": "ssrcss-1ocoo3l-Wrap e42f8511"})
    # listSelect = driver.find_element(by=By.XPATH, value=wrapSelect + "/div/div/nav/div/div")
    finalPageNum = 0
    nextURL = "https://www.bbc.co.uk/search?q=" + userQuery + "&page=" + finalPageNum
    '''next_pages_div = soup.find("div", {"class": "pagination__nav"})
    pages = next_pages_div.findAll("a", {"class": "pagination__nav-item"})

    for pageCounter in pages:
        if pageCounter.text == '...':
            continue

        global counter
        counter += 1

        page_text = int(pageCounter.text)
        if page_text > counter:
            print("Counter", pageCounter.text)
            nextURL = "https://www.bbc.co.uk/search?q=" + userQuery + "&page=" + pageCounter.text
            getData(driver, nextURL, userQuery)'''
