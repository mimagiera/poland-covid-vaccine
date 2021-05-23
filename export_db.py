import os

from consts import *
TWEETS_COLLECTION_FIELDS = "_id,url,date,content,replyCount,retweetCount,likeCount,quoteCount,covid_topic,sentiment"
USERS_COLLECTION_FIELDS = "_id,verified,created,followersCount,friendsCount,statusesCount,favouritesCount,listedCount,mediaCount,location,protected,url"

tweets_export_prefix = f'mongoexport --uri="{DB_CONN_STRING}"  --collection={COLLECTION_NAME_TWEETS} --db={DB_NAME}  --out={COLLECTION_NAME_TWEETS}'
users_export_prefix = f'mongoexport --uri="{DB_CONN_STRING}"  --collection={COLLECTION_NAME_USERS} --db={DB_NAME}  --out={COLLECTION_NAME_USERS}'

os.system(f'{tweets_export_prefix}.json')
os.system(f'{users_export_prefix}.json')


os.system(f'{tweets_export_prefix}.csv --type=csv --fields={TWEETS_COLLECTION_FIELDS}')
os.system(f'{users_export_prefix}.csv --type=csv --fields={USERS_COLLECTION_FIELDS}')
