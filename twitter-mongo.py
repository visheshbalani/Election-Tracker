from twython import TwythonStreamer
import pymongo
from pymongo import MongoClient
import json

API_KEY = "4Wg8fsjAUQQ5aqAbRyOJJ3wdS"
API_SECRET = "BQWiOowxMTrdFeeui5ZBirpmVgktK2GGrMFNkWmWiHOd6xx4e0"
OAUTH_TOKEN = "636967553-hpVoOirEHfUVvEjcUZbAEJQukkjxEOySQq1khPtt"
OAUTH_SECRET = "ansQMG5xnuYGwGq597ORyIUwsc9CmqH23ZKyyI2xWjf2D"

connection = MongoClient()
db = connection['electiondata']

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            	text =  data['text'].encode('utf-8')
		print text
		tweet_record = data
		#tweet_record["_id"] = data["id_str"]
		db["tweets"].insert(tweet_record)


    def on_error(self, status_code, data):
        print status_code
	pass

stream = MyStreamer(API_KEY, API_SECRET,OAUTH_TOKEN, OAUTH_SECRET)

stream.statuses.filter(track='#USElection, #trump, #clinton')
