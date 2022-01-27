# -*- coding: utf-8 -*-
# ryder franklin
# FYP - AI news extraction

import nltk
import subprocess
import requests
import re
import datetime

# cite here for documentation: Bird, Steven, Edward Loper and Ewan Klein (2009),
# Natural Language Processing with Python. O’Reilly Media Inc
# <- NLTK
apiKey = "9065df6b11904d00baaf871bc07c52ce"

def getLanguage(lang):
    if lang == "japanese":
        language = "jp"
    else:
        language = "en"
    return language


def getDate(date):
    theDate = datetime.datetime.now()
    newYear = theDate.year
    newMonth = theDate.month
    newDay = theDate.day
    newDate = str(newYear) + str(newMonth) + str(newDay)
    if "month" in date:
        newMonth = newMonth - 1
        if newMonth == 0:
            newMonth = 12
            newYear = newYear - 1
        newDate = str(newYear) + str(newMonth) + str(newDay)

    print(newDate)
    return newDate


def main():
    takingQueries = True
    while takingQueries:
        print("input topic to extract articles on: ")
        queryTopic = input("> ")
        tokens = nltk.word_tokenize(queryTopic)
        tagged = nltk.pos_tag(tokens)
        print(tagged)

        print("input language for articles: ")
        langInput = input("> ")

        print("input how long ago you wish to get articles (up to a month supported): ")
        dateInput = input("> ")

        # give user input to newsAPI to collect topics
        if tagged[0][1] == 'NN':
            print(tagged[0][0], "is a noun!")
            query = tagged[0][0]

            lang = getLanguage(langInput)
            date = getDate(dateInput)

        # month in the past only
        # 2021-12-20
            url = "https://newsapi.org/v2/everything?q=" + query + "&from=" + date + "&sortBy=publishedAt&language="\
                  + lang + "&apiKey=" + apiKey

            allData = requests.get(url)
            allJSONData = allData.json()
            allArticles = allJSONData["articles"]
            print("Found ", allJSONData["totalResults"], " articles on the topic ", query)

            articlesToPrint = []

            for index, article in enumerate(allArticles):
                aJson = {"title": article["title"], "author": article["author"], 'website': article['source']['name'],
                        'description': article['description'], 'content': article['content']}

                articlesToPrint.append(aJson)

            print(articlesToPrint)
            # subprocess.run('scrapy runspider headlineScraper.py -o scrapedHeadlines.csv')
        elif queryTopic == "exit program":
            print("ending program")
            takingQueries = False
        else:
            print("user didn't input a noun and therefore the topic can't be found")


main()
