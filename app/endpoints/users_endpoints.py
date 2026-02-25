
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ErrorOut, GetUserResponse
from app.services import service
from app.deps import get_session

router = APIRouter()


@router.get(
    path="/api/users/me",
    response_model=GetUserResponse,
    responses={401: {"model": ErrorOut}},
)
async def get_current_user(
        request: Request,
        api_key: str = Header(),
        session: AsyncSession = Depends(get_session),
) -> GetUserResponse:
    print("Загаловки:", dict(request.headers))
    print("DEBUG: получен api_key =", api_key)

    user = await service.get_user_by_api_key(session, api_key)
    user_data = service.user_response(user)  # Возвращает UserOut
    return GetUserResponse(result=True, user=user_data)

# Get user profile by id
@router.get(
    path="/api/users/{user_id}",
    response_model=dict,
    responses={404: {"model": ErrorOut}},
)
async def get_user_profile(
        user_id: int,
        api_key: str = Header(),
        session: AsyncSession = Depends(get_session),
) -> dict:
    # Проверка API-ключа (аутентификация)
    await service.get_user_by_api_key(session, api_key)

    user = await service.get_user_by_id(session, user_id)
    user_data = service.user_response(user)
    return {"user": user_data}

# Follow a user
@router.post(
    path="/api/users/{user_id}/follow",
    response_model=dict,
    responses={400: {"model": ErrorOut}, 404: {"model": ErrorOut}},
)
async def follow_user(
        user_id: int,
        api_key: str = Header(),
        session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Follow another user.
    """

    current_user = await service.get_user_by_api_key(session, api_key)
    await service.follow_user(session, current_user, user_id)
    # await service.follow_user(session, current_user.id, user_id)

    return {"result": True}


# Unfollow a user
@router.delete(
    path="/api/users/{user_id}/follow",
    response_model=dict,
    responses={400: {"model": ErrorOut}, 404: {"model": ErrorOut}},
)
async def unfollow_user(
        user_id: int,
        api_key: str = Header(),
        session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Unfollow a user.
    """

    current_user = await service.get_user_by_api_key(session, api_key)
    await service.unfollow_user(session, current_user, user_id)
    # await service.unfollow_user(session, current_user.id, user_id)

    return {"result": True}

