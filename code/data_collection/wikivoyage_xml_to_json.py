import xmltodict
import json
from collections import defaultdict
import pandas as pd


def convert_xml_to_json(filename):
	'''
	Convert xml wikivoyage file to json
	'''

	xml_str = open(filename).read()
	o = xmltodict.parse(xml_str)

	json_str = json.dumps(o)
	json_d = json.loads(json_str)

	with open('data/wikivoyage/wikivoyage.json', 'wb') as j:
		j.write(json.dumps(json_d))

	return json_d


if __name__ == '__main__':
	jdata = convert_xml_to_json('data/wikivoyage/enwikivoyage-latest-pages-articles.xml')
