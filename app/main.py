from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from app.database import engine
from app.models import Base
from app.routers.agents import router as agents_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Homeward Agent API with Postgres")

api_v1 = FastAPI(title="Homeward Agent API v1")

@api_v1.get("/")
def root():
    return {"message": "Welcome to the Agent API"}

api_v1.include_router(agents_router)

app.mount("/api/v1", api_v1)
