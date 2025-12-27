from fastapi import APIRouter, Depends, HTTPException, status

auth_router = APIRouter()

@auth_router.post("/signup")
async def create_user(user_data: UserCreateSchema):
    pass