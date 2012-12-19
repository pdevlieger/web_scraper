from database_static import static_data
from database_matches import get_player_match_stats, get_calendar_for_player
from pymongo import Connection
from urlparse import urlsplit
import os
import dblib

players = ['C. Benteke','Moussa Dembele','Marouane Fellaini','Eden Hazard',
'Vincent Kompany','Romelu Lukaku','Simon Mignolet','Kevin Mirallas','Thomas Vermaelen',
'Jan Vertonghen','Kevin De Bruyne','Igor De Camargo','Timmy Simmons','Daniel Van Buyten',
'Thibaut Courtois','Jean-Francois Gillet','Gaby Mudingayi','Radja Nainggolan',
'Toby Alderweireld']

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
	for name in ['Moussa Dembele', 'Marouane Fellaini', 'Romelu Lukaku', 'Jan Vertonghen']:
		print name
		db.footballparser.insert(set_calendar_stats(name))
		print "matches done!"
		db.footballpermanent.insert(set_perm_scores(name))
		print "perms done!"

if __name__ == '__main__':
# mongodb://heroku_app9943363:ltoo03cli1dnufi04kepkljv4l@ds045147.mongolab.com:45147/heroku_app9943363
	url=os.environ.get('MONGOLAB_URI', 'mongodb://localhost:27017')
	if url == 'mongodb://localhost:27017':
		db_name = 'test'
		db = Connection(url)[db_name]
	else:
		port_number = int(os.environ.get('PORT', 5000))
		parsed = urlsplit(url)
		db_name = parsed.path[1:]
		db = Connection(url)[db_name]
		user_pass = parsed.netloc.split('@')[0].split(':')
		db.authenticate(user_pass[0], user_pass[1])
	make_database()
    db = dblib.get_connection()
    db.footballparser.remove()
    db.footballpermanent.remove()
    for name in ['Moussa Dembele', 'Marouane Fellaini', 'Romelu Lukaku', 'Simon Mignolet', 'Thomas Vermaelen', 'Jan Vertonghen']:
        db.footballparser.insert(set_calendar_stats(name))
        db.footballpermanent.insert(set_perm_scores(name))

if __name__ == '__main__':
    make_database()
