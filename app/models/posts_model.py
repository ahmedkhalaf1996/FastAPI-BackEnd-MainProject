from typing import List, Optional
from datetime import datetime
from beanie import Document
from pydantic import Field

class Post(Document):
    title: str
    message: str
    creator: str
    selectedFile: str
    likes: Optional[List[str]] = Field(default=[])
    comments: Optional[List[str]] = Field(default=[])
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Collection:
        name = "posts"