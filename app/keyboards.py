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
    count = 5

    for entry in entries:
        count += 1

        if count == 6:
            count = 1
            date = entry.date.split('-')[2][:2]
            entries_kb.add(InlineKeyboardButton(text=f'{date}', callback_data='ojeiejo'))

        if entry.occupancy:
            date = entry.date.split()[1].split(':')[0] + 'ч' # + entry.date.split()[1].split(':')[1]
            entries_kb.add(InlineKeyboardButton(text=f'{date} ✅', callback_data=f'entry_{entry.date}'))

        else:
            date = entry.date.split()[1].split(':')[0] + 'ч' # + entry.date.split()[1].split(':')[1] 
            entries_kb.add(InlineKeyboardButton(text=f'{date} ❌', callback_data='entry_0'))


    return entries_kb.adjust(6).as_markup()

