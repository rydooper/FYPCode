# code adapted from:
# https://github.com/FelixChop/MediumArticles/blob/master/LDA-BBC.ipynb

import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet

# load in data
data = pd.read_csv('articlesData-ukraine.csv')
data.shape()

# tokenise

data['sentences'] = data.articles.progress_map(sent_tokenize)
data['sentences'].head(1).tolist()

data['tokens_sentences'] = data['sentences'].progress_map(
    lambda sentences: [word_tokenize(sentence)] for sentence in sentences)
data['POS_tokens'] = data['tokens_sentences'].progress_map(
    lambda tokens_sentences: [pos_tag(tokens) for tokens in tokens_sentences])
print(data['POS_tokens'].head(1).tolist()[0][:3])

# Inspired from https://stackoverflow.com/a/15590384

### FINISH THIS

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


from nltk.stem.wordnet import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# Lemmatizing each word with its POS tag, in each sentence
data['tokens_sentences_lemmatized'] = data['POS_tokens'].progress_map(
    lambda list_tokens_POS: [
        [
            lemmatizer.lemmatize(el[0], get_wordnet_pos(el[1]))
            if get_wordnet_pos(el[1]) != '' else el[0] for el in tokens_POS
        ]
        for tokens_POS in list_tokens_POS
    ]
)

data['tokens_sentences_lemmatized'].head(1).tolist()[0][:3]

# Regrouping tokens and removing stop words

from nltk.corpus import stopwords

stopwords_verbs = ['say', 'get', 'go', 'know', 'may', 'need', 'like', 'make', 'see', 'want', 'come', 'take', 'use',
                   'would', 'can']
stopwords_other = ['one', 'mr', 'bbc', 'image', 'getty', 'de', 'en', 'caption', 'also', 'copyright', 'something']
my_stopwords = stopwords.words('English') + stopwords_verbs + stopwords_other

from itertools import chain  # to flatten list of sentences of tokens into list of tokens

data['tokens'] = data['tokens_sentences_lemmatized'].map(lambda sentences: list(chain.from_iterable(sentences)))
data['tokens'] = data['tokens'].map(lambda tokens: [token.lower() for token in tokens if token.isalpha()
                                                    and token.lower() not in my_stopwords and len(token) > 1])

data['tokens'].head(1).tolist()[0][:30]
