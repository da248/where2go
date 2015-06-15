import xmltodict, json
from collections import defaultdict
import pandas as pd

def convert_xml_to_json(filename):

	xml_str = open(filename).read()
	o = xmltodict.parse(xml_str)

	json_str = json.dumps(o)
	json_d = json.loads(json_str)

	with open('data/wikivoyage.json','wb') as j:
		j.write(json.dumps(json_d))

	return json_d


if __name__ == '__main__':
	jdata = convert_xml_to_json('data/enwikivoyage-latest-pages-articles.xml')

	# json_d.keys()
	# json_d['mediawiki'].keys()
	# json_d['mediawiki'].keys()['page']
	# json_d['mediawiki']['page']
	# type(json_d['mediawiki']['page'])
	# json_d['mediawiki']['page'][0]
	# json_d['mediawiki']['page'][10]
	# json_d['mediawiki'].keys()
	# type(json_d['mediawiki']['siteinfo'])
	# json_d['mediawiki']['siteinfo'].keys()
	# json_d['mediawiki']['siteinfo']['case']
	# json_d['mediawiki']['siteinfo']['generator']
	# lst = json_d['mediawiki']['page']
	# len(lst)
	# lst[100]
	# lst[105]
	# lst[1000]