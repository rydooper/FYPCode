import time
from bs4 import BeautifulSoup as Soup
import csv

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import seleniumWebScraper as ws
from selenium import webdriver

# driver = webdriver.Firefox("C:\\Selenium\\geckodriver.exe")
driver = webdriver.Chrome("C:\\Selenium\\chromedriver.exe")
url = "https://www.bbc.co.uk/search?q="

counter = 0
websiteData = []


class pageData:
    def __init__(self, title, link, topic):
        self.title = title
        self.link = link
        self.topic = topic


'''id root
class ssrcss-101c4hk-SectionWrapper eustbbg3
id main-content
class ssrcss-1v7bxtk-StyledContainer enjd40x0
class ssrcss-1ocoo3l-Wrap e42f8511
class ssrcss-1un9fz5-WrapWithWidth e42f8510
class ssrcss-v19xcd-Stack e1y4nx260
LIST
for items in LIST^^
    find p and return text'''


def getData(driver, url, userQuery):
    driver.implicitly_wait(1)
    driver.get(url)

    soup = Soup(driver.page_source, "lxml")
    nextLayer = soup.find(id="main-content")
    anotherLayer = nextLayer.find("div", attrs={"class": "ssrcss-1v7bxtk-StyledContainer enjd40x0"})
    thirdLayer = anotherLayer.find("div", attrs={"class": "ssrcss-1ocoo3l-Wrap e42f8511"})
    fourthLayer = thirdLayer.find("div", attrs={"class": "ssrcss-1un9fz5-WrapWithWidth e42f8510"})
    finalLayer = fourthLayer.find("ul", attrs={"class": "ssrcss-v19xcd-Stack e1y4nx260"})
    print(finalLayer)
    try:
        select = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//ul[@class='ssrcss-v19xcd-Stack e1y4nx260']/li"))
        )
        print("found list")
    except TimeoutException:
        print("error :(")

    #select = Select(driver.find_element(By.CLASS_NAME, ''))

    '''for webpage in divs:
        for course in webpage.findAll("div",
                                      {"class": "ssrcss-1n8l1hq-MainSection eustbbg1"}):
            item_selection = course.findAll("div", {"class": "product-item"})
            for item in item_selection:
                print(item)
                print("\n")
                title = item.find("a", {"class": "product-item__title text--strong link"})
                title = title.toLower()
                extra = title['href'].split("?")[0]
                link = url.split("search")[0] + extra.split("all/")[1]
                topic = item.find("span", {"class": ""}).text

                newPageData = pageData(title.text, link, topic)
                websiteData.append(newPageData)'''

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


if __name__ == "__main__":
    # create the driver object.
    print("input topic to extract articles on: ")
    userQuery = input("> ")
    # time.sleep(500)
    driver = ws.configChromeDriver()
    getData(driver, url, userQuery)
    # close the driver.
    driver.close()

    with open('websiteData.csv', 'w', encoding="utf-8") as fd:
        reader = csv.writer(fd, delimiter=",")
        for web in websiteData:
            print(web.title.replace("-", ""), web.link, web.price[1:])
            reader.writerow([web.title, web.link, web.price])
