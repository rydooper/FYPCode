# -*- coding: utf-8 -*-
# ryder franklin
# FYP - AI news extraction

import datetime
import nltk
import seleniumDataExtraction as dataScraper
import csv
import seleniumWebScraperOptions as ws

# cite here for documentation: Bird, Steven, Edward Loper and Ewan Klein (2009),
# Natural Language Processing with Python. O’Reilly Media Inc
# <- NLTK

if __name__ == "__main__":
    # create the driver object.
    print("input topic to extract articles on: ")
    userQuery = input("> ")
    url = "https://www.bbc.co.uk/search?q=" + userQuery
    driver = ws.chromeDriverSetup()
    dataScraper.getData(driver, url)
    driver.close()  # close the driver!

    with open('articlesData.csv', 'w', encoding="utf-8") as fd:
        reader = csv.writer(fd, delimiter=",")
        # writes all the articles found to articlesData.csv
        for article in dataScraper.allArticles:
            reader.writerow([article.title, article.link, article.summary, article.type,
                             article.publishDate, article.publisher, article.imageSrc, article.imageAlt])
        reader.writerow(["lastUpdated: ", datetime.datetime.now()])

    print("Articles scraped and appended to articlesData.csv")