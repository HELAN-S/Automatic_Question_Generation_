from database.db import get_db

def create_user(name, email, password):

    conn = get_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO users (name, email, password)
    VALUES (%s,%s,%s)
    """

    cursor.execute(query, (name, email, password))
    conn.commit()

    cursor.close()
    conn.close()


def get_user_by_email(email):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email=%s"

    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user