import pymongo
import re
from pymongo import MongoClient
from nltk import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from highcharts import Highchart

client  = MongoClient()
db = client['electiondata']
collection = db['tweets']

total_tweets  = collection.count()
total_rts = collection.count({ "retweeted_status" : { "$exists" : True }})  
total_original =  collection.count({ "retweeted_status" : { "$exists" : False }})
total_text = collection.count({"entities.media.type": {"$exists": False}})
total_img = collection.count({"entities.media.type": {"$eq": "photo"}})
#total_video = collection.count({"entities.extended_entities.type": {"eq": "video"}}) Extended entities not included by Twitter
data2 = [total_original, total_rts]
data3 = [total_text, total_img]

print "Total Number of Tweets: "
print  total_tweets
print "Total Number of RTs: "
print  total_rts
print "Total Number of Original Tweets: "
print  total_original

regex_str = [
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens

#stopwords = stopwords.words('english') + ['RT']
all_tokens = []

for tweet_data in collection.find():
	if 'text' in tweet_data:
		tokens =  preprocess(tweet_data["text"].encode('ascii','ignore').lower())
		#tokens = word_tokenize(tweet_data["text"].encode('ascii','ignore'))
		all_tokens += tokens
frequencies = Counter(all_tokens)

#for token,count in frequencies.most_common(50):
#	if token in stopwords or len(token)<2:
#		continue
#	print token,count

flag = 0
data1 = []
words = []
for token, count in frequencies.most_common(): #iteritems()
	if token.startswith('#') and flag<10:
		print token, count
		flag +=1
		data1.append(count)
		words.append(token) 

chart = Highchart()
options = {
'chart': {
        'type':'column',
	'margin':[70,70,70,70]},
'plotOptions': {
	'column': {'colorByPoint': True}
				},
'title':{
        'text':'Top 10 Hashtags'},
'xAxis':{
        'categories':words},
'yAxis':{
        'title':{
                'text':'Number of times mentioned'}
        },
'colors' : ['#00ff87', '#e90052', '#38003c', '#eaff04']
}
chart.set_dict_options(options)
chart.add_data_set(data1, 'column', 'Count')
chart.save_file('./column-highcharts')


chart2 = Highchart()
options = {
'chart': {
	'type':'column',
	 'margin':[100,100,100,100],
	},
'plotOptions': {
        'column': {'colorByPoint': True},
			},
'title':{
	'text':'Original Tweets and Retweeted Tweets'},
'xAxis':{
	'categories':['Original','Retweets']},
'yAxis':{
	'title':{
		'text':'Number of tweets'}
	},
'colors' : ['#00ff87', '#e90052']

}

chart2.set_dict_options(options)
chart2.add_data_set(data2, 'column', 'Count')
chart2.save_file('./OTs_vs_RTs')

chart3 = Highchart()
options = {
'chart': {
	'type':'column',
	 'margin':[100,100,100,100],
	},
'plotOptions': {
        'column': {'colorByPoint': True},
			},
'title':{
	'text':'Type of Tweets'},
'xAxis':{
	'categories':['Text','Text + Image']},
'yAxis':{
	'title':{
		'text':'Number of tweets'}
	},
'colors' : ['#00ff87', '#e90052']

}

chart3.set_dict_options(options)
chart3.add_data_set(data3, 'column', 'Count')
chart3.save_file('./TypeOfTweets')