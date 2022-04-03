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

# cite here for documentation: Bird, Steven, Edward Loper and Ewan Klein (2009),
# Natural Language Processing with Python. O’Reilly Media Inc
# <- NLTK

allHTE = []


class HTETopics:
    def __init__(self, topics):
        self.topics = topics


def runExtraction():
    print("Input the full name of the csv file you wish to commit hot topic extraction on: ")
    fileName = input("> ")
    data = pd.read_csv(fileName)

    ignore = set(stopwords.words('english'))
    stemmer = WordNetLemmatizer()
    text = []
    for sentence in data.contents:
        words = word_tokenize(sentence)
        stemmed = []
        for word in words:
            if word not in ignore:
                stemmed.append(stemmer.lemmatize(word))
        text.append(' '.join(stemmed))

    vec = CountVectorizer(analyzer='word', ngram_range=(1, 1))
    X = vec.fit_transform(text)

    model = lda.LDA(n_topics=5, random_state=1)
    model.fit(X)

    topic_word = model.topic_word_

    vocab = vec.get_feature_names_out()
    n_top_words = 5

    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
        newHTE = HTETopics(topic_words)
        allHTE.append(newHTE)

    if fileName == 'articlesData.csv':
        csvName = 'HTETopics.csv'
    else:
        userQ1 = fileName.split('articlesData')[1]
        userQuery = userQ1.split('.csv')[0]
        csvName = 'HTETopics' + userQuery + '.csv'
    with open(csvName, 'w', encoding="utf-8") as ad:
        reader = csv.writer(ad, delimiter=",")
        reader.writerow('topic')
        for topic in allHTE:
            reader.writerow([topic.topics])


if __name__ == '__main__':
    runExtraction()
