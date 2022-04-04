# -*- coding: utf-8 -*-
# ryder franklin
# FYP - AI news extraction
import seleniumDataExtraction as dataScraper
import hotTopicExtraction as hte
import os
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def wordCloud():
    print("Input the full name of the csv file you wish to generate a word cloud on: ")
    fileName = input("> ")  # each topic from HTE or all articles data can be grabbed using this
    # get data directory
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    text = open(path.join(d, fileName), encoding="utf-8").read()
    print("Generating word cloud...")
    # generate word cloud image
    wordcloud = WordCloud().generate(text)

    # display with matplotlib
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    # generate on each topic from HTE


if __name__ == "__main__":
    # create the driver object.
    takingQueries = True
    while takingQueries:
        print("Do you wish to: "
              "[1] Scrape for articles on a specified topic "
              "[2] Generate a wordcloud on available data "
              "[3] Run hot topic extraction on available data "
              "[4] Close Program ")
        userChoice = input("> ")
        if userChoice == "1":
            print("Please ensure you have a valid version of chrome "
                  "and its corresponding chromedriver installed before scraping.")
            dataScraper.webScrape()
        elif userChoice == "2":
            # EDA with word cloud
            wordCloud()
        elif userChoice == "3":
            hte.runExtraction()
        elif userChoice == "4":
            print("Exiting program now.")
            takingQueries = False
        else:
            print("Unclear input, retry.")
