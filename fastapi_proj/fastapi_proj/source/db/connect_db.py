import sys
import os

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from dotenv import load_dotenv


load_dotenv()

if os.getenv("DOCKER_ENV") == "true":
    SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL_DOCKER")
else:
    SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL_LOCAL")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)  # type: ignore

SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await session.close()
