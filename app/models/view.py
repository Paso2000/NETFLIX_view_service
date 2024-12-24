class View:

    def __init__(self, filmId: int, profileId: Int, timesOFTheFilm: Int ):

        self.filmId = filmId  # Unique ID of the actor
        self.profileId = profileId  # First name of the actor
        self.timesOFTheFilm = timesOFTheFilm  # Last name of the actor


    def to_dict(self):

        return {
            "filmId": self.filmId,
            "profileId": self.profileId,
            "timesOFTheFilm": self.timesOFTheFilm,
        }

    @staticmethod
    def from_dict(data):
        return View(
            filmId=data.get("filmId"),
            profileId=data.get("profileId"),
            timesOFTheFilm=data.get("timesOFTheFilm"),
        )

