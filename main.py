# ryder franklin
# FYP - AI news extraction
import nltk
import subprocess
import requests

# cite here for documentation: Bird, Steven, Edward Loper and Ewan Klein (2009),
# Natural Language Processing with Python. O’Reilly Media Inc
# <- NLTK
apiKey = "9065df6b11904d00baaf871bc07c52ce"


def main():
    print("input topic to extract articles on: ")
    userInput = input("> ")
    tokens = nltk.word_tokenize(userInput)
    tagged = nltk.pos_tag(tokens)
    print(tagged)

    print("input language for articles: ")
    userInput = input("> ")
    lang = userInput

    # give user input to newsAPI to collect topics
    if tagged[0][1] == 'NN':
        print(tagged[0][0], "is a noun!")
        query = tagged[0][0]

        if lang == "english":
            lang = "en"
        elif lang == "japanese":
            lang = "jp"

        url = "https://newsapi.org/v2/everything?q=" + query + "&from=2021-12-19&sortBy=publishedAt&language=" + lang + "&apiKey=" + apiKey
        allData = requests.get(url)
        allJSONData = allData.json()
        allArticles = allJSONData["articles"]
        print("Found ", allJSONData["totalResults"], " articles on the topic ", query)
        print(allArticles)
        # subprocess.run('scrapy runspider headlineScraper.py -o scrapedHeadlines.csv')


main()
