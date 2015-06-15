import json
from collections import defaultdict
import pandas as pd



def load_json_data():
	data = json.loads('data/wikivoyage.json')

	articles_list = jdata['mediawiki']['page']

	articles_dict = {}

	for article in articles_list:
		articles_dict[article['title']] = article

	return articles_dict


if __name__ == '__main__':


	articles_dict = load_json_data()




	article_len_dict = defaultdict(int)

	for key, value in articles_dict.iteritems():
		article_len_dict[len(value['revision']['text'])] += 1



	article_len_dict = defaultdict(int)

	for key, value in articles_dict.iteritems():
		if len(value['revision']['text']) == 1:
			print key

'''
Wikivoyage:Changing username/Open requests
File:WhereIsThis.jpg
'''

