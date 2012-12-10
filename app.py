from flask import Flask, render_template, request, session
from pymongo import Connection

app = Flask(__name__)

connection = Connection()
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
	app.run(debug=True)