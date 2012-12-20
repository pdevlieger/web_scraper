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
# mongodb://heroku_app9943363:ltoo03cli1dnufi04kepkljv4l@ds045147.mongolab.com:45147/heroku_app9943363
	url=os.environ.get('MONGOLAB_URI', 'mongodb://localhost:27017')
	print url
	if url == 'mongodb://localhost:27017':
		db_name = 'test'
		db = Connection(url)[db_name]
		app.run(debug=True)
	else:
		print 'yessariee'
		port_number = int(os.environ.get('PORT', 5000))
		parsed = urlsplit(url)
		db_name = parsed.path[1:]
		db = Connection(url)[db_name]
		user_pass = parsed.netloc.split('@')[0].split(':')
		db.authenticate(user_pass[0], user_pass[1])
		app.run(host = '0.0.0.0', port = port_number, debug=True)
=======
    if 'MONGOLAB_URL' in os.environ:
        app.run()
    else:
        port_number = int(os.environ.get('PORT', 5000))
        app.run(host = '0.0.0.0', port = port_number, debug=True)
>>>>>>> abcf0e23aea02b7c19fd223ae1cae6cb75285153
