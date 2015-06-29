import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import json
import cPickle as pkl
import shutil
import itertools
import os


class Scrap_Wikivoyage_Banners(object):

	def __init__(self):
		self.locations = None

	def load_location(self):
		'''
		load the geolocation data.
		'''
		self.locations = pkl.load(open('../../data/pickles/geotag_dict.pkl', 'rb'))

	def make_default_img_url(self, place):
		'''
		input = place
		output = return the default values for img_path and wiki_url
		'''

		img_path = 'static/banners/default.png'
		wiki_url = 'https://en.wikivoyage.org/wiki/%s' % place
		return img_path, wiki_url

	def get_image_and_link(self, place):
		'''
		For a given place, get the canonical wikivoyage url and save the banner.
		If the banner is just a default banner, save the img path as the default
		banner to minimize duplicates.

		input: place as string
		output: img_path and wiki_url + (save image in the process)
		'''

		base_url = "https://en.wikivoyage.org/w/index.php?title=Special%3ASearch&profile=default&search="
		full_url = base_url + place.title()

		try:
			response = requests.get(full_url).text
			soup = BeautifulSoup(response, 'html.parser')
			wiki_url = soup.find(rel='canonical')['href']
			img_src = 'https:' + soup.select('div.topbanner a.image')[0].select('img')[0]['src']

		except IndexError:
			print 'INDEX ERROR!!! %s page did not exist' % place
			return make_default_img_url(place)

		except ConnectionError:
			print 'CONNECTION ERROR!!! RECONNECT TO %s page' % place
			return make_default_img_url(place)

		if 'Pagebanner_default' in img_src or 'default_banner' in img_src:
			print '%s has default banner!' % place
			img_path = 'static/banners/default.png'

		else:
			place = place.replace('/', '_')  # REPLACE SLASH BECAUSE IT CREATES A DIRECTORY

			try:
				img_response = requests.get(img_src, stream=True)
				img_path = 'static/banners/%s.png' % place

			except IndexError:
				print 'INDEX ERROR!!! %s page did not exist' % place
				return make_default_img_url(place)

			except ConnectionError:
				print 'CONNECTION ERROR!!! RECONNECT TO %s page' % place
				return make_default_img_url(place)

			# save the img file if it doesn't already exist. if it already exists, dont overwrite.
			if not os.path.exists('../../webapp/static/banners/%s.png' % place):
				with open('../../webapp/static/banners/%s.png' % place, 'wb') as out_file:
					shutil.copyfileobj(img_response.raw, out_file)
				del img_response
				print '%s.png successfully created' % place

			else:
				print '%s.png already exists!' % place

		return img_path, wiki_url

	def scrap_banners(self):
		'''
		Go through every key in the locations dictionary and scrape the wiki url and img_path.
		'''
		for key in self.locations.iterkeys():
			img_path, wiki_url = self.get_image_and_link(key)
			self.locations[key]['wiki_url'] = wiki_url
			self.locations[key]['img_path'] = img_path

	def pickle(self):
		'''
		Pickle out the locations.
		'''
		pkl.dump(self.locations, open('../../data/geotag_imglink_wikibanner.pkl', 'wb'))


if __name__ == '__main__':
	swb = Scrap_Wikivoyage_Banners()
	swb.load_location()
	swb.scrap_banners()
	swb.pickle()
