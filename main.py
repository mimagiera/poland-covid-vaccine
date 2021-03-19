import tweepy as tw

from twitter_creds import twitter_keys

# Setup access to API
auth = tw.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])

api = tw.API(auth, wait_on_rate_limit=True)

# Define the search term and the date_since date as variables
hash_tag = "CovidVaccine"
query = "#" + hash_tag + " -filter:retweets"

# Collect tweets
tweets = tw.Cursor(api.search,
                   q=query,
                   lang="pl",
                   tweet_mode='extended').items(5000)

for t in tweets:
    with open("search_results_"+hash_tag+".json", "a", encoding="utf-8") as file:
        file.write(str(t._json) + "\n")
