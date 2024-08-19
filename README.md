docker run -it --rm -p 8000:8000 rag-question-answer-api

This project includes a question-answer system based on Retrieval-Augmented Generation (RAG). The project uses natural language processing (NLP) methods to answer questions posed based on specific data settings.

## Features

- Can load and process PDF documents.
- Generates meaningful answers by analyzing the content.
- Indexes embedded texts using PostgresQL database.


## Getting Started

### Requirements

- Python 3.8 or newer
– Docker

### Setup

#### Virtual Environment

1. Create and activate the Python virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate

2. Pip install -r requirements.txt

3. Docker build -t rag-question-answer-api .

4. Docker run -it --rm -p 8000:8000 rag-question-answer-api


API Endpoints

Upload PDF
URL: /upload_pdf/
Method: POST
Parameters:
url (string): The URL of the PDF file to upload.

Response:
message (string): A message indicating the success of the operation.
file_id (integer): The ID of the file in the database.
Example Request:

bash
Copy Code
curl -X POST "http://localhost:8000/upload_pdf/" -H "Content-Type: application/json" -d '{"url": "https://example.com/sample.pdf"}'
Example Response:

json
Copy Code
{
    "message": "PDF uploaded and embeddings inserted successfully",
    "file_id": 123
}
Query Embeddings
URL: /query/
Method: POST
Parameters:
query (string): The text to query.
file_id (integer): The ID of the PDF file in the database.
Response:
results (array of strings): The most relevant text chunks based on the query.
Example Request:

bash
Kodu kopyala
curl -X POST "http://localhost:8000/query/" -H "Content-Type: application/json" -d '{"query": "What is the main topic of the PDF?", "file_id": 123}'
Example Response:

json
Copy Code
{
    "results": [
        "The main topic is artificial intelligence.",
        "The document discusses machine learning techniques.",
        "Detailed explanation of neural networks.",
        "Overview of AI applications in various fields.",
        "Future trends in artificial intelligence."
    ]
}

