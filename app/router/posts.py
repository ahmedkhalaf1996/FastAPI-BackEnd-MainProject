from typing import Any, Dict, Optional
from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from app.models.posts_model import Post
from app.services.postService import PostService

PostRouter = APIRouter()


# @PostRouter.get('/')
# async def GetAllPost():
#     pass

# Create Post
@PostRouter.post("",  dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED)
async def createPost(post: Post):
    # return {"post":post}
    try:
        return await PostService.createPost(post)
        # respnse  json(createdPost)
    except:
        return JSONResponse(
            status_code=status.HTTP_404_BAD_REQUEST, 
            content={"message": "Some thing wrong"})        

# comment Post
@PostRouter.post("/{id}/commentPost", status_code=status.HTTP_201_CREATED)
async def comment(data :Dict [Any, str], id:str ):
     try: 
        return await PostService.CommentPost(id, data)
        # response json(updatedPost)
     except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"Error": "Unable to Add Your Comment!"}
            )


# get onepost byid
@PostRouter.get("/{id}", response_model=Post)
async def getPost(id:str):
    post = await PostService.GetPostById(id)
    if not post:
         return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message":"post not found"}
        )       
    return post

# get Users&Posts by search
@PostRouter.get("/search") 
async def getBySearch(*, searchQuery:Optional[str] = None):
    try:
        return await PostService.GetPostUsersBySearch(searchQuery)
        # response json({user, posts})
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"Error": "No User Or Posts Result"}
        )

# get many post by pageanion & related to the user
@PostRouter.get("", status_code=status.HTTP_200_OK)
async def getPosts(*, page:Optional[str] = None , id:Optional[str ]= None):
    try:
        return await PostService.GetAllPosts(page, id)
        # response json({  data: posts, currentPage, numberOfPages})
    except:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content={"message": "No Posts"}
        )

# Update Post
@PostRouter.patch("/{id}",  dependencies=[Depends(JWTBearer())] , status_code=status.HTTP_200_OK)
async def Update( id:str, newPost: Dict[Any, Any]): # id = post id
    try:
        # body newpost = {title, message, creator, selectedFile }
        return await PostService.UpdatePost(id, newPost)
        # response json(updatedpost)
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"ermessage": "Can't Update post"}
            )


# like post
@PostRouter.patch("/{id}/likePost", dependencies=[Depends(JWTBearer())] )
async def Like(request: Request,id:str):
    try:
      UserId = decodeJWT(request.headers["authorization"].split(" ")[1])["user_id"]
      return await PostService.LikePost(id, UserId)
      # res json(updatedPost)
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"Can't Like The Post"}
        )        

# Delete Post
@PostRouter.delete("/{id}", dependencies=[Depends(JWTBearer())] )
async def Delete(id:str):
    try:
        return await PostService.DeletePost(id)
        # res json({message:"post Deleted Successfully."})
    except:
       return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"Can't Like The Post"}
        )        














