from app.create_db import get_connection



def get_user_by_email(email: str):
    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT id, name, email, password FROM users WHERE email = ?",
            (email,)
        )

        return cursor.fetchone()
    finally:
        connection.close()


def create_user(name: str, email: str, password_hash: str):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, password_hash)
        )

        connection.commit()

        return cursor.lastrowid
    finally:
        connection.close()

