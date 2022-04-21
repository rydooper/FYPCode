import os
from os import path

from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np


def wordCloudWithMask(filename, maskname):
    # get data directory
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    # Read the whole text.
    text = open(path.join(d, filename), encoding="utf-8").read()
    print("Generating word cloud...")

    # read the mask image - taken from
    # https://www.worldatlas.com/maps <- all maps
    imageMask = np.array(Image.open(path.join(d, maskname)))

    stopwords = set(STOPWORDS)
    stopwords.add("said")
    wc = WordCloud(background_color="white", max_words=2000, mask=imageMask,
                   stopwords=stopwords, contour_width=3, contour_color='steelblue')

    # generate word cloud
    wc.generate(text)

    # save word cloud as png image
    imgName = str(filename.split('.csv')[0])
    if 'CSV-Articles' in imgName:
        imgName = str(imgName.split('CSV-Articles/')[1])
    imgName = 'images/wordCloud-' + imgName + '.png'
    wc.to_file(path.join(d, imgName))

    # show
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
    plt.show()


def wordCloud(filename):
    # each topic from HTE or all articles data can be grabbed using this
    # get data directory
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    text = open(path.join(d, filename), encoding="utf-8").read()
    print("Generating word cloud...")
    # generate word cloud image
    wordcloud = WordCloud().generate(text)
    # store to file
    imgName = str(filename.split('.csv'))
    if 'CSV-Articles' in imgName:
        imgName = str(imgName.split('CSV-Articles/')[1])
    imgName = 'images/wordCloud-' + imgName + '.png'
    wordcloud.to_file(path.join(d, imgName))

    # display with a low max font size
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    print("Input the filepath of the csv file you wish to generate a word cloud on: ")
    fileName = input("> ")
    print("Does this file/topic have a corresponding mask? [1] Yes [2] No")
    maskYes = input("> ")
    if maskYes == "2":
        wordCloud(fileName)
    elif maskYes == "1":
        print("Input the filepath of the jpg or png file you wish to use for mask: ")
        maskName = input("> ")
        wordCloudWithMask(fileName, maskName)
