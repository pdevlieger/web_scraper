from pymongo import Connection
import os
from urlparse import urlsplit

def get_connection():
    url=os.environ.get('MONGOLAB_URI', 'mongodb://localhost:27017')
    if url == 'mongodb://localhost:27017':
        db_name = 'test'
    else:
        parsed = urlsplit(url)
        db_name = parsed.path[1:]
    db = Connection(url)[db_name]
    return db