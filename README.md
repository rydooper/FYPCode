# Artificial Intelligence: Automatic News Extraction

This program was created for my disseration / final year project at NTU.

Currently, it can extract news articles from BBC News, extract hot topics from this data and create a word cloud for this data.

For the best results for topic extraction and word cloud generation, place your CSV articles data in the CSV-Articles folder.

Future development will include: a larger corpus (more news sources) and some machine learning algorithms (1 - to rank relevance of article; 2 - to filter fake news).

<br>

FAQ:
<br>

Q) How to setup news extraction?

A) Download a chrome browser and note the version (likely v98 or 99).
Download the chromedriver for this version, then place the driver file in a folder with this directory C:/Selenium

<br>

Q) Can this folder location be changed?

A) Yes! Edit the executable_path variable in seleniumWebScraperOptions file to set a different path. It is advised that you keep the driver file in a top directory for faster access.

<br>

Q) Why is the web-scrape so slow?

A) It depends entirely on your internet speed and computer processing ability.

<br>

Q) How to create a masked-word cloud?

A) Download an outline of an image, this can be anything.
Edit this image to have the inside as black and the outside as white - see images/mask-map-ukraine for an example setup.

<b> Don't see your question here? Drop me a message or comment. </b>
