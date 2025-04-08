from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from pydantic import BaseModel

class QRCodeRequest(BaseModel):
    url: HttpUrl  # This ensures the URL is valid
    description: Optional[str] = None

class QRCodeResponse(BaseModel):
    filename: str
    url: HttpUrl
    download_url: str
    description: Optional[str] = None
    links: Optional[List[dict]] = []

class Token(BaseModel):
    access_token: str
    token_type: str
