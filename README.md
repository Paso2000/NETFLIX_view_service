# NETFLIX_view_service
ASEE Project, view service part.

## ENTITY CLASSES
### View class
- profileId: Int
- filmID: int
- timesOFTheFilm: Int


### Recommended class
- profileId: Int
- filmID : Int

## ENDPOINT
- /users/{userId}/profiles/{profileId}/views
    - GET
    - POST
- /users/{userId}/profiles/{profileId}/views/{filmID}
    -  GET
    - PUT
    - DELETE
- /users/{userId}/profiles/{profileId}/recommended
    - GET
    - POST
- /users/{userId}/profiles/{profileId}/recommended/{filmID}
    - DELETE

## Overview
