class Recommended:
    def __init__(self, filmId: int, profileId: int):
        self.filmId = filmId  # Unique ID of the film
        self.profileId = profileId

    def to_dict(self):
        return {
            "filmId": self.filmId,
            "profileId": self.profileId
        }

    @staticmethod
    def from_dict(data):
        return Recommended(
            filmId=data.get("filmId"),
            profileId=data.get("profileId")
        )
