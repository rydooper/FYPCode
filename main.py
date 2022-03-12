# -*- coding: utf-8 -*-
# ryder franklin
# FYP - AI news extraction
import seleniumDataExtraction as dataScraper
import seleniumWebScraperOptions as ws
import os
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import datetime
import nltk
import csv


# cite here for documentation: Bird, Steven, Edward Loper and Ewan Klein (2009),
# Natural Language Processing with Python. O’Reilly Media Inc
# <- NLTK

def webScrape():
    print("Input topic to extract articles on: ")
    userQuery = input("> ")
    url = "https://www.bbc.co.uk/search?q=" + userQuery
    driver = ws.chromeDriverSetup()
    # WebDriver Chrome
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # #<- test this later to see if user doesnt have to manually download chromedriver

    dataScraper.getData(driver, url, userQuery)
    driver.close()  # close the driver!
    csvName = 'articlesData-' + userQuery + '.csv'
    metaCSVName = 'articlesMetadata-' + userQuery + '.csv'
    with open(csvName, 'w', encoding="utf-8") as ad:
        reader = csv.writer(ad, delimiter=",")
        # writes all the articles found to articlesData.csv
        for article in dataScraper.allArticles:
            reader.writerow([article.title, article.summary, article.contents])
        reader.writerow(["lastUpdated: ", datetime.datetime.now(), "with userQuery: ", userQuery])

    with open(metaCSVName, 'w', encoding="utf-8") as amd:
        reader = csv.writer(amd, delimiter=",")
        for meta in dataScraper.allMetaData:
            reader.writerow([meta.link, meta.type, meta.publisher, meta.publishDate, meta.imageSrc, meta.imageAlt])
        reader.writerow(["lastUpdated: ", datetime.datetime.now(), "with userQuery: ", userQuery])

    print("Articles scraped and appended to ", csvName, ", metaData stored in ", metaCSVName)


def wordCloud():
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # Read the whole text.
    text = open(path.join(d, 'articlesData-ukraine.csv'), encoding="utf-8").read()

    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    # the matplotlib way:

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    # create the driver object.
    takingQueries = True
    while takingQueries:
        print("Do you wish to: "
              "[1] Scrape for articles on a specified topic "
              "[2] Generate a wordcloud on available data "
              "[3] Close Program ")
        userChoice = input("> ")
        if userChoice == "1":
            print("Please ensure you have a valid version of chrome "
                  "and its corresponding chromedriver installed before scraping.")
            webScrape()
        elif userChoice == "2":
            print("Generating word cloud on previous data stored in articlesData.csv")
            # EDA with word cloud
            wordCloud()
        elif userChoice == "3":
            print("Exiting program now.")
            takingQueries = False
        else:
            print("Unclear input, retry.")
