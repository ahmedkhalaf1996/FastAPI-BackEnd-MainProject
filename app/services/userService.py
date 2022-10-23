from typing import Any, Dict, Optional
from bson import ObjectId
from app.models.posts_model import Post

from app.models.users_model import User
from passlib.context import CryptContext
from app.auth.auth_handler import signJWT
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
# user auth Start
    # Register User
    @staticmethod
    async def createUser(user: Dict[Any, Any]):
        user_in = User(
            name= user['firstName'] +" "+ user['lastName'],
            email=user['email'],
            password=password_context.hash(user['password'])
        )
        # print(user_in)
        createdUser = await  user_in.save()
        token = signJWT(str(createdUser.id))

        return {"result":user_in, "token":token}  
    
    # Login User
    @staticmethod
    async def authenticate(userBody: Dict[Any, Any]):
        user = await UserService.get_user_by_email(email=userBody['email'])
        if not user:
            return None
        if not  password_context.verify(userBody['password'], user.password):
            return None
        
        token = signJWT(str(user.id))
        return {"result":user, "token":token}
    #getuserbyemail
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user
# user auth End
# crud Oprations Start
    
    # Get User By id
    @staticmethod
    async def getUserByid(userid:str):
        try: 
         user = await User.find_one({"_id": ObjectId(userid)})
         posts = await Post.find({"$or": {"creator":userid}})

         if user and posts:
            return {user, posts}
        except:
            return None

    # Update User
    @staticmethod
    async def UpdateUser(userbody: Dict[Any, Any], id:str):
        user = await User.find_one({"_id": ObjectId(id)})
        await user.update({"$set": userbody})
        
        return user

    # Follow User
    @staticmethod
    async def FollowingUser(id:str, NextUserID:str):
        try: 
         user1 = await User.find_one({"_id": ObjectId(id)})
         user2 = await User.find_one({"_id": ObjectId(NextUserID)})
         # check if is nextUser aleady in main userFollwoers List
         if NextUserID in user1.followers:
          user1.followers.remove(NextUserID)
          user2.following.remove(id)
         else:
          user1.followers.append(NextUserID)
          user2.following.append(id)

         await user1.save()
         await user2.save()

         return {"updateduser1": user1, "updateduser2": user2}
        
        except:
            return None

    # Get some Suggested Users for our user
    @staticmethod
    async def GetSugUsers(id:str):
       try:
         AllSugUsers = []
         MainUser = await User.find_one({"_id": ObjectId(id)})
         if MainUser:
          for FoIdes in MainUser.following:
             user = await User.find_one({"_id": ObjectId(FoIdes)})
             AllSugUsers.append(user)
         
         return {"users": AllSugUsers}
       except:
        return None