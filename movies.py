# python for movies

# The Movie DB 
# API Key (v3 auth): 68ecb8ff29c2d7356eb0b66d31136fd9
# API Read Access Token ()

# MUST have requests installed. (pip3 install requests)

import requests
import time
import os, sys # debugging
import json

time_start = time.time()
# list of json
# {"id": id, "name": name, "genre_list": [genres], "keyword_list": [keywords]}
movie_json_list = [] 

movie_set = set() # prevent duplicated movies

genre_dict = {27: "Horror", 28: "Action", 35: "Comedy", 99: "Documentary", 10749: "Romance"}

URL = "https://api.themoviedb.org/3/discover/movie"
API_KEY = "68ecb8ff29c2d7356eb0b66d31136fd9"
WITHOUT_GENRES = "12,16,80,18,10751,14,36,10402,9648,878,10770,10752,37,53"

it = 0
# get keywords
def get_keywords(movie_id):
	global API_KEY, it
	it += 1
	print(str(it) + " " + str(movie_id))
	KEYWORD_URL = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/keywords"
	KEYWORD_PARAM = {"api_key" : API_KEY}
	keyword_data = request_and_process(KEYWORD_URL, KEYWORD_PARAM)

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

def request_and_process(request_url, request_param):
	global f

	request = requests.get(url = request_url, params = request_param)
	data = request.json()
	if 'status_code' in data:
		print(data)
		time.sleep(9) # reset counter
		request = requests.get(url = request_url, params = request_param)
		data = request.json()

	return data


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


for year in range(2008, 2019): #TODO: change years 
	PARAMS = {"api_key" : API_KEY, "vote_average.gte": 6, "year": year, "without_genres": WITHOUT_GENRES, "vote_count.gte": 100}
	data = request_and_process(URL, PARAMS)
	results = data['results']
	add_movie_data(results)
	# get next json data
	total_pages = data["total_pages"]
	for page in range(2, total_pages):
		PAGE_PARAMS = {"api_key": API_KEY, "page": page,"vote_average.gte": 6, "year": year, "without_genres": WITHOUT_GENRES, "vote_count.gte": 100}
		data = request_and_process(URL, PAGE_PARAMS)
		results = data['results']
		add_movie_data(results)

# get keywords 
print('Printing Movies')
print(len(movie_json_list))
print(movie_json_list)

with open(os.getcwd()+'/movies.json', 'w+') as outfile:  
    json.dump(movie_json_list, outfile)

time_end = time.time()
print(time_end-time_start)







