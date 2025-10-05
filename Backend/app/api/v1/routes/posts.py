from fastapi import APIRouter, Depends, HTTPException, Request
from app.crud.post import delete_post_by_id, get_all_posts, make_new_post, get_single_post_by_id
from app.schemas.post import Post as PostSchema
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.user import verify_access_token

router = APIRouter()

@router.get("/", response_model=list[PostSchema])
def all_posts(db: Session = Depends(get_db)):
    try:
        return get_all_posts(db=db)
    except:
        print("Error @ all_posts Function, in app.api.v1.routes.post")

@router.get("/{post_id}", response_model=PostSchema)
def get_post_by_id(post_id: int,db: Session = Depends(get_db)):
    try:
        return get_single_post_by_id(db=db, id=post_id)
    except Exception as e:
        print(f"Exception @ app.api.v1.router.posts @ delete_post func: {e}")

@router.post("/new")
def new_post(post: PostSchema, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="No tokens? :(")
    payload = verify_access_token(token=token, db=db)

    try:
        return make_new_post(db=db, post=post)
    except:
        print("Error @ new_post Function, in app.api.v1.routes.post")

@router.delete("/delete/{PostId}")
def delete_post(PostId: int, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="No tokens? :(")

    payload = verify_access_token(token=token, db=db)

    try:
        return delete_post_by_id(db=db, id=PostId)
    except Exception as e:
        print(f"Exception @ app.api.v1.router.posts @ delete_post func: {e}")