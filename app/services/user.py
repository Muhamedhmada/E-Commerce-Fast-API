from app.repositories.user import find_user


def get_user(user_id: int):
    return find_user(user_id)