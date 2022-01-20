import scrapy
from pandas import read_csv
from readability.readability import Document
# code from guide - https://towardsdatascience.com/tutorial-scrape-100-headlines-in-seconds-with-23-lines-of-python
# -14047deb1a98 <- spyder bot


class HeadlineSpider(scrapy.Spider):
    name = "headline_spider"
    pathToData = "newssitesURLS.csv"

    # startUrls = read_csv(pathToData).url.tolist()
    startUrls = read_csv(pathToData).url.tolist()

    def parse(self, response):
        doc = Document(response.text)
        yield {
            'short_title': doc.short_title(),
            'full_title': doc.title(),
            'url': response.url
        }
