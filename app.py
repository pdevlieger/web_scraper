from flask import Flask, render_template
from pymongo import Connection
import os
from template_builder import index_builder

#mongo_url = os.getenv('MONGOLAB_URI','mongodb://localhost:27017')

app = Flask(__name__, instance_relative_config=True)

port = int(os.environ.get('PORT', 5000))

connection = Connection('mongodb://heroku_app9943363:ltoo03cli1dnufi04kepkljv4l@ds045147.mongolab.com:45147/heroku_app9943363')
db = connection.test
collection_1 = db.footballparser
collection_2 = db.footballpermanent

@app.route('/')
def index():
	x = db.footballparser.find({"_id" : ObjectId("50c14d9e381c171001115c82")})
	string = x['name']
	return render_template(index_builder(string))

@app.route('/<name>')
def player_data(name):
	return render_template('%s.html' % name)

if __name__ == '__main__':
	if connection:
		app.run(host='0.0.0.0', port = port)


# mongodb://heroku_app9943363:ltoo03cli1dnufi04kepkljv4l@ds045147.mongolab.com:45147/heroku_app9943363