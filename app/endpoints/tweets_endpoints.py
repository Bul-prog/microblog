from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.schemas import TweetCreate, TweetOut, ErrorOut
from app.services import service
from app.deps import get_session, get_current_user

router = APIRouter()

@router.post("/api/tweets", response_model=dict)
async def create_tweet(payload: TweetCreate, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    tweet = await service.create_tweet(session, current_user, payload.tweet_data, payload.tweet_media_ids)
    return {"result": True, "tweet_id": tweet.id}

@router.get("/api/tweets", response_model=dict)
async def get_feed(current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    tweets = await service.get_feed(session, current_user)
    res=[]
    for t in tweets:
        res.append(TweetOut(
            id=t.id,
            content=t.content,
            attachments=[m.url for m in t.medias],
            author={"id": t.author.id, "name": t.author.name},
            likes=[{"user_id": l.user_id, "name": l.user.name} for l in t.likes]
        ))
    return {"result": True, "tweets": res}
