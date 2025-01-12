
# NETFILX_view_service
ASEE Project, content service part.
This project provides an API for managing views and recommended.
The service is built using Python, Flask, and MongoDB, leveraging a modular architecture for handling
routes and validations.

## Features
### View Management
- Retrive all Views: Fetch all views
- Create a View: Create a new view record.
- Retrieve a View : Fetch all views for a specific view by userId, profileId and filmId.
- Update View: Modify View details.
- Delete View: Remove a View.

## Recommended Management
- Get all Recommended: Get an array of all the recommended of a profile.
- Add Recommended: Add a new recommended to a specif profile.
- Delete Recommended: Remove a recommended of a film for a specific.

## API Endpoints
### View


```GET /users/{userId}/profiles/{profileId}/views```: Retrieve all views from a specific profileId.

```POST /users/{userId}/profiles/{profileId}/views```: Create a new view for a specific profileId.

```GET /users/{userId}/profiles/{profileId}/views/{filmID}```: Retrieve details of a specific user.

```PUT /users/{userId}/profiles/{profileId}/views/{filmID}```: Update details of a specific user.

```DELETE /users/{userId}/profiles/{profileId}/views/{filmID}```: Delete a user and all associated profiles.

### Recommended
```GET /users/{userId}/profiles/{profileId}/recommended```: Retrieve all recommended for a specific profile.

```POST /users/{userId}/profiles/{profileId}/recommended```: Add a new recommended from a specific profile.

```DELETE /users/{userId}/profiles/{profileId}/recommended/{filmId}```: Remove a recommended of a film for a specific.

## Usage
### Example Requests

#### Example of View
```{
"filmId": 1,
"userId": 1,
"profileId": 1,
"timesOFTheFilm": 13
}
```
#### Example of Recommended
```
{
"filmId": 5,
"userId": 1,
"profileId": 1
}
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.


