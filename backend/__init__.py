from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.db.main import init_db
from backend.routes.auth_router import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting the server...")
    await init_db()
    yield
    print("Spinning down the server...") 

app = FastAPI(
    lifespan=lifespan
)
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
