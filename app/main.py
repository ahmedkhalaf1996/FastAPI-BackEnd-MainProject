from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.DB.database import init_db
from app.router.Routers import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="http//localhost:4200",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## call func and connect to db
@app.on_event("startup")
async def connect():
    await init_db()

app.include_router(router, prefix="")
