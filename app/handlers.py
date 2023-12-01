from aiogram import Router, F
from aiogram.filters import CommandStart
from magic_filter import MagicFilter
from sqlalchemy import update, select
from app.database.models import User, Entry, engine
import app.keyboards as kb
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import async_sessionmaker
from aiogram.fsm.state import State, StatesGroup


class Client(StatesGroup):
    phone = State()


router = Router()

@router.message(CommandStart())
async def cmd_start(message):
    await message.answer('Привет, это бот для записи на маникюр и педикюр к мастеру', reply_markup=kb.main)

@router.message(F.text == 'Записаться')
async def get_phone(message, state):
    await state.set_state(Client.phone)
    await message.answer(f'Введите ваш телефон в формате 89229001234:')

@router.message(Client.phone)
async def set_entry(message, state):
    await state.update_data(phone=message.text)
    Async_session = async_sessionmaker(engine)

    session = Async_session()

    new_user = User(phone=int(message.text))

    session.add(new_user)
    await session.commit()
    await message.answer('Теперь выберете время записи:', reply_markup=await kb.entries())


@router.callback_query(F.data.startswith('entry_'))
async def entry_selected(callback, state):
    entry_date = callback.data.split('_')[1]
    data = await state.get_data() 
    async with async_sessionmaker(engine)() as session:
        await session.execute(update(Entry).where(Entry.date == entry_date).values(occupancy=False, user_phone=int(data['phone'])))

        await session.commit()
        await callback.message.answer(f'Вы выбрали запись на дату {entry_date}') 




