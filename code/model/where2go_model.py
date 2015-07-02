import gensim
import cPickle
import json
import random
import re
import requests
from bs4 import BeautifulSoup


class Where2Go_Model(object):

    def __init__(self):
        self.geotag_imglink_wikiurl = None
        self.wikivoyage_list = None
        self.nyt_list = None
        self.model = None
        self.colors = ['#f1f075', '#eaf7ca', '#c5e96f', '#a3e46b', '#7ec9b1',
                       '#b7ddf3', '#63b6e5', '#3ca0d3', '#1087bf', '#548cba',
                       '#677da7', '#9c89cc', '#c091e6', '#d27591', '#f86767',
                       '#e7857f', '#fa946e', '#f5c272', '#ede8e4', '#ffffff',
                       '#cccccc', '#6c6c6c', '#1f1f1f', '#000000']

    def load_data(self, nyt=False):
        '''
        Load in geotag_imglink_wikiurl, which is a dictionary that
        contains geolocations, img paths, and wikivoyage links.

        input: Boolean
        output: None (loads class data into class variable)
        '''

        with open('../../data/pickles/geo_imglink_wikiurl.pkl', 'rb') as f:
            self.geotag_imglink_wikiurl = cPickle.load(f)

        with open('../../data/pickles/wikivoyage_list_of_words.pkl', 'rb') as g:
            self.wikivoyage_list = cPickle.load(g)

        if nyt:
            with open('../../data/pickles/nyt_articles_word_list.pkl', 'rb') as h:
                self.nyt_list = cPickle.load(h)

    def fit(self, min_count=5, size=100):
        '''
        fit word2vec model using gensim with upto trigrams.
        '''
        bigram = gensim.models.Phrases(self.wikivoyage_list, min_count=10)

        trigram = gensim.models.Phrases(bigram[self.wikivoyage_list], min_count=10)

        model_bigrams = gensim.models.Word2Vec(trigram[self.wikivoyage_list],
                                               min_count=min_count, size=size)

        model_bigrams.init_sims(replace=True)

        self.model = model_bigrams

    def parse_search_query(self, string):
        '''
        Parse the user query to multipliers and destinations.

        input = string
        output = list tuples, where tuple = (number, word)
        '''
        multipliers = []
        words = []

        # replace 'minus' with 'plus minus'
        string = re.sub('-\s*', '+-', string)

        # split on 'plus'
        terms = string.split('+')
        terms = [x for x in terms if x != '']

        # for every words in between 'plus'
        for term in terms:
            # check if there is a multiplier
            split_by_ast = re.split('[*]', term)

            # if there is only a word, without multiplier
            if len(split_by_ast) == 1:
                word = split_by_ast[0].strip().lower()

                # if there is a 'minus' sign, then put the multiplier as -1, else multiplier = 1
                if '-' in word:
                    multipliers.append(-1.)
                    word = re.sub('-', '', word)
                else:
                    multipliers.append(1.)

                # replace space with underscore
                words.append(re.sub(' ', '_', word))

            # If there is a multiplier and a word, determine if its multiplier then word or vice versa.
            # Then replace 'space' with a 'underscore'
            elif len(split_by_ast) == 2:
                first = split_by_ast[0].strip()
                second = split_by_ast[1].strip()
                word_first = first.isalpha()

                if word_first:
                    multipliers.append(float(second))
                    words.append(re.sub(' ', '_', first.lower()))
                else:
                    multipliers.append(float(first))
                    words.append(re.sub(' ', '_', second.lower()))

        # normalize multipliers
        multipliers = [float(i)/sum(map(abs, multipliers)) for i in multipliers]
        query_terms = zip(multipliers, words)
        print query_terms

        return query_terms

    def most_similar(self, input, topn=40):
        '''
        use the trained word2vec model to give most similar recommendations to the input

        input = search string in the format of place/char + place/char -...
        output = top recommendations in json format
        '''
        terms = self.parse_search_query(input)

        # Set to make sure the output doesn't include one of the input destinations.
        check = set()

        # For (multiplier, destination), get the multiplier * vector of that destination.
        # Then sum up to the master vector.
        for i, term in enumerate(terms):
            multiplier, word = term
            check.add(word)
            if i == 0:
                master_vector = multiplier * self.model[word]
            else:
                master_vector += multiplier * self.model[word]

        # Find the most similar vectors to the amter vector
        ms = self.model.most_similar(positive=[master_vector], topn=topn)
        ms_wo_search_terms = [dest for dest in ms if dest[0] not in check]

        print
        print ms_wo_search_terms

        return ms_wo_search_terms

    def make_marker(self):
        '''
        make a maker with default values and random color

        input: None
        output: geojson marker
        '''
        color = random.choice(self.colors)
        geo_template = {"type": "Feature",
                        "geometry": {"type": "Point",
                                     "coordinates": []
                                     },
                        "properties": {"image": None,
                                       "url": None,
                                       "title": "",
                                       "marker-color": color,
                                       "marker-size": "large",
                                       "marker-symbol": "rocket"
                                       }
                        }

        return geo_template

    def get_top_places_json(self, ms, max_markers=10):
        '''
        turn the most similar recommendations to list of geojson markers.
        If there are more than 10 recommendations, just show top 10 most
        similar destinations.

        input = most similar places (out of self.most_similar())
        output = list of geojson markers.
        '''

        top_places = []
        num_show = 0
        for n, entry in enumerate(ms):
            place, sim = entry

            # Check if the recommendation is a geo location.
            if place in self.geotag_imglink_wikiurl:
                # If recommendation is a place, make a geojson marker and update the info.
                marker = self.make_marker()
                full_url = self.geotag_imglink_wikiurl[place]['wiki_url']
                img_src = self.geotag_imglink_wikiurl[place]['img_path']
                lat = self.geotag_imglink_wikiurl[place]['gt_lat']
                lon = self.geotag_imglink_wikiurl[place]['gt_lon']

                marker['geometry']['coordinates'].append(lon)
                marker['geometry']['coordinates'].append(lat)
                marker['properties']['image'] = img_src
                marker['properties']['url'] = full_url
                marker['properties']['title'] = place.upper()
                marker['properties']['marker-symbol'] = num_show + 1

                top_places.append(marker)

                # Check how many markers exist to make sure at most 10 markers show up.
                num_show += 1
                if num_show == max_markers:
                    return top_places
        return top_places

if __name__ == '__main__':
    where2go = Where2Go_Model()
    where2go.load_data()
    where2go.fit(min_count=20, size=150)

    with open('../../data/pickles/where2go_model.pkl', 'wb') as f:
        cPickle.dump(where2go, f)
