from pymongo import MongoClient
from newsapi import NewsApiClient
from textblob import TextBlob

## Fire up newsAPI
newsApi = NewsApiClient(api_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXx')

## Get the top 5 Named Entities
namedEntityCol = MongoClient().precogTask.namedEntityCollection
col = namedEntityCol.find()
count = 0
# wordList used to store documents sirectly from namedEntityCollection
wordList = []
for k in sorted(col, key=lambda k: len(k['tweet']), reverse=True):
    count += 1
    if count > 5:
        break
    wordList.append(k)

dataForEntityAnalysis = MongoClient().precogTask.dataForAnalysis
dataForEntityAnalysis.drop()

for ne in wordList:
    word = ne['word']
    tweets = ne['tweet']
    articleLinks = []
   
    allNews = newsApi.get_everything(q=word,language='en',sort_by='relevancy',)
    articles = allNews['articles']
    print("----------------------------------------------")
    print(word)
    for article in articles:
        print(article['url'])
        articleLinks.append(article['url'])
    print("----------------------------------------------")

    document = {}
    document['word'] = word
    document['tweetList'] = tweets
    document['articleLinksList'] = articleLinks
    dataForEntityAnalysis.insert_one(document)

