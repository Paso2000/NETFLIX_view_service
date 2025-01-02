class Recommended:
    def __init__(self, filmId: int, userId: int, profileId: int):
        self.filmId = filmId  # Unique ID of the film
        self.userId = userId
        self.profileId = profileId

    def to_dict(self):
        return {
            "filmId": self.filmId,
            "userId": self.userId,
            "profileId": self.profileId
        }

