import asyncio
import os
import sqlite3

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ReplyKeyboardRemove
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked

from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())

import Markups
import FSM_classes
from Database import help_system_good, help_system_norm, help_system_bad, help_system_agreement


async def choose_helpsystem(message: types.Message, state: FSMContext):
    if message.text == 'Хорошо 😀':
        await help_system_good(user_id=message.from_user.id)
        await bot.send_message(message.from_user.id, 'Это замечательно! (Что-нибудь на позитивном + пожелание хорошего вечера)', reply_markup=ReplyKeyboardRemove())
        await bot.send_message(message.from_user.id,'Желаете попробовать практику благодарности (запуск на 1 неделе для всех)?', reply_markup=Markups.try_practice_good)
        await state.set_state(FSM_classes.HelpSystem.good_condition)
    elif message.text == 'Нормально 🙂':
        await help_system_norm(user_id=message.from_user.id)
        await bot.send_message(message.from_user.id, 'Вы бы хотели сделать ваше состояние еще лучше?')
        await state.set_state(FSM_classes.HelpSystem.norm_condition)
    elif message.text == 'Плохо 😢':
        await help_system_bad(user_id=message.from_user.id)
        await bot.send_message(message.from_user.id, '')
        await state.set_state(FSM_classes.HelpSystem.bad_condition)


async def try_practice(callback_query: types.CallbackQuery, state: FSMContext):
    db_helpsys = sqlite3.connect('Databases/Help_system.db')
    cur_helpsys = db_helpsys.cursor()
    if callback_query.data[-1] == 'y':
        if callback_query.data[-2] == 'g':
            cur_helpsys.execute("UPDATE good SET try_practice = ? WHERE user_id = ?", ('Да', callback_query.from_user.id))
        elif callback_query.data[-2] == 'n':
            cur_helpsys.execute("UPDATE norm SET try_practice = ? WHERE user_id = ?", ('Да', callback_query.from_user.id))
        else:
            cur_helpsys.execute("UPDATE bad SET try_practice = ? WHERE user_id = ?", ('Да', callback_query.from_user.id))
        db_helpsys.commit()

        await bot.send_message(callback_query.from_user.id, 'Переход на практику "Благодарности"')
    else:
        if callback_query.data[-2] == 'g':
            cur_helpsys.execute("UPDATE good SET try_practice = ? WHERE user_id = ?", ('Нет', callback_query.from_user.id))
            await bot.send_message(callback_query.from_user.id,
                                   'Чтобы ваше состояние оставалось всегда в норме, хотим предложить поддержку, содержащую в себе практики и упражнения для разгрузки, а также общие советы по поддержке. '
                                   '\nХотите попробовать?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                    InlineKeyboardButton('Да, можно попробовать', callback_data='agreement_mailing_help_gy'),
                    InlineKeyboardButton('Нет, не хочу', callback_data='agreement_mailing_help_gn')))
        elif callback_query.data[-2] == 'n':
            cur_helpsys.execute("UPDATE norm SET try_practice = ? WHERE user_id = ?", ('Нет', callback_query.from_user.id))
            await bot.send_message(callback_query.from_user.id,
                                   'Чтобы ваше состояние оставалось всегда в норме, хотим предложить поддержку, содержащую в себе практики и упражнения для разгрузки, а также общие советы по поддержке. '
                                   '\nХотите попробовать?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                    InlineKeyboardButton('Да, можно попробовать', callback_data='agreement_mailing_help_ny'),
                    InlineKeyboardButton('Нет, не хочу', callback_data='agreement_mailing_help_nn')))
        else:
            cur_helpsys.execute("UPDATE bad SET try_practice = ? WHERE user_id = ?", ('Нет', callback_query.from_user.id))
            await bot.send_message(callback_query.from_user.id,
                                   'Чтобы ваше состояние оставалось всегда в норме, хотим предложить поддержку, содержащую в себе практики и упражнения для разгрузки, а также общие советы по поддержке. '
                                   '\nХотите попробовать?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                    InlineKeyboardButton('Да, можно попробовать', callback_data='agreement_mailing_help_by'),
                    InlineKeyboardButton('Нет, не хочу', callback_data='agreement_mailing_help_bn')))
        db_helpsys.commit()


async def agreement_mailing_help(callback_query: types.CallbackQuery, state: FSMContext):
    await help_system_agreement(user_id=callback_query.from_user.id)
    db_helpsys = sqlite3.connect('Databases/Help_system.db')
    cur_helpsys = db_helpsys.cursor()
    if callback_query.data[-2] == 'g':
        cur_helpsys.execute("UPDATE agreement SET state = ? WHERE user_id = ?", ('Хорошо', callback_query.from_user.id))
    elif callback_query.data[-2] == 'n':
        cur_helpsys.execute("UPDATE agreement SET state = ? WHERE user_id = ?",('Нормально', callback_query.from_user.id))
    else:
        cur_helpsys.execute("UPDATE agreement SET state = ? WHERE user_id = ?", ('Плохо', callback_query.from_user.id))
    db_helpsys.commit()
    if callback_query.data[-1] == 'y':
        cur_helpsys.execute("UPDATE agreement SET choice = ? WHERE user_id = ?", ('Да', callback_query.from_user.id))
        await bot.send_message(callback_query.from_user.id, 'Забота о своём психологическом здоровье - это важно! Вы делаете правильный выбор!'
                                                            '\nХорошего вам вечера!')
    else:
        cur_helpsys.execute("UPDATE agreement SET choice = ? WHERE user_id = ?", ('Нет', callback_query.from_user.id))
        await bot.send_message(callback_query.from_user.id,
                               'Очень жаль, что вам неинтересна тема заботы о своём психологическом здоровье(('
                               '\nХорошего вам вечера!')
    db_helpsys.commit()
    await state.set_state(FSM_classes.MultiDialog.menu)


def register_handlers_helpsystem(dp: Dispatcher):
    dp.register_callback_query_handler(try_practice, text=['try_practice_gy', 'try_practice_ny', 'try_practice_by', 'try_practice_gn', 'try_practice_nn', 'try_practice_bn'])
    dp.register_callback_query_handler(agreement_mailing_help, text=['agreement_mailing_help_gy', 'agreement_mailing_help_ny', 'agreement_mailing_help_by', 'agreement_mailing_help_gn', 'agreement_mailing_help_nn', 'agreement_mailing_help_bn'])
