import math
from typing import Any, Dict, List, Mapping
from bson import ObjectId, Regex
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
    async def CommentPostMethod(data :Dict [Any, str], id:str ):
      try:        
        # print("ps", data['value'])
        post = await Post.find_one({"_id": ObjectId(id)})
        post.comments.append(data['value'])
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
        posts = await Post.find_many({"$text": {"$search": searchQuery}}).to_list()
        users = await User.find_many({"$text": {"$search": searchQuery}}).to_list()
        #response json({user, posts})
        return {"user": users, "posts":posts} 
      except:
        return None



    # GetAllPosts Related To the User && With Pagaenation 
    @staticmethod
    async def GetAllPosts(pageStr:str, id:str):
     try:
        page = 1
        if pageStr:
          page = int(pageStr)

        Limit = 2
        startIndex = (int(page) - 1) * Limit
        #...
        MainUser = await User.find_one({"_id": ObjectId(id)})
        MainUser.following.append(str(MainUser.id))        
        
        MainStr = []
        for uid in MainUser.following:
          MainStr.append( {"creator" : uid })
        
        total = await Post.find({"$or":  MainStr  }).count()
        Posts =  await Post.find({"$or":  MainStr  }).limit(Limit).skip(startIndex).to_list()
        
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





