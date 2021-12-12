from pydantic import BaseModel,EmailStr
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from datetime import date, datetime

class BasePost(BaseModel):
    
    title: str
    content: str
    published:bool=True
    
class PostCreate(BasePost):
    pass

# user Response (data that app is sending)

class Post(BasePost):
    id:int
    created_at: datetime
    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserOut(BaseModel):
    id:int
    email:str
    created_at: datetime
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    