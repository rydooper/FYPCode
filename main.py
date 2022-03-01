# ryder franklin
# FYP - AI news extraction
import nltk
import subprocess
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


# cite here for documentation: Bird, Steven, Edward Loper and Ewan Klein (2009),
# Natural Language Processing with Python. O’Reilly Media Inc
# <- NLTK


def main():
    print("input topic to extract articles on: ")
    userInput = input("> ")
    tokens = nltk.word_tokenize(userInput)
    tagged = nltk.pos_tag(tokens)

    # give user input to newsAPI to collect topics
    if tagged[0][1] == 'NN':
        print(tagged[0][0], "is a noun!")
        userQuery = tagged[0][0]


        # spider gets articles output as csv
        subprocess.run('scrapy runspider headlineScraper.py -o scrapedHeadlines.csv')

        # bs4 used to interpret HTML pages


main()
