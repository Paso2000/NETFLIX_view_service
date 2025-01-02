class View:

    def __init__(self, filmId: int, userId: int ,profileId: int, timesOFTheFilm: int):
        self.filmId = filmId  # Unique ID of the actor
        self.userId = userId
        self.profileId = profileId  # First name of the actor
        self.timesOFTheFilm = timesOFTheFilm  # Last name of the actor

    def to_dict(self):
        return {
            "filmId": self.filmId,
            "userId": self.userId,
            "profileId": self.profileId,
            "timesOFTheFilm": self.timesOFTheFilm,
        }


