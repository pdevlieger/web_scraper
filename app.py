from flask import Flask, render_template
from pymongo import Connection
#import os

#mongo_url = os.getenv('MONGOLAB_URI','mongodb://localhost:27017')

app = Flask(__name__)

connection = Connection('mongodb://heroku_app9943363:ltoo03cli1dnufi04kepkljv4l@ds045147.mongolab.com:45147/heroku_app9943363')
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


# mongodb://heroku_app9943363:ltoo03cli1dnufi04kepkljv4l@ds045147.mongolab.com:45147/heroku_app9943363