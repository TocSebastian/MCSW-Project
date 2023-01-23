import DataExtraction
from MovieDB import MovieDB

#O1

# Initialize a list with different movies from different websites
movie_links = ["https://www.imdb.com/title/tt0068646/?ref_=nv_sr_srsg_0",
         "https://www.imdb.com/title/tt0468569/?ref_=nv_sr_srsg_0",
         "https://www.imdb.com/title/tt0071562/?ref_=tt_sims_tt_i_1",
         "https://www.imdb.com/title/tt0099674/?ref_=tt_sims_tt_i_2"]


#  A new DataExtraction object is instantiated and it takes the previous list of items as a parameter

data_extraction = DataExtraction.DataExtraction(movie_links)

# The get_movies_info function is called to get the info about each movie
# in the list. This function returns a list of movie objects

movies = data_extraction.get_movies_info()

# print(movies)



# O2 and O3
db = MovieDB("movies.ttl")

for movie in movies:
    db.write_to_databse(movie)

print('#'*80)

results = db.get_movies_by_name_and_ratings("Godfather", ">", 8, "DESC")

for item in results['items']:
    print(item)
