# Final Project for EECS486 - Tweet-based Movie Recommendations
**Authors: Wendy Du, Michelle Gu, Sukang Kim, Curtis Li, Jacqueline Schafer**

## Usage

### Collecting Twitter Data

Setting up a virtual environment: (You'll need to install virtualenv)
```
python3 -m virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

Retrieving Tweets:
```
python retrieve_tweets.py
```
Retrieves tweets using Twitter API and stores the tweets in a folder named tweets/ in the following filename format:

tweets[date and time]\_[query used]\_[tweet limit].json

Processing Tweets:
```
python tweets.py
```
Processes and tokenizes tweets retrieved in the tweets/ folder and stores the resulting tokens in a folder named tokenized_tweets/ in the same filename format.

In addition, a compilation of all the tokens is generated and stored in a file in the same folder called ALL_tweets.json.

### Collecting Movie Data

Collecting Movie Data:
```
python3 movies.py
```
Ensure that the environment is using Python 3.7, otherwise 'requests' python library will not be included
Retrieves list of movies and their id, title, genres, keyword lists and stores those information into movies.json
JSON format: [{"id": movie id, "name": movie title, "genre_list": list of genres, "keyword_list": list of keywords}]

### Suggesting Movies to Tweets

Running the Python evaluation script:
```
python evaluation.py
```
Ensure that the environment is using Python 3.7, otherwise some libraries will not be included (i.e. textblob).

The printed result is a dictionary of the original tweets to their corresponding suggested movie IDs and its TF-IDF-based cosine similarity scores.

To learn what the actual movie is, you will need to find the corresponding movie with that ID in movies.json.

## File Explanations

1. retrieve_tweets.py --> Retrieve tweets using Twitter API
2. tweet_parser.py --> Helper module that filters out irrelevant data from tweets
3. tweets.py --> Preprocesses tweets to generate a list of tokens
4. movies.py --> Gets movies from themoviedb (ID, name, genre, keyword, rating) to generate a list of keywords (filters out low ratings, at least 5/10, with at least 100 votes)
5. evaluation.py
   - docs = list of tokens from movies (one for each movie)
   - query = tokens from tweets
   - Performs tf-idf weighting and uses cosine similarity to match it up.
   - Also performs sentiment analysis to filter out negative sentiment.
   - Generates top 5 movies from greatest to least similarity based on a tweet.
