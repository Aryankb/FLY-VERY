from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body:str

class ShowBlog(Blog):           #use this to show  only specific part of blog on website i.e. title, body.  (id will not be shown)
    # title :str               IF I WRITE THIS, THEN , ONLY TITLE WILL GET RETURNED 
    class config():                     
        orm_mode=True






class City(BaseModel):
    name : str
    







class UserLogin(BaseModel):
    email:str
    password:str
    lat:float
    long: float

class UserSignup(BaseModel):
    name:str
    email:str
    password:str








class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None






class CreateOrder:
    user_id:int
    product_id:int
    lat:float
    long:float
