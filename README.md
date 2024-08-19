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


### API Endpoints

