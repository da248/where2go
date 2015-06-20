import pymysql.cursors
import unicodedata

import cPickle

# Connect to the database
connection = pymysql.connect(user='admin',
                             db='wiki',
                             cursorclass=pymysql.cursors.DictCursor)

geotag_dict = {}

def rmdiacritics(char):
    '''
    Return the base character of char, by "removing" any
    diacritics like accents or curls and strokes and the like.
    '''
    desc = unicodedata.name(unicode(char))
    cutoff = desc.find(' WITH ')
    if cutoff != -1:
        desc = desc[:cutoff]
    return unicodedata.lookup(desc)

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([rmdiacritics(c) for c in nkfd_form])

# Create dictionary of titles that have concatenated names as the values. For example: San Francisco: San_Francisco
def clean_title(title):
	value = remove_accents(title)
	value = unicodedata.normalize('NFKD', value).encode('ascii','ignore')
	value = value.replace(' ','_')

	return value


try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = '''
		        SELECT p.page_id, p.page_title, p.page_len, g.gt_lat, g.gt_lon
		        FROM geo_tags g
		        JOIN page p
		        ON p.page_id = g.gt_page_id

		        where g.gt_primary = 1
		        ;

		        '''
        cursor.execute(sql)
        result = cursor.fetchall()

        for row in result:
	        key = clean_title(row['page_title'])
	       	del row['page_title']

	        geotag_dict[key] = row


finally:
    connection.close()

with open('../data/geotag_dict.pkl','wb') as f:
	cPickle.dump(geotag_dict, f)



