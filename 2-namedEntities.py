from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

from pymongo import MongoClient
import re
import operator

#from stackExchange
def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
            if type(i) == Tree:
                    current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                    named_entity = " ".join(current_chunk)
                    if named_entity not in continuous_chunk:
                            continuous_chunk.append(named_entity)
                            current_chunk = []
            else:
                    continue
    return continuous_chunk


tweetCollection = MongoClient().precogTask.tweetCollection
tweetDict = tweetCollection.find()
wordDict = {}
count = 1
for t in tweetDict :
    tempDict = get_continuous_chunks(t["text"])
    print(count)
    count += 1
    for w in tempDict:
        if w not in wordDict :
                wordDict[w] = []
        #Ensures no double entries by accident
        if t['_id'] not in wordDict[w]:
                wordDict[w].append(t['_id'])


namedEntityCol = MongoClient().precogTask.namedEntityCollection
namedEntityCol.drop()
for i in wordDict:
    tempDict = {}
    tempDict["word"] = i
    tempDict["tweet"] = wordDict[i]
    namedEntityCol.insert_one(tempDict)


# Printing top 5 NEs
col = namedEntityCol.find()
count = 0
print("Most Frequent Named entities")
for k in sorted(col, key=lambda k: len(k['tweet']), reverse=True):
    count += 1
    if count > 5:
        break
    print(k['word'] + " appears in " + str(len(k['tweet'])) + ' tweets')
