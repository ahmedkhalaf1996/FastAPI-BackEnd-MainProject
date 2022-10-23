from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Request,  status
from fastapi.responses import JSONResponse

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
# from app.models.users_model import  User
from app.services.userService import UserService


from passlib.context import CryptContext
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


UserRouter = APIRouter()

# Authentic Login Register Part Start
# register new user
@UserRouter.post('/signup',  status_code=status.HTTP_201_CREATED)
async def createUser(user: Dict[Any, Any]):
     try:
        return await UserService.createUser(user)
     except:
        return JSONResponse(
            status_code=status.HTTP_404_BAD_REQUEST, 
            content={"message": "User Already Exist"})


# Login user
@UserRouter.post('/signin',  status_code=status.HTTP_200_OK)
async def loginUser(user: Dict[Any, Any]):
    user = await UserService.authenticate(user)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"message": "Item not found"})
    return user
# Authentic Login Register Part End...
# crud Oprations 

# getUsr info and posts Byid !! need to edit and get posts
@UserRouter.get("/getUser/{id}")
async def GetUser(id:str):
    data = await UserService.getUserByid(id)
    if not data:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error":"user not found"}
        )
    return {"user":data.user, "posts":data.posts}


# Update User
@UserRouter.patch("/Update/{id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
async def Update(userbody: Dict[Any, Any], id:str):
    try:
        return await UserService.UpdateUser(userbody, id)
        
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"Error": "Can't Update User"}
            )


# Following User
@UserRouter.patch("/{id}/following", dependencies=[Depends(JWTBearer())] , status_code=status.HTTP_200_OK)
async def getuid(request: Request, id:str):
    NextUserID = decodeJWT(request.headers["authorization"].split(" ")[1])["user_id"]
    try:
        data = await UserService.FollowingUser(id, NextUserID)
        return data
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"Error": "Can't Follow The User"}
            )


# Get Sugested Users
@UserRouter.get("/getSug", dependencies=[Depends(JWTBearer())]  ,status_code=status.HTTP_200_OK)
async def getSug(*,id:Optional[str] = None):
      try:
        users = await UserService.GetSugUsers(id)
        return users
      except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"message": "No Suggestion users"}
        )







