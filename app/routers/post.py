from typing import List, Optional
from fastapi import Response, status, HTTPException, APIRouter

from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from app import models, oauth2, schemas
from sqlalchemy import func
from app.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id).all()
    # posts = db\
    #     .query(models.Post)\
    #     .filter(models.Post.title.contains(search))\
    #     .limit(limit=limit)\
    #     .offset(offset=skip)\
    #     .all()

    results = db\
        .query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.title.contains(search))\
        .limit(limit=limit)\
        .offset(offset=skip)\
        .all()

    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published)
    #             VALUES (%s, %s, %s)
    #        RETURNING *
    #     """,
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # the RETURNING * portion

    return new_post

# be careful of the ordering, FastAPI goes from top-down checking the routes


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    # cursor.execute(
    #     """SELECT * FROM posts
    #        WHERE id = (%s)
    #     """,
    #     (str(id))
    # )
    # post = cursor.fetchone()
    # or .all if want to find more than one

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db\
        .query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.id == id)\
        .first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Not authorized to perform requested action")
    return post
# title: str, content: str
# nothing else


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    # cursor.execute(
    #     """DELETE FROM posts
    #        WHERE id = (%s)
    #        RETURNING *
    #     """,
    #     (str(id))
    # )
    # post = cursor.fetchone()
    # conn.commit()

    post_q = db.query(models.Post).filter(models.Post.id == id)
    post = post_q.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_q.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    # cursor.execute(
    #     """UPDATE posts
    #        SET title = (%s), content = (%s), published = (%s)
    #        WHERE id = (%s)
    #        RETURNING *
    #     """,
    #     (post.title, post.content, post.published, str(id))

    # )
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_query.update(updated_post.dict())
    db.commit()

    return post_query.first()
