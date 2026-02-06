from os import environ
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.models.base import Base
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext

db_user = environ.get("DB_USER", "user")
db_pass = environ.get("DB_PASSWORD", "password")
db_host = environ.get("DB_HOST", "localhost")
db_port = environ.get("DB_PORT", "5432")
db_name = environ.get("DB_NAME", "mydb")

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def verify_schema():
    async with engine.begin() as conn:
        def _sync_verify(sync_conn):
            ctx = MigrationContext.configure(sync_conn)
            diff = compare_metadata(ctx, Base.metadata)
            if diff:
                for d in diff:
                    print(d)
                raise RuntimeError("DB schema verification failed")
        
        await conn.run_sync(_sync_verify)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
