from flask import Flask, render_template
from pymongo import Connection
from urlparse import urlsplit
import os

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<player>')
def player_data(player):
	permanent_stats = db.footballpermanent.find({'name': player})[0]
	match_stats = [x for x in db.footballparser.find({'name': player})]
	last_match = [x for x in match_stats if x['url']!='n/a'][-1]
	next_match = [x for x in match_stats if x['url']=='n/a'][0]
	# template.html has a number of inputs:
	# => name: just steal the player name from the url and pass it
	# => dictionary_perm: a dict that holds the more permanent over-all-season stats
	# => home_team: the home team of the match last played
	# => score: the score of the match last played
	# => away_team: the way team of the match last played
	# => dictionary_match: a dict that holds the stats of the last match played
	# => home_team_next: home team for the next match
	# => away_team_next: away team for the next match
	return render_template('template.html', name = player, dictionary_perm = permanent_stats,
	home_team = last_match['home team'], score = last_match['score'], away_team = last_match['away team'],
	dictionary_match = last_match, home_team_next = next_match['home team'], away_team_next = next_match['away team'])

if __name__ == '__main__':
#	url = 'mongodb://heroku_app9943363:ltoo03cli1dnufi04kepkljv4l@ds045147.mongolab.com:45147/heroku_app9943363'
	url=os.environ.get('MONGOLAB_URI', 'mongodb://localhost:27017')
	if url == 'mongodb://localhost:27017':
		db_name = 'test'
		db = Connection(url)[db_name]
		app.run(debug=True)
	else:
		port_number = int(os.environ.get('PORT', 5000))
		parsed = urlsplit(url)
		db_name = parsed.path[1:]
		db = Connection(url)[db_name]
#		user_pass = parsed.netloc.split('@')[0].split(':')
		app.run(host = '0.0.0.0', port = port_number, debug=True)