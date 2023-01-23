from rdflib import Graph, Literal, URIRef, Namespace, RDF
from Movie import Movie
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import XSD
import datetime
import os
import __main__


class MovieDB:
    """
    The MovieDB class is intended to manage a small ttl database file which
    stores the schema.org format of movies as RDF.

    The class is used to write data in the database file but also read from the file.

    The reading is done with the help of some functions that use SPARQL queries in order
    to get the desired info from the database file
    """
    def __init__(self, db_name: str):
        """
        initialize a new object

        Args:
            param1 (str): name of the ttl database file which will be initialized
        """
        self.schema = Namespace("http://schema.org/")        
        self.graph = Graph()
        self.graph.bind("schema", self.schema)
        self.project_path = os.path.dirname(__main__.__file__)
        self.database = f'{self.project_path}\{"database_files"}\{db_name}'


    def write_to_databse(self, movie: Movie) -> None:
        """
        This function is used to write the builded rdf object in the ttl database
        file. it appends the serialized rdf object to the file without removing
        the old data, this way it can behave as a database with a history of the data
        that has been inserted

        Args:
            param1 (Movie object): this parameter represents a Movie object that
                                     contains all the info about a movie obtained
                                     from a json_ld at a previous step

        Return:
            None
        """
        self.graph.remove((None, None, None))
        self.build_movie_as_rdf(movie)

        with open(self.database, 'ab') as f:
            f.write(self.graph.serialize(format='turtle').encode())


    def _read_database_file(self):
        """
        This method is marked as a private function and it is used to
        update the graph object with the newest content of the database file
        before each query is executed

        Return:
            a graph object with the content of the database file
        """
        db_content = self.graph.parse(self.database, format='turtle')
        return db_content


    def check_if_movie_exists(self, keyword: str) -> bool:
        """
        This method is used to check if a specific movie exists in the database
        file.

        Args:
            param1 (str): this param represents an item that will be 
                          searched  in the database

        Return:
            True if the movie exists, False otherwise
        """
        self.graph = self._read_database_file()

        query = f"""
        PREFIX schema: <http://schema.org/>
        ASK {{
            ?movie a schema:Movie .
            ?movie schema:name "{keyword}" .
        }}
        """

        results = self.graph.query(query)
        return results.askAnswer



    def get_movies_by_name_and_ratings(self, keyword: str, criteria: str, rating: int, order: str):
        """
        Extracts the movies that contain the keyword you insert.
        The movies will contain all the info about a movie which can be filtered by the lowest
        or highest rating value and also they can be sorted ascending or descending.
        This function will build a SPARQL query that will extract the movies based on
        the user inputs
        Args:
            param1 (str): keyword that will be used to search the movie you want
            param2 (str): this param is used to filter the movie by rating
                          Posible values: >, <, >=, <=
            param3 (int): the rating value of the desired movie
            param4 (str): this param will help you to filter the movies by their rating
                          ascending or descending
                          Posible values: ASC, DESC  
        Return; JSON object with the movies found
        """
        self.graph = self._read_database_file()

        query_string = f"""
        PREFIX schema: <http://schema.org/>

        SELECT *
        WHERE {{
          ?movie a schema:Movie .
          ?movie schema:name ?name .
          ?movie schema:ratingCount ?ratingCount .
          ?movie schema:ratingValue ?ratingValue .
          ?movie schema:contentRating ?contentRating .
          ?movie schema:genre ?genre .
          ?movie schema:datePublished ?datePublished .
          ?movie schema:actor ?actor .
          ?movie schema:director ?director .
          ?movie schema:creator ?creator .
          ?movie schema:duration ?duration .
          FILTER(regex(?name, "{keyword}", "i") && ?ratingValue {criteria} {rating})
        }}
        ORDER BY {order}(?ratingValue)
        """
        data = {}
        data['items'] = []
        query = prepareQuery(query_string)
        results = self.graph.query(query)

        for row in results:
            data['items'].append({
                "name": row.name.value,
                "ratingCount": row.ratingCount.value,
                "ratingValue": row.ratingValue.value,
                "contentRating": row.contentRating.value,
                "genre": row.genre.value,
                "datePublished": row.datePublished.value,
                "actor": row.actor.value,
                "director": row.director.value,
                "creator": row.creator.value,
                "duration": row.duration.value
            })

        return data    


    def get_date_time_formated(self) -> str:
        """
        This method is used to get the date and time that will be used to identify
        when a specific movie was inserted in the database file

        Return:
            Literal with the date and time formated
        """
        now = datetime.datetime.now()
        return Literal(now.isoformat(), datatype=XSD.dateTime)


    def build_movie_as_rdf(self, movie: Movie) -> None:
        """
        Creates a movie from the Movie object that will be formated as RDF
        with all the info in it. This function will be called after the created
        object will be written in the database ttl file

        Args:
            param1 (Movie object): this parameter represents a Movie object that
                                     contains all the info about a movie obtained
                                     from a json_ld at a previous step

        Return:
            None
        """
        movie_url = URIRef(movie.movie_url)
        self.graph.add((movie_url, RDF.type, self.schema.Movie))
        self.graph.add((movie_url, self.schema.name, Literal(movie.name)))
        self.graph.add((movie_url, self.schema.ratingCount, Literal(float(movie.ratingCount), datatype=XSD.integer)))
        self.graph.add((movie_url, self.schema.ratingValue, Literal(float(movie.ratingValue), datatype=XSD.float)))
        self.graph.add((movie_url, self.schema.contentRating, Literal(movie.contentRating)))
        self.graph.add((movie_url, self.schema.genre, Literal(movie.genre)))
        self.graph.add((movie_url, self.schema.datePublished, Literal(movie.datePublished)))
        self.graph.add((movie_url, self.schema.actor, Literal(movie.actor)))
        self.graph.add((movie_url, self.schema.director, Literal(movie.director)))
        self.graph.add((movie_url, self.schema.creator, Literal(movie.creator)))
        self.graph.add((movie_url, self.schema.duration, Literal(movie.duration)))
        self.graph.add((movie_url, self.schema.dateCreated , self.get_date_time_formated()))

    