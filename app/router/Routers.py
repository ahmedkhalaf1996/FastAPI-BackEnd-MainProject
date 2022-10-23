from fastapi import APIRouter
from app.router.posts import PostRouter

from app.router.users import UserRouter


router = APIRouter()

router.include_router(UserRouter, prefix='/user', tags=["users"])
router.include_router(PostRouter, prefix='/posts', tags=["posts"])
