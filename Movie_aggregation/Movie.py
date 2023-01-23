

class Movie:

    def __init__(self, m_name, m_url, m_ratingCount, m_ratingValue, m_contentRating, m_genre, m_datePublished, m_actor, m_director, m_creator, m_duration) -> None:
        """
        Initialize a new Movie. a movie is represented by it's attributes
        which are specidied in the constructor parameters.

        Args:
            param1 (str): name of the movie
            param2 (str): url of the movie
            param3 (int): number of votes for the movie
            param4 (float): rating of the movie
            param5 (str): content rating(R rated, PG-13) of the movie
            param6 (list): genre/s of the movie
            param7 (date): date when the movie was published
            param8 (list): main actors of the movie
            param9 (list): director/s of the movie
            param10 (list): creator/s of the movie
            param11 (str): duration of the movie

        """

        self.name = m_name
        self.movie_url = m_url
        self.ratingCount = m_ratingCount
        self.ratingValue = m_ratingValue
        self.contentRating = m_contentRating
        self.genre = m_genre
        self.datePublished = m_datePublished
        self.actor = m_actor
        self.director = m_director
        self.creator = m_creator
        self.duration = m_duration


