# -*- coding: utf-8 -*-
# ryder franklin
# FYP - AI news extraction
import random

import seleniumDataExtraction as dataScraper
import hotTopicExtraction as hte
import wordCloudGeneration as wc

allTopics = ['EU', 'france', 'ukraine']

if __name__ == "__main__":
    # create the driver object.
    takingQueries = True
    while takingQueries:
        print("Do you wish to: "
              "[1] Run a preset analysis on available data "
              "[2] Manually analyse data ")
        userManual = input("> ")
        if userManual == "1":
            randChoice = random.choice(allTopics)
            randCSV = 'CSV-Articles/articlesData-' + randChoice + '.csv'
            hte.runExtraction(randCSV)
            maskName = 'images/mask-map-' + randChoice + '.jpg'
            wc.wordCloudWithMask(randCSV, maskName)
        elif userManual == "2":
            print("Do you wish to: "
                  "[1] Scrape for articles on a specified topic "
                  "[2] Generate a wordcloud on available data "
                  "[3] Run hot topic extraction on available data "
                  "[4] Close Program ")
            userChoice = input("> ")
            if userChoice == "1":
                print("Please ensure you have a valid version of chrome "
                      "and its corresponding chromedriver installed before scraping.")
                print("Input topic to extract articles on: ")
                userQuery = input("> ")
                dataScraper.webScrape(userQuery)
            elif userChoice == "2":
                # EDA with word cloud
                print("Input the filepath of the csv file you wish to generate a word cloud on: ")
                fileName = input("> ")
                print("Does this file/topic have a corresponding mask? [1] Yes [2] No")
                maskYes = input("> ")
                if maskYes == "2":
                    wc.wordCloud(fileName)
                elif maskYes == "1":
                    print("Input the filepath of the jpg or png file you wish to use for mask: ")
                    maskName = input("> ")
                    wc.wordCloudWithMask(fileName, maskName)
            elif userChoice == "3":
                print("Input the filepath of the csv file you wish to commit hot topic extraction on: ")
                fileName = input("> ")
                hte.runExtraction(fileName)
            elif userChoice == "4":
                print("Exiting program now.")
                takingQueries = False
            else:
                print("Unclear input, retry.")
