import tweepy
from tweepy import OAuthHandler

# curtis1227 keys
consumer_key = '60MxomUk4bQx0nkbZFLPTzIFb'
consumer_secret = 'lBI2OB8MwEDi7s2tfUQhXabce5OghaIIwcbuQCc96n1D2DyCIV'
access_token = '206919333-Vi6LOg1NcWgEJKaYnbzb54XzwCeKir4tSZfjnlka'
access_secret = 'McFpqARFMKYQZY9g85BRiQKUP72722PIciiMIwedK0HXZ'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

for tweet in api.user_timeline(screen_name="thehill", count=5):
    print(tweet.text)
# print(api.get_user(screen_name="UMich"))
