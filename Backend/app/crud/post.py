from traceback import print_tb
from sqlalchemy.orm import session
from app.db.models.posts import Post as PostDbModel
from app.schemas.post import Post as PostSchema

def get_all_posts(db: session):
    return db.query(PostDbModel).all()

def get_single_post_by_id(db: session, id: int):
    return db.query(PostDbModel).filter(PostDbModel.PostId == id).one_or_none()

def make_new_post(db: session, post: PostSchema):
    try:
        new_post = PostDbModel(**post.model_dump())

        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return "Post Successfully Uploaded"
    except Exception as e:
        print(f"Error @ function new_post in app.crud.post {e}")

def delete_post_by_id(db: session, id: int):
    try:
        post_info = db.query(PostDbModel).filter(PostDbModel.PostId == id).one_or_none()
        db.query(PostDbModel).filter(PostDbModel.PostId == id).delete()
        db.commit()
        return f'Post {id} : {post_info.Title} was successfully deleted! :(, You will never see it again XP'
    except Exception as e:
        print(f"Error @ app.crud.post @ delete_post_by_id func {e} {type(e).__name__}")
        return "Maybe the posts has already been deleted :P"
        