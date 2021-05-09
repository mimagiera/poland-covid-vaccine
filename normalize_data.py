import pymongo
from pymongo import bulk

from consts import *

mongo_client = pymongo.MongoClient(DB_CONN_STRING)
database_name = mongo_client[DB_NAME]

tweets_collection = database_name[COLLECTION_NAME_TWEETS]
users_collection = database_name[COLLECTION_NAME_USERS]

keys_to_remove_from_tweet = ['renderedContent', 'outlinks', 'tcooutlinks', 'source', 'sourceurl', 'sourcelabel',
                             'media',
                             'coordinates', 'place']

keys_to_remove_from_user = ['rawDescription', 'descriptionUrls', 'linkUrl', 'linkTcourl', 'profileImageUrl',
                            'profileBannerUrl']

bulk_builder = pymongo.bulk.BulkOperationBuilder(users_collection, ordered=False)


def remove_keys_from_tweet(tweet_to_remove_keys):
    for key_to_remove in keys_to_remove_from_tweet:
        tweet_to_remove_keys.pop(key_to_remove, None)
    return tweet_to_remove_keys


def fix_nested_tweets(tweet_to_fix, key_name):
    quoted = tweet_to_fix[key_name]
    if quoted is not None and type(quoted) is dict:
        quoted['_id'] = quoted.pop('id')
        tweet_to_fix[key_name] = quoted['_id']
        tweet_that_was_quoted = do_all_for_tweet(quoted)
        tweet_that_was_quoted['was_' + key_name] = True
        res = tweets_collection.find_one({'_id': quoted['_id']})
        if res is None:
            tweets_collection.insert_one(tweet_that_was_quoted)

    return tweet_to_fix


def fix_user(tweet_with_user):
    user = tweet_with_user['user']
    if type(user) is dict:
        user['_id'] = user.pop('id')
        tweet_with_user['user'] = user['_id']
        for key_to_remove in keys_to_remove_from_user:
            user.pop(key_to_remove, None)
        bulk_builder.insert(user)
    return tweet_with_user


def fix_nested_users(tweet_with_mentioned_users):
    users = tweet_with_mentioned_users['mentionedUsers']
    if users is not None:
        user_ids = []
        for user_to_change in users:
            if type(user_to_change) is dict:
                user_to_change['_id'] = user_to_change.pop('id')
                for key_to_remove in keys_to_remove_from_user:
                    user_to_change.pop(key_to_remove, None)
                bulk_builder.insert(user_to_change)
                user_ids.append(user_to_change['_id'])
        if len(user_ids) > 0:
            tweet_with_mentioned_users['mentionedUsers'] = user_ids
    return tweet_with_mentioned_users


def do_all_for_tweet(tweet_to_do_all):
    # remove redundant user
    tweet_to_do_all = fix_user(tweet_to_do_all)
    # remove keys
    tweet_to_do_all = remove_keys_from_tweet(tweet_to_do_all)
    # fix nested mentioned users
    tweet_to_do_all = fix_nested_users(tweet_to_do_all)
    # fix nested tweets
    tweet_to_do_all = fix_nested_tweets(tweet_to_do_all, 'quotedTweet')
    tweet_to_do_all = fix_nested_tweets(tweet_to_do_all, 'retweetedTweet')
    return tweet_to_do_all


for tweet in tweets_collection.find():
    tweet = do_all_for_tweet(tweet)
    tweets_collection.replace_one({"_id": tweet["_id"]}, tweet)

bulk_builder.execute()

print("Finished")
mongo_client.close()
