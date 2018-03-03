from pymongo import MongoClient

import tweepy
import tweepy.api
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import StreamListener

import sys
import json

#Starts the stream and samples tweets
def main():
    try:
        l = StdOutListener()
        #Setting up random keys
        stream = Stream(auth, l)
        #Sample used for random tweets
        stream.sample()
    except Exception as e:
        print(e)
        print("Connection Error")

#gets text from truncated or retweeted tweet
def getTextFromJSON(tweetJSON):
    print(tweetJSON["id"])
    #Reach the first origin tweet recursively
    if('retweeted_status' in tweetJSON) :
        print("Retweeted")
        return getTextFromJSON(tweetJSON["retweeted_status"])
    elif tweetJSON["truncated"] :
        #Handle the case the base tweet is truncated
        print("No retweet, truncated ")
        id = tweetJSON["id"]
        extendedTweet = api.get_status(id, tweet_mode='extended')
        extendedTweetJSON = extendedTweet._json
        return extendedTweetJSON["full_text"]
    else :
        #Nice simple tweet
        print("Sweet ol' tweet")
        return tweetJSON["text"]

#inserts tweets in the collection as a document of the format : 
#{"_id" : tweetID, "text":fullTextOfTweer}
def insertTweet(data):
    try : 
        d = json.loads(data)
        if d["lang"] == "en" :
            print("-----------------------------------------------")
            fullText = getTextFromJSON(d)
            print(fullText)
            tDic = {}
            tDic["_id"] = d["id"]
            tDic["text"] = fullText
            collection.insert_one(tDic)
            print("-----------------------------------------------")

        else:
            print("-----------------------------------------------")
            print("Non English Tweet")
            print("-----------------------------------------------")
    except Exception as ee:
        print("Delete Request Encountered")

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        global collection
        if collection.count() >= numTweets:
            sys.exit()
        insertTweet(data)
        return True

    def on_error(self, status):
        print("Error")
        return False


####Starting up the connection
client = MongoClient('localhost',27017)
db = client.precogTask
collection = db.tweetCollection
count = collection.count()

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="XXXXXXXXXXXXXXXX"
consumer_secret="XXXXXXXXXXXXXXXXXXXX"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="XXXXXXXXXXXXXXXXXXXXXXXXXXx"
access_token_secret="XXXXXXXXXXXXXXXXXXXXXXXXXX"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

numTweets = 10000
#This has been done to handle crashes
while collection.count() <= numTweets:
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception:    
        print("Crash Restarting")

print("10000 tweets mined")