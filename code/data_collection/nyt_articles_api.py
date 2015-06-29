import requests
import bs4
import json
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, CollectionInvalid
import datetime as dt
import time

# Define the MongoDB database and table
db_cilent = MongoClient()
db = db_cilent['nyt_dump']
table = db['articles']


def single_query(link, payload):
    '''
    Query the NYT API once
    '''
    response = requests.get(link, params=payload)
    if response.status_code != 200:
        print 'WARNING', response.status_code
    else:
        return response.json()


# Determine if the results are more than 100 pages
def more_than_100_pages(total_page):
    if total_page > 100:
        pages_left = min(total_page - 100, 100)
        return 100, pages_left, True
    else:
        return total_page, 0, False


# Looping through the pages give the number of pages
def loop_through_pages(total_pages, link, payload, table):
    for i in range(total_pages):
        if i % 50 == 0:
            print ' || Page ||', i
        payload['page'] = str(i)
        content = single_query(link, payload)
        meta_lst = content['response']['docs']

        for meta in meta_lst:
            try:
                table.insert(meta)
            except DuplicateKeyError:
                print 'DUPS!'


def scrape_meta(days=1):
    '''
    Scrape the meta data (link to article and put it into Mongo)
    '''
    # The basic parameters for the NYT API
    # Url for NYT dev api
    link = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
    payload = {'api-key': '15504a1ea80590cff1e8aceed018cd55:10:72330163',
               'fq': 'section_name:("Travel" "World" "Science")'}

    today = dt.datetime(2015, 6, 16)
    for day in range(days):
        payload['end_date'] = str(today).replace('-', '').split()[0]
        yesterday = today - dt.timedelta(hours=24)
        payload['begin_date'] = str(yesterday).replace('-', '').split()[0]
        print 'Scraping period: %s - %s ' % (str(yesterday), str(today))

        content = single_query(link, payload)
        hits = content['response']['meta']['hits']
        total_pages = min((hits / 10) + 1, 100)
        print 'HITS', hits

        today -= dt.timedelta(days=2)

        loop_through_pages(total_pages, link, payload, table)


def get_articles(table, section=None):
    '''
    Get all the links, visit the page and scrape the content
    '''
    if not section:
        links = table.find({'content_txt': {'$exists': False}}, {'web_url': 1})
    else:
        links = table.find({'$and': [{'content_txt': {'$exists': False}},
                           {'section_name': section}]}, {'web_url': 1})

    counter = 0
    for uid_link in links:
        counter += 1
        if counter % 100 == 0:
            print 'Count: ', counter, ' '
            print uid
        uid = uid_link['_id']
        link = uid_link['web_url']
        try:
            html = requests.get(link).text
        except ConnectionError as e:
            print e
            table.update({'_id': uid}, {'$set': {'content_txt': ['disconnected!']}})

        if html.ok:
            soup = bs4.BeautifulSoup(html, 'html.parser')

            article_content = [i.text for i in soup.select('.story-body-text.story-content')]
            if not article_content:
                article_content += [i.text for i in soup.select('.caption-text')]
            if not article_content:
                article_content += [i.text for i in soup.select('[itemprop="description"]')]
            if not article_content:
                article_content += [i.text for i in soup.select('#nytDesignBody')]
            else:
                article_content += []

            table.update({'_id': uid}, {'$set': {'content_txt': article_content}})


def get_article_from_mongo(table, num_articles=-1, section=""):
    '''
    Get articles from MongoDB in to a list.
    '''
    # if num_articles not specified, use all articles with content
    if num_articles == -1:
        if section == "":
            num = table.find({'content_txt': {'$exists': True}}).count()
        else:
            num = table.find({'$and': [{'content_txt': {'$exists': True}}, {'section_name': section}]}).count()
    else:
        num = num_articles

    if section == "":
        articles = table.find({'content_txt': {'$exists': True}}, {'section_name': 1, 'content_txt': 1}).limit(num)
    else:
        articles = table.find({'$and': [{'content_txt': {'$exists': True}}, {'section_name': section}]},
                              {'section_name': 1, 'content_txt': 1}).limit(num)

    nyt_articles = []

    for uid_article in articles:
        body = uid_article['content_txt']

        nyt_articles.append(body)

    return nyt_articles


if __name__ == '__main__':
    # scrape_meta(365)
    get_articles(table)
