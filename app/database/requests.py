from app.database.models import Entry, async_session
from datetime import datetime, timedelta
# from models import Entry
from sqlalchemy import select, insert
from sqlalchemy.sql import func
# from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import DATABASE_URL
# import asyncio

# DATABASE_URL = 'postgresql+asyncpg://savva@localhost/teleb'

# engine = create_async_engine(DATABASE_URL)
#
# async_session = async_sessionmaker(engine)


async def get_entries():
    async with async_session() as session:
        entries_count = await session.execute(func.count(Entry.date))

        entries_count = int(entries_count.scalar())

        if entries_count < 30:
            current_date = datetime.now()
            i = 0
            while entries_count < 30:
                new_date = current_date + timedelta(days=i)

                if new_date.weekday() < 5:
                    for hour in [10, 11, 12, 15, 16]:
                        entry_date = new_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                        await session.execute(insert(Entry).values(occupancy=True, date=str(entry_date)))
                        entries_count += 1
                        
                i += 1

            await session.commit()


        result = await session.scalars(select(Entry).order_by(Entry.date))

        return result


# if __name__ == "__main__":
#     asyncio.run(get_entries())
