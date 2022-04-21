# -*- coding: utf-8 -*-
# ryder franklin
# FYP - AI news extraction

import seleniumDataExtraction as dataScraper
import hotTopicExtraction as hte
import wordCloudGeneration as wc

if __name__ == "__main__":
    # create the driver object.
    takingQueries = True
    while takingQueries:
        print("Do you wish to: "
              "[1] Run a complete webscrape and analysis on a topic "
              "[2] Run a preset analysis on available data "
              "[3] Manually analyse data "
              "[4] Close program ")
        userManual = input("> ")
        if userManual == "1":
            print("Please ensure you have a valid version of chrome "
                  "and its corresponding chromedriver installed before scraping.")
            print("Input topic to extract articles on: ")
            userQuery = input("> ")
            dataScraper.webScrape(userQuery)
            csvName = 'CSV-Articles/articlesData-' + userQuery + '.csv'
            hte.runExtraction(csvName)
            wc.wordCloud(csvName)
        elif userManual == "2":
            print("Input the filepath to the CSV file you wish to extract topics from and create a word cloud: ")
            csvChoice = input("> ")
            hte.runExtraction(csvChoice)
            print("Use image mask? [1] Yes [2] No")
            imgMskChoice = input("> ")
            if imgMskChoice == "1":
                print("Input filepath to mask: ")
                maskName = input("> ")
                wc.wordCloudWithMask(csvChoice, maskName)
            else:
                wc.wordCloud(csvChoice)
        elif userManual == "3":
            print("Do you wish to: "
                  "[1] Scrape for articles on a specified topic "
                  "[2] Generate a wordcloud on available data "
                  "[3] Run hot topic extraction on available data ")
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
        elif userManual == "4":
            print("Exiting program now.")
            takingQueries = False
        else:
            print("Unclear input, retry.")
