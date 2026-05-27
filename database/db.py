#database/db.py
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="career_user",
        password="career_pass",
        database="question_generator_db"
    )
