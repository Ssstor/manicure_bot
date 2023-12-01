from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine
from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    phone =  mapped_column(BigInteger, primary_key=True)


class Entry(Base):
    __tablename__ = 'entries'
    
    occupancy: Mapped[bool]
    user_phone = mapped_column(ForeignKey('users.phone'))
    date: Mapped[str] = mapped_column(primary_key=True)



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
