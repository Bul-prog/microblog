import os
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import service
from app.deps import get_session, get_current_user

router = APIRouter()

MEDIA_FOLDER = "app/media"
os.makedirs(MEDIA_FOLDER, exist_ok=True)

@router.post("/api/medias")
async def upload_media(file: UploadFile = File(...), current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if not file:
        raise HTTPException(status_code=400, detail="File required")
    fp=os.path.join(MEDIA_FOLDER, file.filename)
    with open(fp,"wb") as f:
        f.write(await file.read())
    media = await service.save_media(session, current_user, file.filename, f"/media/{file.filename}")
    return {"result": True, "media_id": media.id}
