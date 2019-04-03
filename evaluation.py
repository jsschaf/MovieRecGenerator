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
			# If the weighting scheme is set to "probabilistic," there will be
			# another dictionary element in each of the term's list that contains
			# the maximum term frequency for a specific document.
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


































































































