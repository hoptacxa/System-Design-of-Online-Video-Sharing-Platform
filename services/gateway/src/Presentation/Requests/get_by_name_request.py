from pydantic import BaseModel

class GetByNameRequest(BaseModel):
    filename: str
    name: str
