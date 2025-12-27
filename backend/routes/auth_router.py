from fastapi import APIRouter, Depends, HTTPException, status
from backend.schemas.schema import UserCreateSchema, UserLoginSchema, UserResponseSchema
from backend.auth.service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.db.main import get_session
from backend.schemas.schema import UserResponseSchema as UserModel
from backend.auth.utils import verify_password, create_access_token, decode_token
from datetime import timedelta, datetime
from backend.auth.dependencies import RefreshTokenBearer
from fastapi.responses import JSONResponse

auth_router = APIRouter()
user_service = UserService()

@auth_router.post("/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)) :
    new_user = await user_service.create_user(user_data, session)
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )
    return new_user

@auth_router.post("/login")
async def login_user(user_data: UserLoginSchema, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    password = user_data.password   

    user = await user_service.get_user_by_email(email, session)
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid email or password."
        )
    
    access_token = create_access_token({"user_id": str(user.uid), "role": user.role}, refresh=False, expiry=timedelta(minutes=15))
    refresh_token = create_access_token({"user_id": str(user.uid), "role": user.role}, refresh=True, expiry=timedelta(days=7))

    return {
        "access_token": access_token,       
        "refresh_token": refresh_token
    }

@auth_router.get("refresh_token")
async def refresh_access_token(refresh_token_data: dict = Depends(RefreshTokenBearer())):
    expiry_date = refresh_token_data.get("exp")

    if datetime.fromtimestamp(expiry_date) > datetime.now():
        new_access_token = create_access_token(
            user_data=refresh_token_data['user']
        )

        return JSONResponse(
            content={
                "access_token": str(new_access_token)
            }
        )
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,  
        detail="Refresh token has expired, please login again."
    )
    

    
@auth_router.get("/logout")
async def logout_user():
    return {"message" : "User logged out successfully."}
    