from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting the server...")
    await init_db()
    yield
    print("Spinning down the server...") 

app = FastAPI()

