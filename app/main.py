from fastapi import FastAPI
from app.routers.voice import router as voice_router

app = FastAPI()
app.include_router(voice_router)