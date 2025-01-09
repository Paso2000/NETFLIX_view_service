class View:
    """
    Represents a film view record for a user profile.

    Attributes
    ----------
    filmId : int
        The unique identifier of the viewed film.
    userId : int
        The unique identifier of the user who owns the profile.
    profileId : int
        The unique identifier of the user's profile that viewed the film.
    timesOFTheFilm : int
        The number of times the film has been viewed by the profile.

    Methods
    -------
    to_dict():
        Converts the View instance into a dictionary format.
    """

    def __init__(self, filmId: int, userId: int, profileId: int, timesOFTheFilm: int):
        """
        Initializes a View instance with film, user, profile identifiers, and view count.

        Parameters
        ----------
        filmId : int
            The unique identifier of the viewed film.
        userId : int
            The unique identifier of the user who owns the profile.
        profileId : int
            The unique identifier of the user's profile that viewed the film.
        timesOFTheFilm : int
            The number of times the film has been viewed by the profile.
        """
        self.filmId = filmId  # Unique ID of the film
        self.userId = userId  # Unique ID of the user
        self.profileId = profileId  # Unique ID of the profile
        self.timesOFTheFilm = timesOFTheFilm  # Number of views for the film

    def to_dict(self):
        """
        Converts the View instance into a dictionary.

        Returns
        -------
        dict
            A dictionary containing the viewed film, user, profile identifiers, and view count.
        """
        return {
            "filmId": self.filmId,
            "userId": self.userId,
            "profileId": self.profileId,
            "timesOFTheFilm": self.timesOFTheFilm,
        }

