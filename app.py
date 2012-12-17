from flask import Flask, render_template
from pymongo import Connection
from urlparse import urlsplit
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<player>')
def player_data(player):
    permanent_stats = db.footballpermanent.find({'name': player})[0]
    match_stats = [x for x in db.footballparser.find({'name': player})]
    last_match = [x for x in match_stats if x['url']!='n/a'][-1]
    next_match = [x for x in match_stats if x['url']=='n/a'][0]
    template_data = {
            'name' : player,
            'stats' : permanent_stats,
            'last_match' : last_match,
            'next_match' : next_match,
            }
    return render_template('template.html', **template_data)

if __name__ == '__main__':
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
        app.run(host = '0.0.0.0', port = port_number, debug=True)
