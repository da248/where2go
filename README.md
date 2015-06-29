# where2go

Having trouble figuring out where to go for summer vacation? Have some places you like and want to figure out similar places? Where2go was built to recommend you places2go based on places/characterstics you like or dislike. This is a project built in two weeks as a capstone project for Galvanize Data Science Immersive (f.k.a. Zipfian Academy) program.

#### Try it out on www.where2go.help

## Motivation
There are a lot of websites that tell you the cheapest ways to get to a destination and the cheapest hotels to stay at. But why don't they tell us where we should go based on our travel taste? Articles like "XX's Top 25 Travel Destinations" or "YY's 100 Places You Must Visit!" tell you about interesting places around the world but I wanted to build a tool that will tell me where I should go based on my own experience and taste.

## Overview
One of the motivations for this applicaiton was building an unbiased recommendation system that will consider the destination's characterstics instead of looking at destinations that others liked. To do this, I decided to use travel guides to gather destination information. I found that Wikivoyage provided great travel guides that tell you about the history and culture of the place as well as what to see, how to get around, etc. *

The next question was then to figure out which model to use. The traditional recommendation systems for natural language processing include models like TF-IDF + cos-similarity and TF-IDF + SVD + k-means clustering. These models may do a great job of finding similar destinations but I also wanted to use a model that lets me add place characterstics such as 'beach' or 'wine' in my search. So I decided to go with a recent model created at Google called word2vec. Word2vec is an amazing model that turns words into vectors that capture the 'meaning' of words. The cool feature about this model is that you can add/subtract words because they are vectors. For example, you can do something like 'king' - 'man' + 'woman' and this will result to a vector that ~= 'queen'. I trained word2vec on the wikivoyage articles to learn the meaning of places and words so I could do vector operations to find the most similar places. 

With word2vec, I was able to get recommendations of words/destinations that have the closest semantic meaning to the search queries. But I had to figure out a method to figure out which recommendations are actually geographic locations and which were just close words. I was able to use Wikivoyage's geolocation data to check this.

Once I trained the model on travel context, I decided to build a web application based on Bootstrap to deliver my data science project. I was able to use javascript to perform AJAX calls to update the results of user queries to a MapBox map. 


*I also gathered New York Times' travel, world, and science (which has a lot of environmental articles) news to enrich my data source but decided to leave it out as the results were too 'news-ish'. 

## Methodology
The code folder is divided into three sections 1) data_collection, 2) EDA, 3) model. I will walk through each step/file in this section. 

### 1) Gathering Data
####Wikivoyage
There are three files for wikivoyage data.

1) wikivoyage_xml_to_json.py

The purpose of this file is to convert the travel guide articles from Wikivoyage to usable format. Wikivoyage provided a data dump of its articles in XML format and I converted it to JSON format to go through exploratory data analysis with pandas. 

2) wikivoyage_geotags_sql.py

The purpose of this file is to gather the geolocations of articles (places). Wikivoyage provided the geolocations of articles as a sql file. I created my own MySQL database to load in and query the data. I also did a bit of data cleaning in this file to remove the accents. 

3) scrap_wikivoyage_banners.py

This file contains code that I used to scrap the banner images of articles from wikivoyage. I also used this to collect the canonical url of the wikivoyage page. I had to search places using a special search page on Wikivoyage to get over minor syntex differences in place names. 

#### New York Times
4) nyt_articles_api.py

This file was use to gather most recent NYT articles in World, Science, and Travel sections. MongoDB was used to save the articles called with the official NYT API. Data was collected but was not incorporated to the model because the articles contained too much news like semantics. 


### 2) EDA

Exploratory data analysis and data cleaning have been performed with ipython notebook. Wikivoyage and NYT data were loaded, cleaned, pickled out as input format for word2vec, which is list of sentences where sentences are represented as list of words. Also, global NOAA weather data have been downloaded but it was found with EDA that it left out major parts of the world. Thus, more research has to be done to incorporate the weather data to the project.  

### 3) Model

TBC




