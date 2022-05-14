from random import randrange
from typing import Optional
from fastapi import FastAPI, Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from requests import put


app = FastAPI()



# model
class Post(BaseModel):
    title:str
    content:str
    published: bool = True
    rating: Optional[int] = None

#list of data
my_posts = [{"title": "Title of post 1", "content": "Content of Post one", "id": 1},
        {"title":"Title of post 2","content":"Content of Post Two","id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i 


# get post
@app.get("/")
def read_root():
    return {"Massage": "Hello World!!!!!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id']= randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id:int,response: Response):
    post = find_post(id)
    if not post:response.status_code=status.HTTP_404_NOT_FOUND
    print(post)
    return {"post_details": post}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found")
       # response.status_code=status.HTTP_404_NOT_FOUND
       # return {"post_details": f"post with id:{id} was not found"}
    return {"post_details": post}


@app.delete("/posts/{id}")
def delete_post(id:int):
    #deleting post
    #find the index of post that was delete
    #my_post.pop(idex)

    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail=f"post id{id} does not found")

    my_posts.pop(index)
    return {'message':'post was deleted'}



@app.put("/posts/{id}")
def update_post(id: int,post:Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail=f"post id{id} does not found")

    post_dict = post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {"data":post_dict}

    return {'message':"updated post"}
#@app.get("/post/recent/latest")
#def get_latest_post():
#    post = my_posts[len(my_posts)-1]
 #   return {"details":post}



