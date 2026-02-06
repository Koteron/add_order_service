from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.client import Client

TEST_CLIENT_NAME = "Test Client"
TEST_CLIENT_ADDRESS = "123 Test Street"

# Registration is out of the task's scope, so I'll create / get a client here

async def create_or_get_test_client(session: AsyncSession) -> Client:
    result_client = await session.execute(
        select(Client)
        .where(Client.name == "Test Client")
    )
    client = result_client.scalar_one_or_none()
    
    if client:
        return client

    new_client = Client(
        name=TEST_CLIENT_NAME,
        address=TEST_CLIENT_ADDRESS
    )
    session.add(new_client)
    await session.commit()
    return new_client

