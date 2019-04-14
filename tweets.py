tweets_folder_name = 'tweets/'
tokenized_tweets_folder_name = 'tokenized_tweets/'

import os
import string
import json

from nltk.tokenize import TweetTokenizer, MWETokenizer
import nltk.corpus as corpus

# Twitter Tokenizer
tweettk = TweetTokenizer()
# Multi-Word Tokenizer
mwetk = MWETokenizer()
# Load movie titles into Multi-Word Tokenizer
movie_titles = []
with open('movies.json', 'r') as file:
    movie_titles = [movie['name'].split() for movie in json.load(file)]
for title in movie_titles:
    # Movies that are one word don't need to be included
    if len(title) < 2:
        continue
    mwetk.add_mwe(tuple(title))
    # Include lowercased version as well
    mwetk.add_mwe(tuple([s.lower() for s in title]))

stop_words = set(corpus.stopwords.words('english'))
printable = set(string.printable)


def tokenizeTweets(tweets):
    for tweet in tweets:
        # Remove any non-ASCII chars
        text = ''.join([x for x in tweet['text'] if x in printable])
        text = tweettk.tokenize(text)
        text = mwetk.tokenize(text)
        text = [token for token in text if token not in stop_words]
        tweet['text'] = text
    return tweets


def main():
    # ALL_tweets is not a list of tweets like others.
    # Rather, it is a dictionary of tweets with tweet['id_str'] as keys.
    ALL_tweets = {}

    list_of_filenames = os.listdir(tweets_folder_name)
    # For each retrieved file of tweets, tokenize and write to new file
    for filename in list_of_filenames:
        tweets = []
        with open(os.path.join(tweets_folder_name, filename), 'r') as file:
            tweets = json.load(file)

        tweets = tokenizeTweets(tweets)

        with open(os.path.join(tokenized_tweets_folder_name, filename), 'w') as file:
            json.dump(tweets, file, indent=2)

        for tweet in tweets:
            # Find duplicates in previous retrievals
            if tweet['id_str'] in ALL_tweets:
                print('duplicate', tweet['id_str'])
            ALL_tweets[tweet['id_str']] = tweet

    with open(os.path.join(tokenized_tweets_folder_name, 'ALL_tweets.json'), 'w') as file:
        json.dump(ALL_tweets, file, indent=2)

if __name__ == '__main__':
    main()
