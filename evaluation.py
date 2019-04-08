"""
EECS 486: Final Project

Python implementation that takes preprocessed Twitter data and preprocessed
movie keyword data as input, then uses a TF-IDF-based information retrieval
system to identify top movies that a given user will find interesting
depending on the person's expressed likes and dislikes.

NOTE: This program runs with Python 3.7.
"""


import collections
import movies # Python library containing movie keyword identification 
			  # and preprocessing.

import tweets # Python library containing preprocessed Twitter data.

from math import log10, sqrt


def indexMovies(movie, invertedIndex): 
	"""
	Adds movie tokens to inverted index passed in as input (invertedIndex).
	Return: Additional entry in inverted index data structure (passed in as
			input).
	"""

	# TODO: ADD MOVIEID INFO HERE 
	# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	# Find term frequency of each token in movie tokens list.
	termFreq = collections.Counter(movie)
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


































































































