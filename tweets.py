import json
import tweepy
from tweepy import OAuthHandler

# curtis1227 keys
consumer_key = '60MxomUk4bQx0nkbZFLPTzIFb'
consumer_secret = 'lBI2OB8MwEDi7s2tfUQhXabce5OghaIIwcbuQCc96n1D2DyCIV'
access_token = '206919333-Vi6LOg1NcWgEJKaYnbzb54XzwCeKir4tSZfjnlka'
access_secret = 'McFpqARFMKYQZY9g85BRiQKUP72722PIciiMIwedK0HXZ'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

def parseUser(u):
    new_u = { key: u[key] for key in [
        'created_at',
        'description',
        'entities',
        'favourites_count',
        'followers_count',
        'friends_count',
        'id',
        'id_str',
        'lang',
        'listed_count',
        'location',
        'name',
        'screen_name',
        'statuses_count',
        'url'
        ]
    }
    return new_u

def parseTweet(s):
    new_s = { key: s[key] for key in [
        'created_at',
        'entities',
        'favorite_count',
        'id',
        'id_str',
        'lang',
        'metadata',
        'text',
        'source'
        ]
    }
    new_s['user'] = parseUser(s['user'])
    return new_s

def retrieveTweets():
    tweets = []
    query = '#movie'
    limit = 100
    # Maybe use random words for query?
    with open('tweets.json', 'w') as file:
        for i, tweet in enumerate(tweepy.Cursor(api.search, q=query, result_type='recent').items(limit)):
                processed_tweet = parseTweet(tweet._json)
                print(i, processed_tweet)
                tweets.append(processed_tweet)
                json.dump(processed_tweet, file, sort_keys=True, indent=2)
                file.write(',\n')
    return tweets

# tweets = retrieveTweets()
tweets = {}
with open('tweets.json', 'r') as file:
    tweets = json.load(file)

for tweet in tweets:
    print(tweet['text'])
