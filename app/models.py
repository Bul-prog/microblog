from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Index, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Follow(Base):
    __tablename__ = "follow"

    follower_id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True,
        nullable=False
    )
    following_id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True,
        nullable=False
    )

    __table_args__ = (
        Index("idx_follower_following", "follower_id", "following_id"),
        UniqueConstraint("follower_id", "following_id", name="uix_follow"),
    )


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    api_key = Column(String, nullable=False, unique=True)

    tweets = relationship("Tweet", back_populates="author", cascade="all, delete-orphan")
    medias = relationship("Media", back_populates="uploader")

    # Отношения через таблицу follows (модель Follow)
    # Подписчики (те, кто подписался на текущего пользователя)
    followers = relationship(
        "User",
        secondary="follow",  # Имя таблицы из Follow.__tablename__
        primaryjoin="User.id == Follow.following_id",
        secondaryjoin="User.id == Follow.follower_id",
        back_populates="following",
        lazy="selectin"  # Асинхронная загрузка
    )
    # На кого подписан текущий пользователь
    following = relationship(
        "User",
        secondary="follow",
        primaryjoin="User.id == Follow.follower_id",
        secondaryjoin="User.id == Follow.following_id",
        back_populates="followers",
        lazy="selectin"
    )


class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    author = relationship("User", back_populates="tweets")
    medias = relationship("Media", back_populates="tweet")
    likes = relationship("Like", back_populates="tweet", cascade="all, delete-orphan")


class Media(Base):
    __tablename__ = "medias"
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    url = Column(String, nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    uploader = relationship("User", back_populates="medias")
    tweet_id = Column(Integer, ForeignKey("tweets.id", ondelete="CASCADE"), nullable=True)
    tweet = relationship("Tweet", back_populates="medias")


class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    tweet_id = Column(Integer, ForeignKey("tweets.id", ondelete="CASCADE"))
    user = relationship("User")
    tweet = relationship("Tweet", back_populates="likes")





