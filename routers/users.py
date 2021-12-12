from .. import schemas, utils,models
from fastapi import FastAPI,Response,status,Depends,APIRouter
from ..database import engine,get_db,SessionLocal
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session, session
#USER fuctions

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_users(user:schemas.UserCreate,db:Session=Depends(get_db)):
    # hash the password -user password
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} does not exists")
    return user