import os
import time

import pymongo
from consts import *

mongo_client = pymongo.MongoClient(DB_CONN_STRING)
database_name = mongo_client[DB_NAME]
data_collection = database_name[COLLECTION_NAME_TWEETS]


def tw_check(tw):
    if tw["_id"] == tw["conversationId"]:
        return True


tweets = [tweet for tweet in data_collection.find({'conversation_downloaded' : False}, {"replyCount": 1, "conversationId": 1})]
root_tweets_count = {tw["conversationId"]: tw for tw in list(filter(lambda tw: tw_check(tw), tweets))}
conversations_roots_count = {tw["conversationId"]: 0 for tw in list(filter(lambda tw: tw_check(tw), tweets))}
for tweet in tweets:
    if not tw_check(tweet) and tweet["conversationId"] in root_tweets_count.keys():
        conversations_roots_count[tweet["conversationId"]] = conversations_roots_count[tweet["conversationId"]] + 1

conversation_ids = []
for key, val in conversations_roots_count.items():
    print("{} === {}".format(root_tweets_count[key]["replyCount"], val))
    if root_tweets_count[key]["replyCount"] != val and root_tweets_count[key]["replyCount"] != 0:
        conversation_ids.append(key)



file = open("conversation_ids.txt", "w")
for conversationId in conversation_ids:
    file.write("\"" + str(conversationId) + "\",\n")
file.close()