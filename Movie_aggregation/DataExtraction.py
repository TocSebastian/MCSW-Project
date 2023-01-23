import typing
import extruct
import requests
from Movie import Movie
from w3lib.html import get_base_url


class DataExtraction:
    def __init__(self, list_of_items: typing.List[str]) -> None:
        """
        Initialize a new DataExtraction class. It also initialize the headers
        that will be used with the requests library and the syntaxes used
        to extract the Schema.org from the movies

        Args:
            param1 (List[str]): list of URLs to different movies on different sites.
        """
        self.urls = list_of_items
        self.syntaxes = ['json-ld','opengraph','microdata','rdfa']
        self.missing_info = "0"
        self.headers = {
                        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
                        "Accept-Language": "en-US, en;q=0.5"
                       }


    def extract_metadata(self, url) -> typing.Dict:
        """
        Extracts the medatada from a website. The metadata contains the
        Schema.org data about the movie. This method will look for syntaxes
        defined in the self.syntaxes variable from the constructor

        Args:
            param1 (str): URL to the desired movie

        Return: dictionary with the metadata content

        Raise a Value error in case the request fails
        """
        try:
            r = requests.get(url, headers=self.headers)
        except Exception:
            raise ValueError(f'Requested URL {url} is not correct. Make sure that you entered a valid URL')

        base_url = get_base_url(r.text, r.url)
        metadata = extruct.extract(r.text, 
                               base_url=base_url,
                               uniform=True,
                               syntaxes=self.syntaxes)                                  
        return metadata


    def get_movie_info_as_jsonld(self, metadata_dict,
                                    target_key, target_value) -> typing.Dict:
        """
        Extracts the info about a movie in a json ld format.
        it searches for a key with a specific value  in the metadata and gets 
        that information.

        Args:
            param1 (Dict): metadata that will be used to search the movie type
            param2 (str): key that will be searched in the metadata json.
            param3 (str): value of the key thwt will be searched for

        Return: dictionary with the Movie info
        """  
        for key in metadata_dict:
            if len(metadata_dict[key]) > 0:
                for item in metadata_dict[key]:
                    if target_key in item:
                        if item[target_key] == target_value:
                            return item

    def extract_data_from_jsonld(self, movie_dict) -> typing.Dict:
        """
        Searches for different categories in the received JSON string with
        the Movie info.

        Args:
            param1 (Dict): dictionary that will contain the Movie info

        Return: dict with the required fields if succedded, a dict with the
                missing value for each key in it if something went wrong
        """

        base_url = 'https://www.imdb.com'

        dict = {"name": "", "url": "", "ratingCount": "", "ratingValue": "", "contentRating": "", "genre": "",
                "datePublished": "", "actor": "", "director": "", "creator": "", "duration": ""}

        try:

            dict["name"] = movie_dict.get("name") or 0
            dict["url"] = base_url + movie_dict.get("url") or 0
            dict["contentRating"] = movie_dict.get("contentRating") or 0
            dict["genre"] = movie_dict.get("genre") or 0
            dict["datePublished"] = movie_dict.get("datePublished") or 0
            dict["duration"] = movie_dict.get("duration") or 0

            # rating data

            rating = movie_dict.get("aggregateRating")

            dict["ratingCount"] = rating.get("ratingCount") or 0
            dict["ratingValue"] = rating.get("ratingValue") or 0

            # actor data

            actor = movie_dict.get("actor")
            actor_data = []

            for data in actor:
                actor_data.append(data.get('name'))

            dict["actor"] = actor_data or 0

            # director data

            director = movie_dict.get("director")
            director_data = []

            for data in director:
                director_data.append(data.get('name'))

            dict["director"] = director_data or 0

            # creator data

            creator = movie_dict.get("creator")
            creator_data = []

            for data in creator:
                if 'name' in data:
                    creator_data.append(data.get('name'))

            dict["creator"] = creator_data or 0

            return dict

        except:
            for key in dict:
                dict[key] = self.missing_info

            return dict


    def get_movies_info(self) -> typing.List[Movie]:
        """
        This is the main function that will parse and extract all the info
        from each URL in the list of URLs required by the user.
        This method will search for data about the movie

        Return: list of Movie objects that contain the info for each movie as a whole.
        """
        movies = []

        for item in self.urls:
            metadata = self.extract_metadata(item)
            movie_dict  = self.get_movie_info_as_jsonld(metadata, '@type', 'Movie')
            
            movie_info = self.extract_data_from_jsonld(movie_dict)
            # print(movie_dict)
            print(movie_info)

            movies.append(Movie(movie_info["name"],
                                    movie_info["url"],
                                    movie_info["ratingCount"],
                                    movie_info["ratingValue"],
                                    movie_info["contentRating"],
                                    movie_info["genre"],
                                    movie_info["datePublished"],
                                    movie_info["actor"],
                                    movie_info["director"],
                                    movie_info["creator"],
                                    movie_info["duration"]))


        return movies