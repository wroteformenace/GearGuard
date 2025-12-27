from sqlmodel.ext.asyncio.session import AsyncSession
from backend.db.Models import User
from backend.schemas.schema import UserCreateSchema
from sqlmodel import select
from backend.auth.utils import generate_hash_password


class UserService:
    async def create_user(self, user_data: UserCreateSchema, session: AsyncSession) -> dict | None:
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password_hash = generate_hash_password(user_data_dict["password"])
        if await self.user_exists(new_user.email, session):
            return None
        session.add(new_user)
        await session.commit()
        return new_user


    async def user_role(self, user_id: int, session: AsyncSession) -> str:
        statement = select(User.role).where(User.id == user_id)
        results = await session.exec(statement)
        role = results.first()
        if role is None:
            return None
        return role
        

    async def get_user_by_email(self, email: str, session: AsyncSession) -> User | None:
        statement = select(User).where(User.email == email)
        results = await session.exec(statement)
        return results.first()
    
    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return user is not None
