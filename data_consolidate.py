from database_static import static_data
from database_matches import get_player_match_stats, get_calendar_for_player
import dblib

player_list = ['C. Benteke','Moussa Dembele','Marouane Fellaini',
    'Eden Hazard','Vincent Kompany','Romelu Lukaku','Simon Mignolet','Kevin Mirallas',
    'Thomas Vermaelen','Jan Vertonghen','Kevin De Bruyne','Igor De Camargo',
    'Timmy Simmons','Daniel Van Buyten','Thibaut Courtois','Jean-Francois Gillet',
    'Gaby Mudingayi','Radja Nainggolan','Toby Alderweireld']

def set_perm_scores(name):
    return static_data(name)

def set_calendar_stats(name):
    calendar = get_calendar_for_player(name)
    for day in calendar:
        url = day['url']
        day['Match stats'] = get_player_match_stats(url,name)
    return calendar

def make_database():
    db = dblib.get_connection()
    db.footballparser.remove()
    db.footballpermanent.remove()
    for name in player_list:
        db.footballparser.insert(set_calendar_stats(name))
        db.footballpermanent.insert(set_perm_scores(name))

if __name__  == '__main__':
    make_database()