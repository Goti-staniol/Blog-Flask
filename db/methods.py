from db.models import (
    User,
    UserPost,
    Comment,
    engine
)
from sqlalchemy.orm import Session, sessionmaker
from typing import List, Type

def get_session() -> Session:
    session = sessionmaker(bind=engine)
    return session()

def add_new_user(email: str, password: str) -> None:
    with get_session() as session:
        session.add(User(email=email, password=password))
        session.commit()

def check_user(email: str, password: str) -> bool:
    with get_session() as session:
        user = session.query(User).filter_by(
            email=email
        ).first()

        if user:
            if user.password == password:
                return True
            else:
                return False
        else:
            add_new_user(email, password)
            return True

def add_post(
    user_id: int,
    img: any,
    title: str,
    desc: str
) -> None:
    with get_session() as session:
        session.add(
            UserPost(
                user_id=user_id,
                img=img,
                title=title,
                desc=desc
            )
        )
        session.commit()

def get_posts() -> List[Type[UserPost]]:
    with get_session() as session:
        posts_list = []
        posts = session.query(UserPost).all()

        for post in posts:
            posts_list.append(post)

        return posts_list

def get_post(post_id: int) -> Type[UserPost]:
    with get_session() as session:
        post = session.query(UserPost).filter_by(
            post_id=post_id
        ).first()

        if post:
            return post

def add_comment(user_id: int, post_id: int, text: str) -> None:
    with get_session() as session:
        session.add(
            Comment(
                user_id=user_id,
                post_id=post_id,
                comment=text
            )
        )
        session.commit()

def get_comment(post_id: int) -> List[Type[Comment]]:
    with get_session() as session:
        comments = []

        post = session.query(UserPost).filter_by(
            post_id=post_id
        ).first()

        if post:
            for comment in post.comment:
                comments.append(comment)

            return comments














