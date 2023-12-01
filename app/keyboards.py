from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import get_entries


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Записаться')],
    # [KeyboardButton(text='Ваши записи')]
], resize_keyboard=True, input_field_placeholder='Выберите запись')


async def entries():
    entries_kb = InlineKeyboardBuilder()
    entries = await get_entries()

    for entry in entries:
        if entry.occupancy:
            entries_kb.add(InlineKeyboardButton(text=str(entry.date), callback_data=f'entry_{str(entry.date)}'))

    return entries_kb.adjust(2).as_markup()

