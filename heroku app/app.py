import pymongo
from nltk import word_tokenize
import re
from collections import Counter
from nltk.corpus import stopwords
from highcharts import Highchart
from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'electiondata'
app.config['MONGO_URI'] = 'mongodb://election:rooney_10@ds139817.mlab.com:39817/electiondata'

mongo =  PyMongo(app)
##define functions here
#def get_db():	

@app.route('/')
def index():
	user = mongo.db.tweets
	total_tweets = user.count()
	total_rts = user.count({ "retweeted_status" : { "$exists" : True }})
	total_original = user.count({ "retweeted_status" : { "$exists" : False }}) 
	total_text = user.count({"entities.media.type": {"$exists": False}})
	total_img = user.count({"entities.media.type": {"$eq": "photo"}})
	return render_template('template.html', total_tweets=total_tweets, total_rts =total_rts, total_original = total_original)

@app.route('/Top10')
def Top10():
	return render_template('column-highcharts.html')

@app.route('/Tweets')
def Tweets():
        return render_template('OTs_vs_RTs.html')

@app.route('/Type')
def Type():
        return render_template('TypeOfTweets.html')

@app.route('/Map')
def Map():
	return render_template('map.html')

if __name__ == "__main__":
	#call here for initilising if required
	app.run(debug=True)



