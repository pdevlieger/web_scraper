from database_static import static_data
from database_matches import get_player_match_stats, get_calendar_for_player
from template_builder import template_builder
from pymongo import Connection

"""   connecting to mongoDB..."""
connection = Connection()
db = connection
collection_1 = db.footballparser
collection_2 = db.footballpermanent

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
	collection_1.remove()
	collection_2.remove()
	for name in ['Moussa Dembele', 'Marouane Fellaini', 'Vincent Kompany', 'Romelu Lukaku', 'Simon Mignolet', 'Thomas Vermaelen', 'Jan Vertonghen']:
		collection_1.insert(set_calendar_stats(name))
		collection_2.insert(set_perm_scores(name))

make_database()