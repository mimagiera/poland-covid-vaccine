import pymongo

from consts import *

mongo_client = pymongo.MongoClient(DB_CONN_STRING)
database_name = mongo_client[DB_NAME]

tweets_collection = database_name[COLLECTION_NAME_TWEETS]
users_collection = database_name[COLLECTION_NAME_USERS]

file = open("users-mentions-edges.csv", "w")
for tw in tweets_collection.find({}, {"user": 1, "mentionedUsers": 1}):
    if tw["mentionedUsers"]:
        for user2 in tw["mentionedUsers"]:
            file.write(f'{tw["user"]},{user2}\n')
file.close()