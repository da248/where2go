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

	result['top_places'] = []
	app.result = result
	return render_template('index.html', data=result)


@app.route('/map', methods=['POST'])
def userinput():
	data = request.data

	ms = app.where2go.most_similar(data)
	top_places_json = app.where2go.get_top_places_json(ms)	
	
	app.result['top_places'] = top_places_json
	print top_places_json
	return json.dumps(app.result)

if __name__ == '__main__':
	app.where2go = load_pickle()

	app.run(host= '0.0.0.0', port=80, debug=True)
