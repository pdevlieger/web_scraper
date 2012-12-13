from database_static import static_data
from database_matches import get_player_match_stats, get_calendar_for_player
from template_builder import template_builder
from pymongo import Connection
from urlparse import urlsplit
#import os

"""   connecting to mongoDB on mongolab"""
#url=os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017')
url = 'mongodb://heroku_app9943363:ltoo03cli1dnufi04kepkljv4l@ds045147.mongolab.com:45147/heroku_app9943363'
#port_number = int(os.environ.get('PORT', 5000))
parsed = urlsplit(url)
db_name = parsed.path[1:]

db = Connection(url)[db_name]
#collection_1 = db.footballparser
#collection_2 = db.footballpermanent

"""
Step 1 is to store data as a dict I call 'data'

sample data {'competition': CL, 'ongoing_game': True, 'home_team': 'Arsenal', etc.}
Pass data to insert
	collection.insert(data)
"""

def set_perm_scores(name):
	return static_data(name)

def set_calendar_stats(name):
	calendar = get_calendar_for_player(name)
	for day in calendar:
		url = day['url']
		day.update(get_player_match_stats(url,name))
	return calendar

def make_database():
	db.footballparser.remove()
	db.footballpermanent.remove()
	for name in ['Moussa Dembele', 'Marouane Fellaini', 'Romelu Lukaku', 'Simon Mignolet', 'Thomas Vermaelen', 'Jan Vertonghen']:
		db.footballparser.insert(set_calendar_stats(name))
		db.footballpermanent.insert(set_perm_scores(name))

make_database()