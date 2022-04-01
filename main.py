# -*- coding: utf-8 -*-
# ryder franklin
# FYP - AI news extraction
import seleniumDataExtraction as dataScraper
import os
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# cite here for documentation: Bird, Steven, Edward Loper and Ewan Klein (2009),
# Natural Language Processing with Python. O’Reilly Media Inc
# <- NLTK

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
            dataScraper.webScrape()
        elif userChoice == "2":
            print("Generating word cloud on previous data stored in articlesData.csv")
            # EDA with word cloud
            wordCloud()
        elif userChoice == "3":
            print("Exiting program now.")
            takingQueries = False
        else:
            print("Unclear input, retry.")
