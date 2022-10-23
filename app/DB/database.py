import beanie
import motor
import motor.motor_asyncio

from app.models.posts_model import Post
from app.models.users_model import User

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://Ahmed:5747723@cluster0.l2olo5l.mongodb.net")
    
    await beanie.init_beanie(
        database=client.test,
        document_models=[User, Post] 
    )

 
