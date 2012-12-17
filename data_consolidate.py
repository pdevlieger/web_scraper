from database_static import static_data
from database_matches import get_player_match_stats, get_calendar_for_player

import dblib

def set_perm_scores(name):
    return static_data(name)

def set_calendar_stats(name):
    calendar = get_calendar_for_player(name)
    for day in calendar:
        url = day['url']
        day.update(get_player_match_stats(url,name))
    return calendar

def make_database():
    db = dblib.get_connection()
    db.footballparser.remove()
    db.footballpermanent.remove()
    for name in ['Moussa Dembele', 'Marouane Fellaini', 'Romelu Lukaku', 'Simon Mignolet', 'Thomas Vermaelen', 'Jan Vertonghen']:
        db.footballparser.insert(set_calendar_stats(name))
        db.footballpermanent.insert(set_perm_scores(name))

if __name__ == '__main__':
    make_database()
