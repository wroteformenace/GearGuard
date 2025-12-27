from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from backend.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

# This engine does the task of connecting the database to the progamming language
# engine = create_engine(
#     url=Config.DATABASE_URL,
#     echo=True
# )

# This is the async version of the engine that connects to the database.
# This is a wrapper around the normal engine to convert it into the async engine.
engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True
    )
)

# This function creates a connection to the database at the start of the server. And performs the specified tasks.
async def init_db():
    async with engine.begin() as conn:
        # Import the Book model and tell the connection to create all the tables (models) with the base class as SQLModel. 
        # If the table is already present, it will not again be created.
        """
        Import the database models here so that they are registered with SQLModel
        """
        await conn.run_sync(SQLModel.metadata.create_all) # Run synchronously and access the metadata associated with the SQLModel class and create all the tables for it if it is not already present.


# Generates an Async Session for database operations.
async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=engine, # Engine must be binded with this session
        class_=AsyncSession,
        expire_on_commit=False # Session lives even after the completion of the transaction.
    )

    async with Session() as session:
        yield session