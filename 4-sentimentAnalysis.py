from pymongo import MongoClient
from textblob import TextBlob
from newspaper import Article
from newspaper import ArticleException

dataForEntityAnalysis = MongoClient().precogTask.dataForAnalysis.find()
tweetCollection = MongoClient().precogTask.tweetCollection

polarityCollection = MongoClient().precogTask.polarityCollection
polarityCollection.drop()
for ne in dataForEntityAnalysis:
    #Finding avg tweet polarity
    wordData = {}
    wordData['word'] = ne['word']

    tweetPolarityList = []
    totalTweetPolarity = 0
    print("analysing word " + ne['word'])
    for t in ne['tweetList']:
        print("analysing tweet " + str(t))
        tweet = tweetCollection.find_one({'_id' : t})
        tempPol = TextBlob(tweet['text']).sentiment.polarity
        tweetPolarityList.append(tempPol)
        totalTweetPolarity += tempPol
    avgTweetPolarity = totalTweetPolarity/len(ne['tweetList'])
    wordData['tweetPolarityList'] = tweetPolarityList

    #finding average article polarity
    totalArticlePolarity = 0
    articlePolarityList = []
    for articleURL in ne['articleLinksList']:
        print("analysing article " + articleURL)
        try:
            articleObj = Article(articleURL,language = 'en')
            articleObj.download()
            articleObj.parse()
            articleObj.nlp()
            tempPol = TextBlob(articleObj.text).sentiment.polarity
            totalArticlePolarity += tempPol
            articlePolarityList.append(tempPol)
        except ArticleException:
            print("not a valid newspaper article. ignoring it")
    avgArticlePolarity = totalArticlePolarity/len(ne['articleLinksList'])
    wordData['articlePolarityList'] = articlePolarityList
    
    #Adding to the collection
    polarityCollection.insert_one(wordData)
    #Printing Stats
    print("Word  :  " + ne['word'])
    print("Tweet polarity     : " + str(avgTweetPolarity))
    print("Article polarity   : " + str(avgArticlePolarity)) 
