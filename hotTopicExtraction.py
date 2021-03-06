# code adapted from https://stackoverflow.com/questions/61560056/
# extracting-key-phrases-from-text-based-on-the-topic-with-python
import csv
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import lda
from sklearn.feature_extraction.text import CountVectorizer


allHTE = []


class HTETopics:
    def __init__(self, topics):
        self.topics = topics


def runExtraction(fileName):
    data = pd.read_csv(fileName)
    print("Extracting topics...")

    ignoreStopWords = set(stopwords.words('english'))
    stemmer = WordNetLemmatizer()
    text = []
    for sentence in data.contents:
        words = word_tokenize(sentence)
        stemmed = []
        for word in words:
            if word not in ignoreStopWords:
                stemmed.append(stemmer.lemmatize(word))
        text.append(' '.join(stemmed))

    countVectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 1))
    termFrequency = countVectorizer.fit_transform(text)
    vocab = countVectorizer.get_feature_names_out()

    LDAModel = lda.LDA(n_topics=5, n_iter=1000, random_state=1)
    LDAModel.fit(termFrequency)

    topicWord = LDAModel.topic_word_
    nTopWords = 5

    for i, topicDistribution in enumerate(topicWord):
        topicWords = np.array(vocab)[np.argsort(topicDistribution)][:-(nTopWords + 1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topicWords)))
        newHTE = HTETopics(topicWords)
        allHTE.append(newHTE)

    if fileName == 'CSV-Articles/articlesData.csv':
        csvName = 'CSV-Articles/HTETopics.csv'
    else:
        userQ1 = fileName.split('articlesData')[1]
        userQuery = userQ1.split('.csv')[0]
        csvName = 'CSV-Articles/HTETopics' + userQuery + '.csv'
    with open(csvName, 'w', encoding="utf-8") as ad:
        reader = csv.writer(ad, delimiter=",")
        reader.writerow(["topic"])
        for topic in allHTE:
            reader.writerow([topic.topics])


if __name__ == '__main__':
    print("Input the filepath of the csv file you wish to commit hot topic extraction on: ")
    fileName = input("> ")
    runExtraction(fileName)
