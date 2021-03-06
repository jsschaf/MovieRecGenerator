"""
EECS 486: Final Project

Python implementation that takes preprocessed Twitter data and preprocessed
movie keyword data as input, then uses a TF-IDF-based information retrieval
system to identify top movies that a given user will find interesting
depending on the person's expressed likes and dislikes.

NOTE: This program runs with Python 3.7.
"""


import collections
import json
import operator
import os

from math import log10, sqrt
from porterstemmer import *
from textblob import TextBlob
# To use the TextBlob library on CAEN, we will need to run the following 
# command:
# `pip install --user textblob`.


def stemWords(tokensList):
	"""
	Stem the words found in the tokensList input.
	Return: list of (stemmed) tokens
	"""

	# Use the Porter Stemmer implementation from porterstemmer.py based off of
	# the implementation found here: 
	# http://tartarus.org/~martin/PorterStemmer/python.txt
	stemmer = PorterStemmer()

	# Iterate through individual tokens and stem each one according to the
	# already implemented Porter Stemmer class.
	for idx in range(0, len(tokensList)):
		tokensList[idx] = stemmer.stem(tokensList[idx], 0, len(tokensList[idx]) - 1)
	return tokensList


def indexMovies(movie, invertedIndex): 
	"""
	Adds movie tokens to inverted index passed in as input (invertedIndex).
	Return: Additional entry in inverted index data structure (passed in as
			input).
	"""

	finalMovieTokens = []

	# Get ID for movie.
	movieID = movie['id']

	# Find term frequency of each token in movie tokens list. The tokens list
	# contains both the genre and keyword lists.
	for genre in movie['genre_list']:
		if genre != "movie":
			genre = genre.lower()
			finalMovieTokens.append(genre)
	for keyword in movie['keyword_list']:
		if (keyword != "movie") and (keyword != "with"):
			keyword = keyword.lower()
			finalMovieTokens.append(keyword)

	# Also include name of movie in list of tokens.
	finalMovieTokens.append(movie['name'])
	finalMovieTokens = stemWords(finalMovieTokens)
	termFreq = collections.Counter(finalMovieTokens)
	termFreq = dict(termFreq)

	# Add all tokens and term frequencies to invertedIndex, updating the inverted
	# index.
	for token in termFreq:

		# If the token already exists in the inverted index, then add to the
		# index. Otherwise, create a new entry in the dictionary.
		if token in invertedIndex:
			invertedIndex[token][1][movieID] = termFreq[token]
			invertedIndex[token][0] += 1
		else:

			# The structure of the inverted index is as follows:
			# Dictionary({term_1: [df, {docID_1: tf_1, docID_2: tf_2, ...}],
			# 			  term_2: [df, {docID_1: tf_1, docID_2: tf_2, ...}],
			# 			  ...})
			#
			# The term refrequency will be 1 for each document because we assume
			# that we will only see one occurence of a keyword per document.
			invertedIndex[token] = []
			invertedIndex[token].append(1) # document frequency
			invertedIndex[token].append({}) # empty dictionary for the actual	
											# inverted index
			invertedIndex[token][1][movieID] = termFreq[token]

			# For keeping track of the number of documents in the collection.
			invertedIndex[token].append(0)

	# Determine number of documents in the collection.
	docCount = {}
	for term in invertedIndex:
		for doc in invertedIndex[term][1]:
				docCount[doc] = True
		maxDocs = len(docCount)
	for term in invertedIndex:
		invertedIndex[term][2] = maxDocs


def retrieveMovies(tweet, invertedIndex):
	"""
	Retrieves information from the index for a given tweet as a query.
	Return: IDs for relevant movies and similarity scores (dictionary)
	"""

	# Find set of movies from inverted index that have at least one token
	# from the tweet query.
	# The retrieved variable will be formatted as:
	# Dictionary({docID: {token: tf-idf, token: tf-idf, ...}},
	# 			  docID: {token, tf-idf, token: tf-idf, ...}},
	# 			  ...)
	# tf-idf (the value of each token) is the weight given the weighting 
	# scheme passed in.
	tweet = stemWords(tweet)
	termFreq = collections.Counter(tweet)
	termFreq = dict(termFreq)
	retrieved = {}
	for token in termFreq:
		if token in invertedIndex:

			# Iterate through docs in inverted index and add docs to retrieved
			# dictionary if not already there.
			for doc in invertedIndex[token][1]:
				if doc not in retrieved:
					retrieved[doc] = {}

				# Add weight as value to corresponding token.
				retrieved[doc][token] = float(invertedIndex[token][1][doc])

	# Calculate tf-idf scores for each movie in retrieved.
	for doc in retrieved:
		for token in retrieved[doc]:
			idf = log10(float(invertedIndex[token][2]) / \
				float(invertedIndex[token][0]))
			retrieved[doc][token] = float(retrieved[doc][token]) * idf

	# Calculate the tf-idf scores for each term in the query, if found in
	# the inverted index.
	queryWeight = {}
	for token in termFreq:
		if token in invertedIndex:
			queryTF = termFreq[token]
			queryIDF = log10(float(invertedIndex[token][2]) / \
				float(invertedIndex[token][0]))
			queryWeight[token] = float(queryTF) * queryIDF

	# Calculate length of query vector for similarity normalization.
	denominatorQuery = 0
	for term in queryWeight:
		denominatorQuery += (queryWeight[term] * queryWeight[term])
	denominatorQuery = sqrt(denominatorQuery)

	# Iterate through all retrieved docs. Calculate cosine similarity scores
	# for each doc and the input query.
	for doc in retrieved:
		numerator = 0.0
		denominatorDoc = 0.0
		for token in retrieved[doc]:
			numerator += (retrieved[doc][token] * queryWeight[token])
			denominatorDoc += (retrieved[doc][token] * retrieved[doc][token])
		denominatorDoc = sqrt(denominatorDoc)
		retrieved[doc] = numerator / (denominatorDoc * denominatorQuery)
	return retrieved


if __name__ == '__main__':

	# Open JSON file containing a list of tweets.
	#
	# listOfTweets is a dictionary-based format of the tweets that we will be
	# using to suggest movies for.
	tweetsFile = open(os.getcwd() + "/tokenized_tweets/ALL_tweets.json", 'r')
	tweetsContents = tweetsFile.read()
	listOfTweets = json.loads(tweetsContents)

	# Open JSON file containing a list of movies and their corresponding
	# keywords.
	moviesFile = open(os.getcwd() + "/movies.json", 'r')
	moviesContents = moviesFile.read()
	listOfMovies = json.loads(moviesContents)

	# Put movie information into inverted index.
	invertedIndex = {}
	for movie in listOfMovies:
		indexMovies(movie, invertedIndex)

	# Because some Twitter users may express negative opinions about certain
	# movies/topics, it would not be reasonable to make movie suggestions
	# based on these types of opinions. This is because we do not know 
	# what the user will like in terms of movies, only the types of movies
	# that he or she does not like. Furthermore, suggesting an "opposite" to
	# a given movie topic is not really realistic because there is no real
	# definitive opposite to, say, action/adventure movies.
	#
	# We use sentiment analysis to filter out the negative tweets and only 
	# use positive and neutral tweets for training and testing.
	collected_results = {}
	for key, value in listOfTweets.items():

		# TextBlob only recognises sentiment analysis on sentences. We will have
		# to compose the sentence together first, assuming that the tokens 
		# found in the text are in the original order.
		sentence = ""
		for word in value["text"]:
			sentence += word
			sentence += " "
		results = TextBlob(sentence) 
		if (results.sentiment[0] > 0) or (not (results.sentiment[0] < 0)):
			collected_results[value["original_text"]] = []
			listOfDocs = retrieveMovies(value["text"], invertedIndex)
			sorted_listOfDocs = sorted(listOfDocs.items(), \
				key=operator.itemgetter(1), reverse=True)
			if len(sorted_listOfDocs) > 5:
				for i in range(5):
					collected_results[value["original_text"]].append(sorted_listOfDocs[i])
			else:
				for i in sorted_listOfDocs:
					collected_results[value["original_text"]].append(i)
	print(collected_results)


































































































