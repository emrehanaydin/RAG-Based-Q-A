from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    file_id: str
