from flask import Flask, render_template
from pymongo import Connection
import os

list_names = ['Moussa Dembele', 'Marouane Fellaini','Vincent Kompany','Romelu Lukaku',
'Simon Mignolet','Thomas Vermaelen','Jan Vertonghen']

#mongo_url = os.getenv('MONGOLAB_URI','mongodb://localhost:27017')

app = Flask(__name__)#, instance_relative_config=True)

port = int(os.environ.get('PORT', 5000))

connection = Connection('mongodb://heroku_app9943363:ltoo03cli1dnufi04kepkljv4l@ds045147.mongolab.com:45147/heroku_app9943363')
#connection = Connection('mongodb://heroku_app9943363:ltoo03cli1dnufi04kepkljv4l@ds045147.mongolab.com:45147/heroku_app9943363')
#connection = Connection()
db = connection
collection_1 = db.footballparser
collection_2 = db.footballpermanent

def get_name_stats(player):
	dictionary_permanent = db.footballpermanent.find()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<player>')
def player_data(player):
#	permanent_stats = [x for x in collection_2.find({'name': player})][0]
#	match_stats = [x for x in db.footballparser.find({'name': player})]
#	last_match = [x for x in match_stats if x['url']!='n/a'][-1]
#	next_match = [x for x in match_stats if x['url']=='n/a'][0]
	return render_template('template.html', name = player, dictionary_perm = {'Final rating': 4, 'Attacking': 5, 'Defending': 7},
#	home_team = last_match['home team'], score = last_match['score'], away_team = last_match['away team'],
#	dictionary_match = last_match, home_team_next = next_match['home team'], away_team_next = next_match['away team'])
	home_team = 'Manchester City', score = '3 - 1', away_team = 'Arsenal',
	dictionary_match = {'Goals': 0, 'Yellow card': 1, 'Man of the Match': True}, home_team_next = 'Sunderland', away_team_next = 'Manchester City')

#name = 'Vincent Kompany',
#	dictionary_perm = {'Final rating': 4, 'Attacking': 5, 'Defending': 7},
#	home_team = 'Manchester City',
#	score = '3 - 1',
#	away_team = 'Arsenal',
#	dictionary_match = {'Goals': 0, 'Yellow card': 1, 'Man of the Match': True},
#	home_team_next = 'Sunderland',
#	away_team_next = 'Manchester City'	

if __name__ == '__main__':
	if connection:
#		app.run(debug=True)
		app.run(host='0.0.0.0', port = port, debug=True)

# mongodb://heroku_app9943363:ltoo03cli1dnufi04kepkljv4l@ds045147.mongolab.com:45147/heroku_app9943363