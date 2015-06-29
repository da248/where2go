from flask import Flask
from flask import request
from flask import render_template
from collections import defaultdict
import cPickle as pkl
import json
import random
import sys
sys.path.insert(0,'../code/model')
from where2go_model import Where2Go_Model

app = Flask(__name__)
app.result = None
app.where2go = None
# OUR HOME PAGE
#============================================

def load_pickle():
	return pkl.load(open('../data/pickles/where2go_model.pkl', 'rb'))

@app.route('/')
def welcome():

	# #PREPARE RESULT DICTIONARY THAT WILL BE PASSED TO HTML
	result = {}

	# myname = "Wynn"
	# search_place_holder = 'Example:   Spain   //   istanbul   //   Beijing + 1.5*beach   //   '
	# #top_places_json = [{"geometry": {"type": "Point", "coordinates": [4.3517, 50.8464]}, "type": "Feature", "properties": {"marker-size": "large", "marker-color": "#9c89cc", "marker-symbol": "rocket", "title": "BRUSSELS"}}, {"geometry": {"type": "Point", "coordinates": [5.7222, 45.2002]}, "type": "Feature", "properties": {"marker-size": "large", "marker-color": "#9c89cc", "marker-symbol": "rocket", "title": "GRENOBLE"}}, {"geometry": {"type": "Point", "coordinates": [7.4667, 51.5167]}, "type": "Feature", "properties": {"marker-size": "large", "marker-color": "#ede8e4", "marker-symbol": "rocket", "title": "DORTMUND"}}, {"geometry": {"type": "Point", "coordinates": [3.0633, 50.6372]}, "type": "Feature", "properties": {"marker-size": "large", "marker-color": "#ede8e4", "marker-symbol": "rocket", "title": "LILLE"}}, {"geometry": {"type": "Point", "coordinates": [-0.190278, 51.1472]}, "type": "Feature", "properties": {"marker-size": "large", "marker-color": "#9c89cc", "marker-symbol": "rocket", "title": "GATWICK_AIRPORT"}}, {"geometry": {"type": "Point", "coordinates": [-4.42, 36.7194]}, "type": "Feature", "properties": {"marker-size": "large", "marker-color": "#6c6c6c", "marker-symbol": "rocket", "title": "MALAGA"}}, {"geometry": {"type": "Point", "coordinates": [8.04306, 52.2789]}, "type": "Feature", "properties": {"marker-size": "large", "marker-color": "#fa946e", "marker-symbol": "rocket", "title": "OSNABRUCK"}}]

	# result['myname'] = myname
	

	# #where2go.last_search ###NEED TO BE FIXED
	# result['search_place_holder'] = search_place_holder
	# result['center_location'] = []
	result['top_places'] = []
	app.result = result
	return render_template('index.html', data=result)


@app.route('/map', methods=['POST'])
def userinput():
	data = request.data

	ms = app.where2go.most_similar(data)
	top_places_json = app.where2go.get_top_places_json(ms)	
	
	#center_location = [50,0]
	# top_places_json = [{"geometry": {"type": "Point", "coordinates": [4.3517, 150.8464]}, "type": "Feature", "properties": {"marker-size": "large", "marker-color": "#9c89cc", "marker-symbol": "rocket", "title": "BRUSSELS"}}, {"geometry": {"type": "Point", "coordinates": [5.7222, 145.2002]}, "type": "Feature", "properties": {"marker-size": "large", "marker-color": "#9c89cc", "marker-symbol": "rocket", "title": "GRENOBLE"}}, {"geometry": {"type": "Point", "coordinates": [7.4667, 151.5167]}, "type": "Feature", "properties": {"marker-size": "large", "marker-color": "#ede8e4", "marker-symbol": "rocket", "title": "DORTMUND"}}, {"geometry": {"type": "Point", "coordinates": [3.0633, 50.6372]}, "type": "Feature", "properties": {"marker-size": "large", "marker-color": "#ede8e4", "marker-symbol": "rocket", "title": "LILLE"}}, {"geometry": {"type": "Point", "coordinates": [-0.190278, 51.1472]}, "type": "Feature", "properties": {"marker-size": "large", "marker-color": "#9c89cc", "marker-symbol": "rocket", "title": "GATWICK_AIRPORT"}}, {"geometry": {"type": "Point", "coordinates": [-4.42, 36.7194]}, "type": "Feature", "properties": {"marker-size": "large", "marker-color": "#6c6c6c", "marker-symbol": "rocket", "title": "MALAGA"}}, {"geometry": {"type": "Point", "coordinates": [8.04306, 52.2789]}, "type": "Feature", "properties": {"marker-size": "large", "marker-color": "#fa946e", "marker-symbol": "rocket", "title": "OSNABRUCK"}}]
	#top_places_json = [{"geometry": {"type": "Point", "coordinates": [4.3517, 50.8464]}, "type": "Feature","properties": {"image": "static/banners/brussels.png", "url": "https://www.wikivoyage.org/wiki/brussels", "marker-size": "large", "marker-color": "#9c89cc", "marker-symbol": "rocket", "title": "BRUSSELS"}}]

	app.result['top_places'] = top_places_json
	print top_places_json
	return json.dumps(app.result)

if __name__ == '__main__':
	app.where2go = load_pickle()

	app.run(host= '0.0.0.0', port=7777, debug=True)
