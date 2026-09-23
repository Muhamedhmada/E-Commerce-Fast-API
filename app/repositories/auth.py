from app.create_db import get_connection



def get_user_by_email(email: str):
    db = get_connection()

    cursor = db.execute(
        "SELECT id, name, email, password FROM users WHERE email = ?",
        (email,)
    )

    return cursor.fetchone()


def create_user(name: str, email: str, password_hash: str):
    db = get_connection()

    cursor = db.execute(
        """
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
        """,
        (name, email, password_hash)
    )

    db.commit()

    return cursor.lastrowid

