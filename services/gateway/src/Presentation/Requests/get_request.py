from pydantic import BaseModel

class GetRequest(BaseModel):
    filename: str
    cid: str
