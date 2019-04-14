import os
import json
import arrow

import tweepy
from tweepy import OAuthHandler

from tweets import tweets_folder_name
from tweet_parser import parseTweetBasic

# curtis1227 keys
consumer_key = '60MxomUk4bQx0nkbZFLPTzIFb'
consumer_secret = 'lBI2OB8MwEDi7s2tfUQhXabce5OghaIIwcbuQCc96n1D2DyCIV'
access_token = '206919333-Vi6LOg1NcWgEJKaYnbzb54XzwCeKir4tSZfjnlka'
access_secret = 'McFpqARFMKYQZY9g85BRiQKUP72722PIciiMIwedK0HXZ'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def retrieveTweets(query='movie', limit=250):
    """
    Retrieve tweets from Twitter.
    """
    tweets = []
    # Maybe use random words for query?

    for tweet in tweepy.Cursor(api.search, q=query, result_type='recent').items(limit):
        processed_tweet = parseTweetBasic(tweet._json)
        tweets.append(processed_tweet)

    local = arrow.now('US/Eastern')
    local = local.format('YYYY-MM-DD-HH-mm')

    with open(os.path.join(tweets_folder_name, 'tweets{}_{}_{}.json'.format(local, query, limit)), 'w') as file:
        json.dump(tweets, file, indent=2)

    return tweets

retrieveTweets()
