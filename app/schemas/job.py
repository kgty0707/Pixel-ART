from pydantic import BaseModel
from typing import Optional

class JobResponse(BaseModel):
    jobId: str
    status: str

class StatusResponse(BaseModel):
    jobId: str
    status: str

class ImageResult(BaseModel):
    jobId: str
    prompt: str
    imageUrl: Optional[str] = None
    imageData: Optional[str] = None
