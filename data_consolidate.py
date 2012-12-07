import os
import pickle
from database_static import static_data
from database_matches import get_player_match_stats, get_calendar_for_player
from template_builder import template_builder
from pymongo import Connection

"""   connecting to mongoDB..."""
connection = Connection()
db = connection.test
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

#def update_calendar_stats(name):
#	os.chdir('/Users/pieterdevlieger/web_scraper/data/')
#	db_pklfile = open('days_played_%s.pkl' % name, 'r')
#	db_calendar = pickle.load(db_pklfile)
#	db_pklfile.close()
#	calendar = get_calendar_for_player(name)
#	calendar_played = [day for day in calendar if day[5]!='n/a']
#	if len(db_file) >= len(calendar_played):
#		pass
#	else:
#		matches_to_append = len(db_file) - len(calendar_player)
#		to_append = calendar_played[matches_to_append:]
#		for day in to_append:
#			url = day[5]
#			match_stats = get_player_match_stats(url, name)
#			day.append(match_stats)
#			db_calendar.update(day)
#		file_2 = open('days_played_%s.pkl' % name, 'w')
#		pickle.dump(days_played, file_2)
#		file_2.close()
	#elif base not same =>doublecheck function. zip
#	calendar_scheduled = [day for day in calendar_played if day[5]=='n/a']
#	for day in calendar_scheduled:
#		day = list(day)
#		day.append(None)
#		days_scheduled.append(day)
#	file_3 = open('days_scheduled_%s.pkl' % name, 'w')
#	pickle.dump(days_scheduled, file_3)
#	file_3.close()
#	os.chdir('/Users/pieterdevlieger/web_scraper/')

#def HTML_builder(name):
#	
#	
#	os.chdir('/Users/pieterdevlieger/web_scraper/templates')
#	template_builder(db_perm, db_played[-1], db_scheduled[0], name)
#
#for name in url_by_player.keys():
#	HTML_builder(name)