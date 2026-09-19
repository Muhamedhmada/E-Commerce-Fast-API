from app.create_db import get_connection


def find_user(user_id: int):

    connection = get_connection()

    cursor = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    connection.close()

    return dict(user) if user else None