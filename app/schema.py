from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class QRCodeRequest(BaseModel):
    url: HttpUrl  # This ensures the URL is valid
    description: Optional[str] = None

class QRCodeResponse(BaseModel):
    filename: str
    url: HttpUrl
    download_url: str
    description: Optional[str] = None
    links: Optional[List[dict]] = []
