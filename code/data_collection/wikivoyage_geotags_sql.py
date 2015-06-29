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


def clean_title(title):
    '''
    Create dictionary of titles that have concatenated names as the values.
    For example: San Francisco: San_Francisco

    '''

    value = remove_accents(title.decode('utf-8'))
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = value.replace(' ', '_')

    return value

def create_geotag_dict():
  with connection.cursor() as cursor:

      sql = '''
            SELECT p.page_id, p.page_title, p.page_len, g.gt_lat, g.gt_lon
            FROM geo_tags g
            JOIN page p
            ON p.page_id = g.gt_page_id
            WHERE g.gt_primary = 1
            ;
            '''

      cursor.execute(sql)
      result = cursor.fetchall()

      for row in result:
          key = clean_title(row['page_title']).lower()
          del row['page_title']
          geotag_dict[key] = row

  return geotag_dict

def pickle_geotag_dict(dict, output_file_path):
  with open(output_file_path, 'wb') as f:
      cPickle.dump(dict, f)


if __name__ == '__main__':
  geotag_dict = create_geotag_dict():
  pickle_geotag_dict(geotag_dict, '../data/geotag_dict.pkl')