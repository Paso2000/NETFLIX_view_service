# NETFLIX_view_service
ASEE Project, view service part.

## ENTITY CLASSES
### View class
- profile: Profile
- filmID: int
- timesOFTheFilm: Int
- isFinished: boolean


### Recommended class
- profile: Profile
- filmID : Int
- raccomandationType: String
- Vie-wed: Boolean

## ENDPOINT
- /users/{userId}/profiles/{profileId}/views
    - GET
    - POST
- /users/{userId}/profiles/{profileId}/views/{filmID}
    -  GET
    - PUT
    - DELETE
- /users/{userId}/profiles/{profileId}/raccomanded
    - GET
    - POST
- /users/{userId}/profiles/{profileId}/raccomanded/{filmID}
    - GET
    - PUT
    - DELETE

## Overview
