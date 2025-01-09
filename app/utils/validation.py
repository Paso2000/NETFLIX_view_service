def validate_view(data):
    """
    Validates the data for a view record.

    This function checks if all required fields are present and if their types are correct.

    Parameters
    ----------
    data : dict
        The data to validate. Expected fields:
        - filmId (int): The unique ID of the viewed film.
        - userId (int): The unique ID of the user.
        - profileId (int): The unique ID of the user's profile.
        - timesOFTheFilm (int): The number of times the film has been viewed.

    Returns
    -------
    Tuple[bool, dict]
        - True and None if validation is successful.
        - False and a message dictionary if validation fails, containing details on the missing fields or type mismatches.
    """
    required_fields = {
        "filmId": int,
        "userId": int,
        "profileId": int,
        "timesOFTheFilm": int
    }

    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, {"message": f"Missing fields: {', '.join(missing_fields)}"}

    # Validate field types
    for field, field_type in required_fields.items():
        if not isinstance(data[field], field_type):
            return False, {"message": f"Field '{field}' must be of type {field_type.__name__}"}

    return True, None


def validate_recommended(data):
    """
    Validates the data for a recommended film record.

    This function checks if all required fields are present and if their types are correct.

    Parameters
    ----------
    data : dict
        The data to validate. Expected fields:
        - filmId (int): The unique ID of the recommended film.
        - userId (int): The unique ID of the user.
        - profileId (int): The unique ID of the user's profile.

    Returns
    -------
    Tuple[bool, dict]
        - True and None if validation is successful.
        - False and a message dictionary if validation fails, containing details on the missing fields or type mismatches.
    """
    required_fields = {
        "filmId": int,
        "userId": int,
        "profileId": int
    }

    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, {"message": f"Missing fields: {', '.join(missing_fields)}"}

    # Validate field types
    for field, field_type in required_fields.items():
        if not isinstance(data[field], field_type):
            return False, {"message": f"Field '{field}' must be of type {field_type.__name__}"}

    return True, None

