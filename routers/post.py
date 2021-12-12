from .. import schemas, utils,models
from fastapi import FastAPI,Response,status,Depends,APIRouter
from ..database import engine,get_db,SessionLocal
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session, session
from typing import Optional,List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



# used list to wrap up whole posts
@router.get('/',response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
    post = db.query(models.Post).all()
    return post

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db)):
    
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}',response_model=schemas.Post)
def get_posts2(id:int,db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The post with id {id} does not exits')
    
    return post

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id {id} does not exist")
    else:
        post.delete(synchronize_session=False)
        db.commit()

    return {'data':'successfull'}

@router.put('/{id}',response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,db:Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id {id} does not exist")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()