import math
from typing import Any, Dict
from bson import ObjectId
from app.models.posts_model import Post

from app.models.users_model import User



class PostService:

    # create Post
    @staticmethod
    async def createPost(post:Post):
      try:
        await post.save()
        return post
      except:
        return None




    # add comment to the post
    @staticmethod
    async def CommentPost(data :Dict [Any, str], id:str ):
      try:        
        post = await Post.find_one({"_id": ObjectId(id)})
        post.comments.append(data.value)
        await post.save()
        return post
      except:
        return None

    # GetPostById
    @staticmethod
    async def GetPostById(id:str):
      try:        
        post = await Post.find_one({"_id": ObjectId(id)})
        return post
      except:
        return None      




    # GetPostUsersBySearch
    @staticmethod
    async def GetPostUsersBySearch(searchQuery:str):
      try:
        posts = await Post.find({"$or": {"title":searchQuery, "message":searchQuery}}).to_list()
        users = await User.find({"$or": {"name":searchQuery, "bio":searchQuery}}).to_list()
        #response json({user, posts})
        return {"posts":posts,"user": users} 
      except:
        return None



    # GetAllPosts
    @staticmethod
    async def GetAllPosts(page:str, id:str):
     try:
        if not page:
          page = 1
        
        Limit = 2
        startIndex = (int(page) - 1) * Limit;

        #...
        MainUser = await User.find_one({"_id": ObjectId(id)})
        MainUser.following.append(MainUser.id)
        
        total = await Post.count({"$or":{"creator":MainUser.following}})

        Posts = await Post.find({"$or":{"creator":MainUser.following}}, 
        limit=Limit, skip=startIndex, sort=({ "_id": -1 })).to_list()
        
        return {
          "data": Posts, 
          "currentPage":page, 
          "numberOfPages": math.ceil(float(total) / float(Limit)) }
     except:
      return None

    # UpdatePost
    @staticmethod
    async def UpdatePost(id:str,  newPost: Dict[Any, Any]):
      try:  
        post = await Post.find_one({"_id": ObjectId(id)})
        await post.update({"$set": newPost})
        
        return post 
      except:
        return None



    # LikePost
    @staticmethod
    async def LikePost(id:str, UserId:str):
      try:  
        #return json(updatedpost)
        post = await Post.find_one({"_id": ObjectId(id)})
        
        if UserId in post.likes:
          post.likes.remove(UserId)
        else:
          post.likes.append(UserId)
        
        await post.save()
        
        return post      
      
      except:
        return None



    # 
    @staticmethod
    async def DeletePost(id:str):
      try:
        post = await Post.delete({"_id": ObjectId(id)})
        if post:
          return {"message":"post Deleted Successfully."}
      except:
        return None





