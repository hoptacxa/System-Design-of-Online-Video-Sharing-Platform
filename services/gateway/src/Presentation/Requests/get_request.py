from pydantic import BaseModel

class GetRequest(BaseModel):
    cid: str
