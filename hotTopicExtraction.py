# code adapted from https://stackoverflow.com/questions/61560056/
# extracting-key-phrases-from-text-based-on-the-topic-with-python
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import lda
from sklearn.feature_extraction.text import CountVectorizer


def runExtraction():
    data = pd.read_csv('articlesData-ukraine.csv')

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


if __name__ == '__main__':
    runExtraction()
