from typing import List, Optional
from uuid import UUID
from beanie import Document, Indexed
from pydantic import Field, EmailStr
import pymongo

class User(Document):
    
    name: str
    email: Indexed(EmailStr, unique=True)
    password: str
    bio:Optional[str] = Field(default="")
    imageUrl: Optional[str] = Field(default="")
    followers:Optional[List[str]] = Field(default=[])
    following:Optional[List[str]] = Field(default=[])
    
    class Collection:
        name = "users"
        indexes = [ # to help us search on user
            [("name", pymongo.TEXT),("email", pymongo.TEXT)],
        ]    
