from cfg import DB_URL

from flask_login import UserMixin

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    create_engine,
    Column,
    Integer, String,
    Boolean,
    ForeignKey,
    LargeBinary,
    DateTime
)

engine = create_engine(DB_URL)
Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)

    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    admin = Column(Boolean, default=False)

    comment = relationship('Comment', back_populates='user')
    post = relationship('UserPost', back_populates='user')

    def get_id(self):
        return str(self.user_id)


class UserPost(Base):
    __tablename__ = 'posts'

    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False)
    post_like = Column(Integer, default=0)
    post_title = Column(String, nullable=False)
    post_desc = Column(String, nullable=True)
    post_img = Column(LargeBinary, nullable=True)
    post_tags = Column(String, nullable=True)
    post_datetime = Column(DateTime, nullable=False)

    comment = relationship('Comment', back_populates='post')
    user = relationship('User', back_populates='post')


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False)
    post_id = Column(Integer, ForeignKey(UserPost.post_id))
    comment = Column(String, nullable=False)

    post = relationship('UserPost', back_populates='comment')
    user = relationship('User', back_populates='comment')









