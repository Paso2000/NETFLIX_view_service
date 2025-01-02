
def validate_view(data):

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
