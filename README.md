## Dependencies
[] Python 3
[] Tweepy library : for tweet mining
[] NLTK library : For Extracting names entities
    nltk.download() 'words'
    numpy
[] 

## Task 1 : Mining Tweets
Tweets were mined using the tweepy library for python. Tweets are stored in `precogTask` db in the `tweetCollection` collection. 
Script : 1-tweetMining.py
The Script collects only English tweets. The nicest part is that it will not stop unless it has collected the required number of tweets. The output on the terminal is the tweet being worked on. I was surprised to see more non-english tweets than english tweets

## Task 2 : Mining most frequent named enties
I used the NLTK library to find the named entities. A new collection of named entities and the tweets that they appear is made(precogTask.namedEntitiesCollection)

It will also print the 5 most freqently named entities

Script: 2-namedEntities.py

## Task 3 : Getting news for the 5 most named entities
`newsapi.org` used to get news relevant to named entities. 
Text from news is not extracted here
It'll be done later(in task 4) using `Newspaper` library
Script : 3-newsExtraction.py

## Task 4 : Sentiment analysis of tweets and named entities and news articles
First, I extract all the text from the news article(link generated in Task 3)
Sentiment analysis done using TextBlob. Newspaper urls that are not proper articles are ignored
word, tweet and article sentiment polarity are stored in collection `neTweetArticleSentiment`

script : 4-sentimentAnalysis.py

## Task 5 : Representation of past data
Representation of previous data: Average sentiment

For the temporal, spatial and content analysis, I cannot use the existing tweet data obtained from Task 1. The reason is that I used a stream sample to generate data, to ensure randomness. A stream gives realtime data, and hence the timespan is too less to generate any useful temporal analysis. 

NOTE : Spatial representation was not done since too few tweets had geodata.
Otherwise, data would've been represented as point on a map, with color highlighting its sentiment. If the tweets had data, it would've shown some good results.

## Task 6 : Deploy this project. 
Project output has been uploaded to kaustubh-welankar.github.io

## Task 7 : Upload code to Github
