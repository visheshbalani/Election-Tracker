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

regex_str = [
        r'<[^>]+>', # HTML tags
        r'(?:@[\w_]+)', # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
        r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
        r'(?:[\w_]+)', # other words
        r'(?:\S)' # anything else]  
]
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
	return tokens_re.findall(s)

def preprocess(s, lowercase=False):
	tokens = tokenize(s)
        if lowercase:
       		tokens = [token.lower() for token in tokens]
       	return tokens


mongo =  PyMongo(app)
##define functions here

@app.route('/')
def index():
	user = mongo.db.tweets
	total_tweets = user.count()
	total_rts = user.count({ "retweeted_status" : { "$exists" : True }})
	total_original = user.count({ "retweeted_status" : { "$exists" : False }}) 
	
	#stopwords = stopwords.words('english') + ['RT']
	all_tokens = []
	for tweet_data in user.find():
		if 'text' in tweet_data:
			tokens =  preprocess(tweet_data["text"].encode('ascii','ignore').lower())
			all_tokens += tokens
	frequencies = Counter(all_tokens)
	

	flag = 0
	data1 = []
	words = []
	for token, count in frequencies.most_common(): #iteritems()
		if token.startswith('#') and flag<10:
			#print token, count
			flag +=1
			data1.append(count)
			words.append(token)


	return render_template('template.html', total_tweets=total_tweets, total_rts =total_rts, total_original = total_original, data1=data1, words=words)


if __name__ == "__main__":
	#call here for initilising if required
	app.run(debug=True)


