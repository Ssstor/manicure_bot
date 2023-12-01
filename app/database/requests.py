from app.database.models import Entry, async_session 
from sqlalchemy import select


async def get_entries():
    async with async_session() as session:
        result = await session.scalars(select(Entry))
        return result


