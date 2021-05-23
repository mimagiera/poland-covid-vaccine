import ast
import glob
import json
from os import walk

import pymongo
from pymongo import bulk
from pymongo.errors import DuplicateKeyError

from consts import *

is_conversation_downloaded = True
is_covid_topic = False

def import_old_data():
    mongo_client = pymongo.MongoClient(DB_CONN_STRING)
    database_name = mongo_client[DB_NAME]
    old_data_col = database_name[COLLECTION_NAME_TWEETS]
    bulk_builder = pymongo.bulk.BulkOperationBuilder(old_data_col, ordered=False)
    for filename in glob.iglob("data_from_scrap" + '**/**', recursive=True):
        print(filename)
        if filename.endswith(".json"):
            with open(filename) as file_to_import:
                for jsonObj in file_to_import:
                    tweet_json = json.loads(jsonObj)
                    # '_id' is used as document id in mongo
                    # Without this conversion each document would have new ObjectId as id
                    tweet_json["_id"] = tweet_json.pop("id")
                    tweet_json["covid_topic"] = is_covid_topic
                    tweet_json["conversation_downloaded"] = is_conversation_downloaded
                    try:
                        old_data_col.insert_one(tweet_json)
                    except DuplicateKeyError as e:
                        pass

    print("Finished inserting")
    mongo_client.close()


import_old_data()


# dont look below, was used to convert data to json format. Not needed anymore
def convert_files_to_proper_json():
    dir_name = "data/20210319_2100"
    proper_dir_name = "properdata/20210319_2100"
    _, _, filenames = next(walk(dir_name))
    print(filenames)

    for file_name_inside in filenames:
        file_name = f"{dir_name}/{file_name_inside}"
        proper_file_name = f"{proper_dir_name}/{file_name_inside}"
        with open(file_name, encoding="utf-8") as file_to_convert_data_from:
            with open(proper_file_name, "a", encoding="utf-8") as file_with_proper_json:
                for tweet_dict_string in file_to_convert_data_from:
                    tweet_dict = ast.literal_eval(tweet_dict_string)
                    tweet_json = json.dumps(tweet_dict)
                    file_with_proper_json.write(tweet_json + "\n")

# convert_files_to_proper_json()
