from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body:str

class City(BaseModel):
    name : str
    modify : bool
    

class ShowBlog(Blog):           #use this to show  only specific part of blog on website i.e. title, body.  (id will not be shown)
    # title :str               IF I WRITE THIS, THEN , ONLY TITLE WILL GET RETURNED 
    class config():                     
        orm_mode=True

class User(BaseModel):
    name:str
    email:str
