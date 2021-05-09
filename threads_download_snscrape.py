import os
import time

# import pymongo
# #
# DB_CONN_STRING = "mongodb://localhost:27017/"
# DB_NAME = "recent-poland-covid-vaccine-tweets"
# COLLECTION_NAME = "tweets"
#
# mongo_client = pymongo.MongoClient(DB_CONN_STRING)
# database_name = mongo_client[DB_NAME]
# data_collection = database_name[COLLECTION_NAME]
#
# def tw_check(tw):
#     if tw["_id"] == tw["conversationId"] and tw["replyCount"] > 0:
#         return True
#
#
#
# #projection = {"date":1, "content":1, "user.username":1, "user.id":1, "user.followersCount":1, "user.verified":1}
# conversation_ids = list(filter(lambda tw: tw_check(tw), [tweet for tweet in data_collection.find({},{"replyCount":1, "conversationId":1})]))
# conversation_ids = list(set(map(lambda tw: tw["conversationId"], conversation_ids)))
#
# file = open("conversation_ids.txt", "w")
# for conversationId in conversation_ids:
#     file.write("\"" + str(conversationId) + "\",\n")
# file.close()

# conversation ids need to be putted here
conversation_ids = [ ]

_total_count = len(conversation_ids)
_current_count = 0
_current_progress = 0
_begin_time = time.time()

since_date = "2021-02-01"
data_dir = "data_from_scrap/threads"

try:
    os.makedirs(data_dir)
except FileExistsError:
    # directory already exists
    pass

for conversation_id in conversation_ids:
    print(f"Getting tweets from thread: {conversation_id} since date: {since_date}")

    data_file = f"{data_dir}/{conversation_id}.json"
    os.system(
        f'snscrape --jsonl --progress --since {since_date} twitter-search "conversation_id:{conversation_id} lang:pl"> {data_file}')
    
    _current_count += 1
    _current_progress = (100*_current_count)/_total_count
    print("Progress: {}".format(_current_progress) + "  Estimated time: {}".format((time.time()-_begin_time)*(100-_current_progress)/_current_progress/3600))