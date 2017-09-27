''' This module obtains the movie list from an api
creates an instance of movie class from media.py and
opens up the movie and trailer in an html using fresh_tomatoes.py'''

import json
import urllib2
import fresh_tomatoes
import media


# images and trailer videos need base url to be appended to the values we get fromt he api
BASE_TRAILER_URL = "https://www.youtube.com/watch?v="

BASE_POSTER_PATH = "http://image.tmdb.org/t/p/w185/"
# there are two apis for getting information we need for movies.
#First one contains list of movies
#The second contains the details for a particular movie
# movie_identifer is used to store the movie id so it can
# be used in the api that provides the  movie detail
movie_identifiers = []

# movies object contain all the instances of Movie class.
movies = []

# Get the list of movies from the movie api data
movie_data = urllib2.urlopen("https://api.themoviedb.org/3/discover/movie?" \
    "api_key=8b09908c76103179a325e29ed2f5e153&language=en-US&" \
    "sort_by=popularity.desc&include_adult=false&primary_release_year=2016" \
    "&include_video=true&page=1")

# Read the json data returned from the api
data = movie_data.read()

json_data = json.loads(data)

# Store the top 10 movies ( I am using the api get the popular movies in 2016)
for i in range(0, 10):

    # Read the ids of th emovie from the api response
    movie_ids = json_data['results'][i]['id']

    # Store ids of top 10 movies by popularity as an array
    movie_identifiers.append(movie_ids)

# Loop through the movie ids obtained from the previous step
for movie_id in movie_identifiers:
	# This is the api link used
    movie_url = "https://api.themoviedb.org/3/movie/{0}?" \
    "api_key=8b09908c76103179a325e29ed2f5e153&append_to_response=videos".format(movie_id)

    # Open the movie detail url and read the json response
    movie_detail_data = urllib2.urlopen(movie_url)

    detail_data = movie_detail_data.read()

    movie_detail = json.loads(detail_data)
    # movie title and overview from the api response
    title = movie_detail['title']

    overview = movie_detail['overview'],
    # add the poster and video keys to the base url to obtain the complete url
    trailer_url = BASE_TRAILER_URL+movie_detail['videos']['results'][0]['key']

    poster_url = BASE_POSTER_PATH+movie_detail['poster_path']

    #creating a movie class instance
    movie = media.Movie(title, overview, poster_url, trailer_url)

    movies.append(movie)
# Opening the movie web page
fresh_tomatoes.open_movies_page(movies)
