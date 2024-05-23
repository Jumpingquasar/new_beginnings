import time

import psycopg2
from fastapi import FastAPI, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from starlette.responses import Response

import app.models.posts
from app.database import engine, get_db
from app.helpers.check_uuid import check_uuid
from app.models import posts
from app.schemas.posts import Post

posts.Base.metadata.create_all(bind=engine)

while True:
    try:
        psycopg2.connect(host="localhost", database="fastapi", user="postgres",
                         password="1945", port=5432, cursor_factory=RealDictCursor)
        print("Connected to PostgreSQL")
        break
    except Exception as e:
        print("Failed to connect to PostgreSQL")
        print("Error: ", e)
        print("Retrying in 5 seconds...")
        time.sleep(5)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World!!!"}


@app.get("/posts")
def posts(db: Session = Depends(get_db)):
    all_posts = db.query(app.models.posts.Post).all()
    return {"data": all_posts}


@app.get("/posts/{post_id}")
def get_post_by_id(post_id: str, db: Session = Depends(get_db)):
    if not (check_uuid(post_id)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID format")

    post = db.query(app.models.posts.Post).filter(post_id == app.models.posts.Post.id).first()
    if post is not None:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.post("/posts")
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = app.models.posts.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.put("/posts/{post_id}")
def update_post(post_id: str, post: Post, db: Session = Depends(get_db)):
    if not (check_uuid(post_id)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID format")

    post_query = db.query(app.models.posts.Post).filter(post_id == app.models.posts.Post.id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}


@app.delete("/posts/{post_id}")
def delete_post(post_id: str, db: Session = Depends(get_db)):
    if not (check_uuid(post_id)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID format")
    deleted_post = db.query(app.models.posts.Post).filter(post_id == app.models.posts.Post.id)
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    else:
        deleted_post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
