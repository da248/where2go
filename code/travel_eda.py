
# coding: utf-8

# # WIKIVOYAGE EDA

# In[1]:

import pandas as pd
import json
from collections import defaultdict
import unicodedata
import mistune
from bs4 import BeautifulSoup
import string
import re
from nltk.tokenize import sent_tokenize, word_tokenize


# ##Load & Extract Articles

# In[2]:

with open('../data/wikivoyage.json','rb') as f:
    data = json.loads(f.read())


# ###Extract Article texts

# In[3]:

articles = data['mediawiki']['page']


# ### Save Articles by Titles

# In[4]:

articles_dict = {}
for article in articles:
    # Lets strip the accents using unicodedata
    title = unicodedata.normalize('NFKD', article['title']).encode('ascii','ignore')
    articles_dict[title] = article


# In[5]:

articles_dict.keys()[:10]


# __You can see that some articles are files, categories ,etc with : in their names.  
# Lets see how many of these there are.__

# In[6]:

junk_articles_dict = defaultdict(int)
for article in articles:
    title = article['title']
    if ':' in title:
        junk_articles_dict[title.split(':')[0]] += 1

print len(junk_articles_dict)
junk_articles_dict


# __There are a lot of special type articles. Let's actually take a look at the content to see if they are useful.__

# In[7]:

special_articles_dict = defaultdict(list)
for article in articles:
    title = article['title']
    if ':' in title:
        if len(special_articles_dict[title.split(':')[0]]) < 5:
            special_articles_dict[title.split(':')[0]].append(article) 

print len(special_articles_dict)
special_articles_dict.keys()


# __Let's take a look at two most common special type articles__

# In[8]:

special_articles_dict['MediaWiki']


# In[9]:

special_articles_dict['Wikivoyage']


# __These special articles are not actual travel guide articles so I will create a new dictionary without them.__

# In[10]:

# articles without :'s in their titles
articles_dict = {}
for article in articles:
    # Lets strip the accents using unicodedata
    title = unicodedata.normalize('NFKD', article['title']).encode('ascii','ignore')
    if ':' not in title:
        articles_dict[title] = article

print len(articles_dict)
articles_dict[articles_dict.keys()[1]]


# ### Now that we have a dictionary of travel guide articles, lets check out the article lenghts.

# In[11]:

article_lengths_dict = {}
for key, value in articles_dict.iteritems():
    article_length = len(value['revision']['text']['#text'])
    article_lengths_dict[key] = article_length

article_lengths_dict


# __Check out some articles with short lengths__

# In[12]:

articles_dict['Berneray (disambiguation)']


# In[13]:

df_article_lengths = pd.DataFrame(article_lengths_dict.items(), columns = ['title', 'length'])


# __Plot histogram to see the distribution of articles by length.__

# In[14]:

condition1 = df_article_lengths['length'] < 10000
df_article_lengths[condition1].hist(bins=100);


# In[15]:

### STUDY HOW MANY CHARS ARTICLES HAVE.
condition2 = df_article_lengths['length'] < 500
df_article_lengths[condition2].hist(bins=10)

## IT CAN BE SEEN THAT THERE ARE ABOUT 17,000 ARTICLES LESS THAN 200 CHARACTERS.
## ARTICLES WITH LESS THAN 200 WORDS WOULD MEAN THEY DON'T HAVE GOOD DESTINATION DESCRIPTONS OR ARE AMBIGUOUS DESTINATIONS, MEANING THEY AREN'T
## POPULAR DESTINATIONS.


# In[16]:

condition3 = df_article_lengths['length'] < 200
df_article_200_char_plus = df_article_lengths[-condition3]


# In[17]:

final_titles = df_article_200_char_plus['title']


# In[18]:

print final_titles.head(10)


# In[19]:

final_articles = {}
for title in final_titles:
    final_articles[title] = unicodedata.normalize('NFKD', articles_dict[title]['revision']['text']['#text']).encode('ascii','ignore')
final_articles
print len(final_articles)


# In[1]:

#final_articles['Paris']


# In[22]:

def clean_paragraph(string):
    # get rid of https:
    m = re.sub(r'(https?://\S+\ +\S+)', '', string)
    # get rid of [File:stuff]
    m = re.sub(r'\[File:[^)]*\]','', m)
    # get rid of ==stuff==
    m = re.sub(r'(\=+[^)]+\=+)','', m)
    #get rid of ], [, '. E.g. [[Paris]] --> Paris
    m = re.sub(r'[\[\]\']','',unicodedata.normalize('NFKD', m).encode('ascii','ignore')).strip()

    return m


# In[23]:

def clean_sentence(string):
    # punctuation and numbers to be removed
    punctuation = re.compile(r'[-.?!,":;()|0-9]')
    sent = re.sub(punctuation,'', string)
    return sent


# In[ ]:




# In[24]:

def convert_article_into_list_of_words(article):
    md = mistune.markdown(article)
    parsed_md = BeautifulSoup(md)
    
    parsed_test_wo_dict = []
    
    #Grab all the paragraphs and lists
    for line in parsed_md.find_all(['p','li']):
        text = line.text
        
        #remove dictionaries by filtering on {{
        if '{{' not in text:
            #clean the paragraph by removing things like https:stuff, File:stuff
            text = clean_paragraph(text)
            
            #tokenize paragraph to sentences
            sentences = sent_tokenize(text)
            
            for sentence in sentences:
                #clean sentence by removing numbers and punctuations
                sent = clean_sentence(sentence)
                #convert sentence to list of words
                word_list = sent.split()
                #keep the sentence if there are more than 3 words.
                if len(word_list) > 3:
                    parsed_test_wo_dict.append(word_list)
    return parsed_test_wo_dict


# In[ ]:

final_articles_words = {}

for key, value in final_articles.iteritems():
    final_articles_words[key] = convert_article_into_list_of_words(value)



