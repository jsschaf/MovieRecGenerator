"""
EECS 486: Final Project

Python implementation that requests movies from the Movie DB and stores movie data in movies.json

NOTE: This program runs with Python 3.7
NOTE: This program requires python library "requests"
NOTE: API Key (v3 auth): 68ecb8ff29c2d7356eb0b66d31136fd9
"""
import requests
import time
import os, sys
import json

# list of movie data json
# json format: {"id": id, "name": name, "genre_list": [genres], "keyword_list": [keywords]}
movie_json_list = [] 

# prevent duplicated movies
movie_set = set() 

# dictionary that maps from genre ID to genre string 
genre_dict = {27: "Horror", 28: "Action", 35: "Comedy", 99: "Documentary", 10749: "Romance"}

# URL to get JSON from the movie DB 
URL = "https://api.themoviedb.org/3/discover/movie"
# API KEY - credentials
API_KEY = "68ecb8ff29c2d7356eb0b66d31136fd9"
# array of genres that we are not interested in looking at 
WITHOUT_GENRES = "12,16,80,18,10751,14,36,10402,9648,878,10770,10752,37,53"

# function that get keywords given the movie id
# returns an array of unprocessed list of keywords retrieved 
def get_keywords(movie_id):
	global API_KEY
	KEYWORD_URL = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/keywords"
	KEYWORD_PARAM = {"api_key" : API_KEY}
	keyword_data = request_and_retrieve(KEYWORD_URL, KEYWORD_PARAM)

	keyword_results = keyword_data['keywords']
	keywords_list = []
	keywords_set = set()

	for res in keyword_results:
		keywords_string = res["name"]
		keywords_string_split = keywords_string.split()
		for keyword in keywords_string_split:
			if keyword in keywords_set:
				continue
			keywords_set.add(keyword)
			keywords_list.append(keyword)

	return keywords_list

# function that requests JSON and returns 
def request_and_retrieve(request_url, request_param):
	request = requests.get(url = request_url, params = request_param)
	data = request.json()
	# sleep if we exceed # requests per second
	if 'status_code' in data:
		time.sleep(9) # reset counter
		request = requests.get(url = request_url, params = request_param)
		data = request.json()

	return data

# function that adds movie data to list of json  
def add_movie_data(json_data):
	# go through the movies
	global genre_dict
	global movie_set
	global movie_json_list

	for result in results:
		movie_id = result['id']

		if movie_id not in movie_set:
			movie_set.add(movie_id)

			# get genres 
			genre_list = []
			for genre_id in result['genre_ids']:
				genre_list.append(genre_dict[genre_id])
			
			# get keywords 
			keywords_list = get_keywords(movie_id)
			if(len(keywords_list) == 0):
				continue
			movie_json_list.append({"id": movie_id, "name": result['original_title'], 
									"genre_list": genre_list, "keyword_list": keywords_list})


if __name__ == '__main__':
	for year in range(2008, 2020):  
		PARAMS = {"api_key" : API_KEY, "vote_average.gte": 5, "primary_release_year": year, "without_genres": WITHOUT_GENRES, "vote_count.gte": 20, "with_original_language": "en"}
		data = request_and_retrieve(URL, PARAMS)
		results = data['results']
		add_movie_data(results)
		# get next json data
		total_pages = data["total_pages"]
		for page in range(2, total_pages):
			PAGE_PARAMS = {"api_key": API_KEY, "page": page,"vote_average.gte": 5, "primary_release_year": year, "without_genres": WITHOUT_GENRES, "vote_count.gte": 20, "with_original_language": "en"}
			data = request_and_retrieve(URL, PAGE_PARAMS)
			results = data['results']
			add_movie_data(results)

	with open(os.getcwd()+'/movies.json', 'w+') as outfile:  
	    json.dump(movie_json_list, outfile)


