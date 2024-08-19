import time
import numpy as np
import logging
from fastapi import FastAPI, HTTPException
from sentence_transformers import SentenceTransformer
from utils.pdf_utils import extract_text_from_pdf, chunk_text, normalize_turkish
from utils.db_utils import get_db_connection, insert_embeddings_into_db
import requests
from api.models import QueryRequest

app = FastAPI()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

processed_urls = set()


@app.post("/upload_pdf/")
async def upload_pdf(url: str):
    if url in processed_urls:
        logger.warning(f"URL already processed: {url}")
        raise HTTPException(status_code=400, detail="This URL has already been processed.")

    try:
        # Download the PDF
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        pdf_path = f'/tmp/{time.time()}.pdf'

        with open(pdf_path, 'wb') as file:
            file.write(response.content)

        # Extract and process text from PDF
        text = extract_text_from_pdf(pdf_path)

        text = normalize_turkish(text)

        # Chunk the text and compute embeddings
        chunks = chunk_text(text)
        embeddings = model.encode(chunks)

        # Insert embeddings into the database
        conn = get_db_connection()
        try:
            file_id = insert_embeddings_into_db(chunks, embeddings, conn)
        finally:
            conn.close()

        # Mark URL as processed
        processed_urls.add(url)

        logger.info(f"PDF uploaded and embeddings inserted successfully for URL: {url}")

        return {"message": "PDF uploaded and embeddings inserted successfully", "file_id": file_id}

    except requests.RequestException as e:
        logger.error(f"Failed to download the PDF: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to download the PDF: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@app.post("/query/")
async def query_embeddings(request: QueryRequest):
    try:
        query = request.query
        file_id = request.file_id
        query_embedding = model.encode([query])[0]

        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, chunk_text, embedding FROM embeddings WHERE ufid=%s", (file_id,))
            rows = cursor.fetchall()

            # Convert embeddings from string to numpy array
            embeddings = [np.fromstring(row[2].strip('[]'), sep=',') for row in rows]
            chunk_texts = [row[1] for row in rows]

            # Calculate similarity scores
            scores = [
                np.dot(query_embedding, embed) / (np.linalg.norm(query_embedding) * np.linalg.norm(embed))
                for embed in embeddings
            ]

            # Get top 5 results
            top_indices = np.argsort(scores)[-5:][::-1]
            top_chunks = [chunk_texts[i] for i in top_indices]

            logger.info(f"Query executed successfully for file_id: {file_id}")

            return {"results": top_chunks}

        finally:
            conn.close()

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
