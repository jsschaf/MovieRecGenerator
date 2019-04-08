import json, re, string
import arrow

from nltk.tokenize import TweetTokenizer, MWETokenizer
tweettk = TweetTokenizer()
mwetk = MWETokenizer()

import nltk.corpus as corpus
stop_words = set(corpus.stopwords.words('english'))

import tweepy
from tweepy import OAuthHandler

from tweet_parser import parseTweetBasic, parseUserBasic

# curtis1227 keys
consumer_key = '60MxomUk4bQx0nkbZFLPTzIFb'
consumer_secret = 'lBI2OB8MwEDi7s2tfUQhXabce5OghaIIwcbuQCc96n1D2DyCIV'
access_token = '206919333-Vi6LOg1NcWgEJKaYnbzb54XzwCeKir4tSZfjnlka'
access_secret = 'McFpqARFMKYQZY9g85BRiQKUP72722PIciiMIwedK0HXZ'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

def retrieveTweets():
    tweets = []
    query = 'movie'
    limit = 150
    # Maybe use random words for query?

    local = arrow.now('US/Eastern')
    local = local.format('YYYY-MM-DD-HH-mm')
    with open('tweets{}.json'.format(local), 'w') as file:
        file.write('[')
        for i, tweet in enumerate(tweepy.Cursor(api.search, q=query, result_type='recent').items(limit)):
                processed_tweet = parseTweetBasic(tweet._json)
                tweets.append(processed_tweet)
                json.dump(processed_tweet, file, sort_keys=True, indent=2)
                file.write(',\n')
        file.write('{}]\n')
    return tweets

# tweets = retrieveTweets()
tweets = {}
with open('tweets.json', 'r') as file:
    tweets = json.load(file)

with open('test.txt', 'w') as file:
    for tweet in tweets:
        text = tweettk.tokenize(tweet['text'])
        # Remove stopwords
        # text = [token for token in text if token not in stop_words]
        file.write(str(text) + '\n')
        # print(json.dumps(tweet, indent=2))
