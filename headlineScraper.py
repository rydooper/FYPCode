import scrapy
from pandas import read_csv
from readability.readability import Document  # pip install readability-lxml for this


# code adapted from
# https://towardsdatascience.com/tutorial-scrape-100-headlines-in-seconds-with-23-lines-of-python-14047deb1a98
# <- spyder bot


class HeadlineSpider(scrapy.Spider):
    name = "headline_spider"
    pathToData = "newssitesURLS.csv"

    "https://search.bbc.co.uk/search?scope=all"
    startUrls = read_csv(pathToData).url.tolist()

    def parse(self, response):
        doc = Document(response.text)
        print(doc)
        yield {
            'short_title': doc.short_title(),
            'full_title': doc.title(),
            'url': response.url,
            'full_text': doc.summary(),
        }

'''
headers = {"Accept-Language": "en-UK, en;q=05"}
        url = "https://www.bbc.co.uk/news"

        results = requests.get(url, headers=headers)

        soup = BeautifulSoup(results.text, "html.parser")
        soup.prettify()  # makes content from results more readable

        topStoryHTML = "latest-stories-tab-container"
        topStoryDiv = soup.find_all('div', topStoryHTML)
        print(topStoryDiv)
        for container in topStoryDiv:
            storyTitle = container.h3.a.text
            print(storyTitle)'''