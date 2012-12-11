from flask import Flask, render_template
from pymongo import Connection

app = Flask(__name__)

mongodb_uri = 'mongodb://localhost:27017'
db_name = 'mongoquest'
try:
	connection = Connection(mongodb_uri)
	database = connection[db_name]
except:
	print('Error')
	connection = None

#connection = Connection()
db = connection.test
collection_1 = db.footballparser
collection_2 = db.footballpermanent

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/<name>')
def player_data(name):
	return render_template('%s.html' % name)

if __name__ == '__main__':
	if connection:
		app.run(debug=True)

#	mongodb_uri = 'mongodb://localhost:27017'
#	db_name = 'mongoquest'
#	try:
#		connection = Connection(mongodb_uri)
#		database = connection[db_name]
#	except:
#		print('Error: unable to connect to database. ')
#		connection = None
#	if connection:
#		app.run