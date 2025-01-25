from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from app.database import engine
from app.models import Base
from app.routers.agents import router as agents_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Homeward Agent API with Postgres")


@app.get("/")
def root():
    return {"message": "Welcome to the Agent API!"}


app.include_router(agents_router)
