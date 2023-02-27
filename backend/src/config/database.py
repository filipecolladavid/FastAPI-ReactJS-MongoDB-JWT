from .settings import settings
from ..models.user import User

from motor.motor_asyncio import AsyncIOMotorClient

from beanie import init_beanie


# Call this from within your event loop to get beanie setup.
async def startDB():
    # Create Motor client
    client = AsyncIOMotorClient(settings.DATABASE_URL)

    # Init beanie with the Product document class
    await init_beanie(database=client.db_name, document_models=[User])