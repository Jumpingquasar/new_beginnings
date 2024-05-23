import uuid


def check_uuid(check_id: str):
    try:
        uuid.UUID(check_id)
        return True
    except ValueError:
        return False
