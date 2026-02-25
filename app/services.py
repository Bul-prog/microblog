from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.schemas import UserOut, UserShort
from sqlalchemy.orm import selectinload

from app.models import User, Tweet, Media, Like, Follow

class Service:

    async def get_user_by_api_key(self, session: AsyncSession, api_key: str) -> User:
        result = await session.execute(select(User).where(User.api_key == api_key).options(selectinload(User.followers),
                                                                                           selectinload(User.following))  # Загрузка связей
        )
        print(f"DEBUG: get_user_by_api_key api_key='{api_key}'")
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid api-key")
        return user


    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> User:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def create_tweet(self, session: AsyncSession, user: User, content: str, media_ids: Optional[List[int]] = None) -> Tweet:
        tweet = Tweet(content=content, author_id=user.id)
        session.add(tweet)
        await session.flush()
        if media_ids:
            result = await session.execute(select(Media).where(Media.id.in_(media_ids), Media.uploader_id == user.id))
            medias = result.scalars().all()
            for m in medias:
                m.tweet_id = tweet.id
        await session.commit()
        return tweet

    async def delete_tweet(self, session: AsyncSession, user: User, tweet_id: int) -> None:
        result = await session.execute(select(Tweet).where(Tweet.id == tweet_id))
        tweet = result.scalar_one_or_none()
        if not tweet:
            raise HTTPException(status_code=404, detail="Tweet not found")
        if tweet.author_id != user.id:
            raise HTTPException(status_code=403, detail="Forbidden")
        await session.delete(tweet)
        await session.commit()

    async def save_media(self, session: AsyncSession, user: User, filename: str, url: str) -> Media:
        media = Media(filename=filename, url=url, uploader_id=user.id)
        session.add(media)
        await session.commit()
        return media

    async def add_like(self, session: AsyncSession, user: User, tweet_id: int):
        result = await session.execute(select(Tweet).where(Tweet.id == tweet_id))
        tweet = result.scalar_one_or_none()
        if not tweet:
            raise HTTPException(status_code=404, detail="Tweet not found")
        result = await session.execute(select(Like).where(Like.user_id == user.id, Like.tweet_id == tweet_id))
        if result.scalar_one_or_none():
            return
        like = Like(user_id=user.id, tweet_id=tweet_id)
        session.add(like)
        await session.commit()

    async def remove_like(self, session: AsyncSession, user: User, tweet_id: int):
        result = await session.execute(select(Like).where(Like.user_id == user.id, Like.tweet_id == tweet_id))
        like = result.scalar_one_or_none()
        if like:
            await session.delete(like)
            await session.commit()

    async def follow_user(self, session: AsyncSession, user: User, target_id: int):
        if user.id == target_id:
            raise HTTPException(status_code=400, detail="Cannot follow yourself")
        target = await self.get_user_by_id(session, target_id)
        result = await session.execute(select(Follow).where(Follow.follower_id == user.id, Follow.following_id == target.id))
        if result.scalar_one_or_none():
            return
        follow = Follow(follower_id=user.id, following_id=target.id)
        session.add(follow)
        await session.commit()

    async def unfollow_user(self, session: AsyncSession, user: User, target_id: int):
        result = await session.execute(select(Follow).where(Follow.follower_id == user.id, Follow.following_id == target_id))
        follow = result.scalar_one_or_none()
        if follow:
            await session.delete(follow)
            await session.commit()

    async def get_feed(self, session: AsyncSession, user: User) -> List[Tweet]:
        # закомментиррованы для теста
        # result = await session.execute(select(Follow.following_id).where(Follow.follower_id == user.id))
        # following_ids = [row[0] for row in result.all()]
        # if not following_ids:
        #     return []
        result = await session.execute(select(Tweet).options(selectinload(Tweet.medias), selectinload(Tweet.author), selectinload(Tweet.likes))) #.where(Tweet.author_id.in_(following_ids)))
        tweets = result.scalars().all()
        tweets.sort(key=lambda t: len(t.likes), reverse=True)
        return tweets

    async def get_user_profile(self, session: AsyncSession, user: User) -> User:
        return user

    async def get_user_profile_by_id(self, session: AsyncSession, uid: int) -> User:
        return await self.get_user_by_id(session, uid)

    def user_response(self, user: User) -> UserOut:
        """
        Convert ORM User model into UserOut schema.
        """

        followers = [
            UserShort(id=f.id, name=f.name)
            for f in (user.followers or [])
            if f is not None
        ]

        following = [
            UserShort(id=f.id, name=f.name)
            for f in (user.following or [])
            if f is not None
        ]
        print(f"User {user.id} has {len(user.followers)} followers and {len(user.following)} following!!!!!!!!!!!!!!!!!!!!!!")

        return UserOut(
            id=user.id,
            name=user.name,
            followers=followers,
            following=following
        )


service = Service()
