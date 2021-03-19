import tweepy as tw

from twitter_creds import twitter_keys

# Setup access to API
auth = tw.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])

api = tw.API(auth)

# Define the search term and the date_since date as variables
search_words = "#szczepimysie"
date_since = "2020-03-18"

# Collect tweets
tweets = tw.Cursor(api.search,
                   q=search_words,
                   lang="pl",
                   tweet_mode='extended',
                   since=date_since).items(5)
for t in tweets:
    print(t._json)
    # print(t.text)
