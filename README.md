# 486final
# Authors: Wendy Du, Michelle Gu, Sukang Kim, Curtis Li, Jacqueline Schafer

1. retrieve_tweets --> retrieve from twitter API
2. parser --> gets text from and ID
3. tweets.py --> preprocessing --> generates a list of tokens
4. movies.py --> gets movies from themoviedb (ID, name, genre, keyword, rating) --> generates a list of keywords (filters out low ratings, at least 5/10, with at least 100 votes)
5. evaluation.py 
    docs = list of tokens from movies. one for each movie. 
    query = tokens from tweets
    performs tf-idf weighting and uses cosine similarity to match it up. 
    also performs sentiment analysis to filter out negative sentiment
    generates top 5 movies from greatest to smallest similarity based on a tweet
