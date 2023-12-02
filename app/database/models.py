from typing import Optional
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import DATABASE_URL

# DATABASE_URL = 'postgresql+asyncpg://savva@localhost/teleb'

engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class Entry(Base):
    __tablename__ = 'entries'
    
    occupancy: Mapped[bool]
    user_phone: Mapped[Optional[str]]
    date: Mapped[str] = mapped_column(primary_key=True)



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
