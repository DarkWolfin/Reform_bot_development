from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext


from Token import Token
bot = Bot(Token)

from Databases import db_start, data_profile

import FSM_classes
import Markups


async def choose_specialist(message: types.message, state: FSMContext):
    await FSM_classes.MultiDialog.specialist.set()
    await bot.send_message(message.from_user.id, 'В скором времени появится возможность записаться к психотерапевту на приём или наладить с ним контакт путем письменного общения')