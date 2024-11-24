import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()


class PGhandler:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
        )

    def add_history(self, user_id, text):
        # Add a new history record for the user.
        with self.conn.cursor() as cursor:
            cursor.execute(
                """ INSERT INTO user_history (user_id, text)
                VALUES (%s, %s)
                RETURNING id; """,
                (user_id, text),
            )
            self.conn.commit()

    def get_user_history(self, user_id, limit=20):
        # Retrieve the latest history records for a user, limited to a fixed number.
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """ SELECT text FROM user_history
                WHERE user_id = %s
                ORDER BY timestamp DESC
                LIMIT %s;  """,
                (user_id, limit),
            )
            return [record["text"] for record in cursor.fetchall()]

    def clean_history(self, user_id, max_records=20):
        # Replace outdated data with new input texts
        with self.conn.cursor() as cursor:
            cursor.execute(
                """DELETE FROM user_history
                WHERE user_id = %s
                AND id NOT IN (
                    SELECT id FROM user_history
                    WHERE user_id = %s
                    ORDER BY timestamp DESC
                    LIMIT %s
                );  """,
                (user_id, user_id, max_records),
            )  # This sql query replaces the oldest data point with the new one to keep the data for each user at a maximum number.
            self.conn.commit()

    def close(self):
        # close connection to DB
        self.conn.close()
