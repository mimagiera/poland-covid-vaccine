import ast
import json
from os import walk

import pymongo

DB_CONN_STRING = "mongodb://localhost:27017/"

DB_NAME = "poland-covid-vaccine-tweets"
COLLECTION_NAME = "tweets"

debug = True


def import_old_data():
    mongo_client = pymongo.MongoClient(DB_CONN_STRING)
    database_name = mongo_client[DB_NAME]
    old_data_col = database_name[COLLECTION_NAME]
    dir_name = "data/20210319_2100"
    _, _, filenames = next(walk("%s" % dir_name))

    for file_name_inside in filenames:
        file_name = f"{dir_name}/{file_name_inside}"
        with open(file_name) as file_to_import:
            tweets_from_file = []
            for jsonObj in file_to_import:
                tweet_json = json.loads(jsonObj)
                # '_id' is used as document id in mongo
                # Without this conversion each document would have new ObjectId as id
                tweet_json["_id"] = tweet_json.pop("id")
                tweets_from_file.append(tweet_json)
            try:
                insert_result = old_data_col.insert_many(tweets_from_file)
                if debug:
                    print(f"Inserted ids from file {file_name}: {insert_result.inserted_ids}")
            except Exception as e:
                print(f"Error inserting data from file {file_name}: {e}")

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
