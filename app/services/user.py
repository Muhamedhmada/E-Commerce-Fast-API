from app.repositories import user as repo 


def get_user(user_id: int):
    return repo.find_user(user_id)

def get_users():
    return repo.get_users()