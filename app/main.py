import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.deps import init_models
from app.endpoints.users_endpoints import router as users_router
from app.endpoints.tweets_endpoints import router as tweets_router
from app.endpoints.medias_endpoints import router as medias_router
from app.test_key import create_test_users
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

@app.get("/")
async def healthcheck():
    return {"result": True}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["api_key", "Content-Type", "Authorization"],
)

app.mount("/media", StaticFiles(directory="app/media"), name="media")

app.include_router(users_router)
app.include_router(tweets_router)
app.include_router(medias_router)


@app.on_event("startup")
async def startup():
    await init_models()
    # await create_test_users()

@app.get("/api/routes")
async def list_routes():
    return [{"path": route.path, "name": route.name} for route in app.routes]


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

