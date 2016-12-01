import pymongo
import json
from pymongo import MongoClient

client  = MongoClient()
db = client['electiondata']
collection = db['tweets']

geo = { 
	"type": "FeatureCollection",
	"features": []
}
for tweet_data in collection.find():
	if tweet_data["coordinates"]:
		geo_json = {
			"type" : "Feature",
			"geometry": tweet_data["coordinates"]
			}
		geo["features"].append(geo_json)

with open('geojsondata.json', 'w') as outfile:
	json.dump(geo, outfile)



