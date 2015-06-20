import requests
import json

payload = {'datasetid': 'GHCNDMS',
		   'datatypeid': ['MMXT','MMNT','MNTM'],
		   'startdate': '2014-06-05',
		   'enddate': '2015-06-05',
		   'limit': 10}

url = 'http://www.ncdc.noaa.gov/cdo-web/api/v2/data?'

r = requests.get(url, params=payload, headers = {'token': 'dZpmfqxxGSJlkTMyVHubkKDJzjLQeIhV'})

if __name__=='__main__':
    print r.text