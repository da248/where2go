# where2go

Having trouble figuring out where to go for summer vacation? Have some favorite destinations and want to find out similar places? Where2go was built to recommend you places to go based on places/characterstics you like or dislike, not based on which destination has cheap flight costs. This is a project built in two weeks as a capstone project for Galvanize Data Science Immersive (f.k.a. Zipfian Academy) program.

#### Try it out on www.where2go.help

## Motivation
There are a lot of websites that tell you the cheapest ways to get to a destination and the cheapest hotels to stay at. But they are forgetting to ask us a very fundamental question...do you know where2go? Articles like "XX's Top 25 Travel Destinations" or "YY's 100 Places You Must Visit!" tell you about interesting places around the world but I wanted to build a tool that will tell me where I should go based on my own experience and taste.

## Overview
One of the motivations for this applicaiton was building an unbiased recommendation system that will consider the destination's characterstics instead of looking at destinations that others liked. To do this, I decided to use travel guides to gather destination information. I found that Wikivoyage provided great travel guides that tell you about the history and culture of the place as well as what to see, how to get around, etc. *

The next question was then to figure out which model to use. The traditional recommendation systems for natural language processing include models like TF-IDF + cos-similarity and TF-IDF + SVD + k-means clustering. These models may do a great job of finding similar destinations but I wanted to use a model that lets me add place characterstics such as 'beach' or 'wine' in my search. So I decided to go with a recent model created at Google called word2vec. Word2vec is an amazing model that turns words into vectors that capture the 'meaning' of words. The cool feature about this model is that you can add/subtract words because they are vectors. For example, you can do something like 'king' - 'man' + 'woman' and this will result to a vector that ~= 'queen'. I trained word2vec on the wikivoyage articles to learn the meaning of places and words in travel context so I could do vector operations to find the most similar places. 

With word2vec, I was able to get recommendations of words/destinations that have the closest semantic meaning to the search queries. But I had to figure out a method to figure out which recommendations are actually geographic locations and which were just close words. I was able to use Wikivoyage's geolocation data to check this.

Once I trained the model on travel context, I decided to build a web application based on Bootstrap to deliver my data science project. I was able to use javascript to perform AJAX calls to update the results of user queries to a MapBox map. 


*I also gathered New York Times' travel, world, and science (which has a lot of environmental articles) news to enrich my data source but decided to leave it out as the results were too 'news-ish'. 

## Methodology
The code folder is divided into three sections 1) data collection, 2) EDA, 3) model. I will walk through each step/file in this section. 

### 1) Gathering Data
####Wikivoyage
There are three files for wikivoyage data.

1) wikivoyage_xml_to_json.py

The purpose of this file is to convert Wikivoyage travel guide articles to JSON format. Wikivoyage provided a data dump of its articles in XML format and I converted it to JSON format to go through exploratory data analysis with pandas. 

2) wikivoyage_geotags_sql.py

The purpose of this file is to gather the geolocations of articles (places). Wikivoyage provided the geolocations of articles as a sql file. I created my own MySQL database to load in and query the data. I also did a bit of data cleaning in this file to remove the accents. 

3) scrap_wikivoyage_banners.py

This file contains code that I used to scrap the banner images of articles from wikivoyage. I also used this to collect the canonical url of the wikivoyage page. I had to search places using a special search page on Wikivoyage to overcome minor syntax differences in place names. 

#### New York Times
4) nyt_articles_api.py

This file was use to gather most recent NYT articles in World, Science, and Travel sections. MongoDB was used to save the articles called with the official NYT API. Data was collected but was not incorporated to the model because the articles contained too much news like semantics. 


### 2) EDA

Exploratory data analysis and data cleaning have been performed with ipython notebook. Wikivoyage and NYT data were loaded, cleaned, pickled out as input format for word2vec, which is list of sentences where sentences are represented as list of words. Also, global NOAA weather data have been downloaded but later have been determined that it leaves out major parts of the world. Thus, more data has to be collected to incorporate the weather to the project.  

### 3) Model

Where2go is based on a model created at Google called word2vec. Word2vec is a neural network with 1 hidden layer that has continuous bag of words (CBOW) or skip-grams implementation. Where2go uses the version that uses skip-grams and hierarchical softmax for optimization. 

On the high level, word2vec tries to train the neural network to paramatize a model that can predict the surrounding words for every word on the corpus. The predictions are then used to backpropogate and optimize the parameters to make words with similar contexts to be closer together, while being further away from words that have different contexts.
The input-hidden layer weighting matrix, which is also the vector representation of words, is then used to gain insight into the meaning/similarity of words. 

In my where2go_model.py file, I implemented gensim's word2vec model and wrote functions to vectorize user search queries and functions to filter the recommendations to actual geolocations and output destinations in geojson format.

### Webapp
I was able to launch my own website using python Flask. I used javascript to perform ajax calls for the search engine so that I could run users' search query on my model to predict the most similar places and show my recommendations on the map. The flask file is named 'app.py' and can be found in the folder 'webapp'; the 'index.html' file that contains the html and javascript can be found in the folder 'templates'. I used Bootstrap to design my website. 

## Final Remarks
This project has been very fun and intellectually challenging. I started this application as a capstone project but there are so many things I would like to add to this app. I really want to add more travel guide data to make my results more robust, add historical weather data to help users decide when to go to a destination, and add average flight and hotel costs to help users choose plausible places. If you have any comments and recommendations for this project, please feel free to contact me. Also, I am looking for data science opportunities! You can reach me through my linkedin page, www.linkedin.com/in/dongwonwynnahn 




