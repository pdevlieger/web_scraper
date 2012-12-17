from flask import Flask, render_template
import os

import dblib
db = dblib.get_connection()

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
    if 'MONGOLAB_URL' in os.environ:
        app.run(debug=True)
    else:
        port_number = int(os.environ.get('PORT', 5000))
        app.run(host = '0.0.0.0', port = port_number, debug=True)
