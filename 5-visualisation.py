from pymongo import MongoClient
from matplotlib import pyplot
import numpy
import tweepy
import tweepy.api
from tweepy import OAuthHandler
polarityCollection = MongoClient().precogTask.polarityCollection


count = 1

for wordData in polarityCollection.find():
    print(wordData['word'] + " : " + str(len(wordData['tweetPolarityList'])))
    bins = numpy.linspace(-1.05,1.05,20)
    pyplot.figure(count)
    fig = pyplot.figure()
    fig.canvas.set_window_title("Analysis of word " + wordData["word"])
    
    #Tweet Polarity
    pyplot.subplot(2,1,1)
    pyplot.xlabel("Polarity")
    pyplot.ylabel("Number of tweets with sentiment")
    pyplot.hist(wordData['tweetPolarityList'],bins,alpha=0.5, label='Tweets') 
    #alpha is transparency factor : 0 = transparent 1 = opaque
    
    #Article polarity
    pyplot.subplot(2,1,2)
    pyplot.xlabel("Polarity")
    pyplot.ylabel("Number of articles with sentiment")
    pyplot.hist(wordData['articlePolarityList'],bins,alpha=0.5, label='Articles')
    
    pyplot.legend(loc = 'upper right')
    count += 1

    
    #pyplot.subplot(2,2,3)
    #Tweet time : new data mined
    ##### Generating time and locations visualisations
    ####timeList = []
    ####print("-------------------------"+wordData['word']+"------------------------------------")
    ####Test visualisation for location
    ####for tweet in tweepy.Cursor(api.search,q=wordData['word'],tweet_mode='extended',language='en').items(1000):
    ####    tweetJSON = tweet._json
    ####    #if tweetJSON["geo"] != None:
    ####    #    print(tweetJSON["id_str"],end=" : ")
    ####    #    print(tweetJSON["geo"])
    ####    ### LACK OF GEOTAGGED DATA
    ####    time = tweetJSON['created_at']
    ####    timeList.append(time)
    ####    
    ####Test visualisation for time graph
    ####dates = []
    ####for t in times:
    ####    dates.append(time.strftime('%Y-%m-%d', time.strptime(t,'%a %b %d %H:%M:%S +0000 %Y')))
    ####
    ####    pyplot.hist(dates)
    ####pyplot.subplot(2,2,3)
    ####print(timeList)

pyplot.show()



