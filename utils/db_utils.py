import psycopg2
import uuid
import numpy as np
from api.config import get_db_settings

db_settings = get_db_settings()

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=db_settings.dbname,
            user=db_settings.user,
            password=db_settings.password,
            host=db_settings.host
        )
        return conn
    except Exception as e:
        raise RuntimeError(f"Error connecting to the database: {e}")

def insert_embeddings_into_db(chunks: list, embeddings: np.ndarray, conn) -> str:
    """Inserts text chunks and their embeddings into the database.

    Args:
        chunks (list): List of text chunks.
        embeddings (np.ndarray): Array of embeddings corresponding to the text chunks.
        conn (psycopg2.connection): Database connection object.

    Returns:
        str: Unique file ID for the inserted records.
    """
    file_id = str(uuid.uuid4().hex)

    try:
        with conn.cursor() as cursor:
            for chunk_text, embedding in zip(chunks, embeddings):
                embedding_list = embedding.tolist()
                chunk_text = chunk_text.replace("\x00", "")
                cursor.execute(
                    "INSERT INTO embeddings (ufid, chunk_text, embedding) VALUES (%s, %s, %s)",
                    (file_id, chunk_text, embedding_list)
                )
            conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        raise RuntimeError(f"Error inserting data into the database: {e}")

    return file_id
