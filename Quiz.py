import asyncio
import os
import sqlite3

import contourpy.util.data
from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ReplyKeyboardRemove
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked
from Storage import storage


from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=storage)

import FSM_classes


async def high_workload_preview(message: types.Message, state: FSMContext):
    db_quiz_workload = sqlite3.connect('Databases/Quiz.db')
    cur_quiz_workload = db_quiz_workload.cursor()
    if message.text == 'Начать':
        await bot.send_message(message.from_user.id, 'Отлично, тогда приступим!')
        await asyncio.sleep(1)
        cur_quiz_workload.execute("UPDATE workload SET agree = ? WHERE user_id = ?",
                            ('Да', message.from_user.id))
        await bot.send_message(message.from_user.id, '1) Есть ли какие-либо ситуации или задачи, которые вызывают у вас <b>тревогу или неприятные эмоции</b> на работе?', parse_mode='html',
                               reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton('Да'), KeyboardButton('Нет')))
        await state.set_state(FSM_classes.Quiz.high_workload_1)
    elif message.text == 'Нет, не хочу его проходить':
        await bot.send_message(message.from_user.id, 'Очень жаль, что вы не хотите поделиться('
                                                     '\nЭто нужно для того, чтобы лучше понять ваше состояние и подготовить более персонализированные рекомендации')
        cur_quiz_workload.execute("UPDATE workload SET agree = ? WHERE user_id = ?",
                                  ('Нет', message.from_user.id))
        await bot.send_message(message.from_user.id, 'Пожалуйста, напишите, с чем связано ваше решение, это поможет нам стать лучше!')
        await state.set_state(FSM_classes.Quiz.high_workload_cause_not)
    db_quiz_workload.commit()


async def high_workload_cause_not(message: types.Message, state: FSMContext):
    db_quiz_workload = sqlite3.connect('Databases/Quiz.db')
    cur_quiz_workload = db_quiz_workload.cursor()
    cur_quiz_workload.execute("UPDATE workload SET cause = ? WHERE user_id = ?",
                              (message.text, message.from_user.id))
    await bot.send_message(message.from_user.id, 'Спасибо, что поделились! Я обязательно передам ваш ответ команде создателям Reform!')
    await state.set_state(FSM_classes.MultiDialog.menu)


async def high_workload_1(message:types.Message, state:FSMContext):
    db_quiz_workload = sqlite3.connect('Databases/Quiz.db')
    cur_quiz_workload = db_quiz_workload.cursor()
    cur_quiz_workload.execute("UPDATE workload SET answer_1 = ? WHERE user_id = ?",
                              (message.text, message.from_user.id))
    if message.text == 'Да':
        await bot.send_message(message.from_user.id, 'Пожалуйста опишите данные ситуации', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FSM_classes.Quiz.high_workload_1_details)
    elif message.text == 'Нет':
        await bot.send_message(message.from_user.id, '2) Есть ли какие-либо проекты или задачи, с которыми у вас <b>возникли сложности</b>?', parse_mode='html',
                               reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton('Да'), KeyboardButton('Нет')))
        await state.set_state(FSM_classes.Quiz.high_workload_2)


async def high_workload_1_details(message:types.Message, state:FSMContext):
    db_quiz_workload = sqlite3.connect('Databases/Quiz.db')
    cur_quiz_workload = db_quiz_workload.cursor()
    cur_quiz_workload.execute("UPDATE workload SET answer_1_details = ? WHERE user_id = ?",
                              (message.text, message.from_user.id))
    await bot.send_message(message.from_user.id,
                           '2) Есть ли какие-либо проекты или задачи, с которыми у вас <b>возникли сложности</b>?',
                           parse_mode='html',
                           reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton('Да'),
                                                                                                   KeyboardButton(
                                                                                                       'Нет')))
    await state.set_state(FSM_classes.Quiz.high_workload_2)


async def high_workload_2(message:types.Message, state:FSMContext):
    db_quiz_workload = sqlite3.connect('Databases/Quiz.db')
    cur_quiz_workload = db_quiz_workload.cursor()
    cur_quiz_workload.execute("UPDATE workload SET answer_2 = ? WHERE user_id = ?",
                              (message.text, message.from_user.id))
    if message.text == 'Да':
        await bot.send_message(message.from_user.id, 'Пожалуйста опишите данные ситуации', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FSM_classes.Quiz.high_workload_2_details)
    elif message.text == 'Нет':
        await bot.send_message(message.from_user.id, '3) Как часто вы испытываете физическую усталость или недомогание?', parse_mode='html',
                               reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(KeyboardButton('Часто'), KeyboardButton('Иногда'), KeyboardButton('Редко')))
        await state.set_state(FSM_classes.Quiz.high_workload_3)


async def high_workload_2_details(message:types.Message, state:FSMContext):
    db_quiz_workload = sqlite3.connect('Databases/Quiz.db')
    cur_quiz_workload = db_quiz_workload.cursor()
    cur_quiz_workload.execute("UPDATE workload SET answer_2_details = ? WHERE user_id = ?",
                              (message.text, message.from_user.id))
    await bot.send_message(message.from_user.id,
                           '3) Как часто вы испытываете физическую усталость или недомогание?', parse_mode='html',
                               reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(KeyboardButton('Часто'), KeyboardButton('Иногда'), KeyboardButton('Редко')))
    await state.set_state(FSM_classes.Quiz.high_workload_3)


async def high_workload_3(message:types.Message, state:FSMContext):
    db_quiz_workload = sqlite3.connect('Databases/Quiz.db')
    cur_quiz_workload = db_quiz_workload.cursor()
    cur_quiz_workload.execute("UPDATE workload SET answer_3 = ? WHERE user_id = ?",
                              (message.text, message.from_user.id))
    await bot.send_message(message.from_user.id, '4) Уделяете ли вы внимание физической активности и здоровому питанию?', parse_mode='html',
                           reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(KeyboardButton('Да'), KeyboardButton('Стараюсь'), KeyboardButton('Нет')))
    await state.set_state(FSM_classes.Quiz.high_workload_4)


async def high_workload_4(message:types.Message, state:FSMContext):
    db_quiz_workload = sqlite3.connect('Databases/Quiz.db')
    cur_quiz_workload = db_quiz_workload.cursor()
    cur_quiz_workload.execute("UPDATE workload SET answer_4 = ? WHERE user_id = ?",
                              (message.text, message.from_user.id))
    await bot.send_message(message.from_user.id, '5) Есть ли у вас внутренний диссонанс или несоответствие между вашими ценностями и текущей работой?', parse_mode='html',
                           reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton('Да'), KeyboardButton('Нет')))
    await state.set_state(FSM_classes.Quiz.high_workload_5)


async def high_workload_5(message:types.Message, state:FSMContext):
    db_quiz_workload = sqlite3.connect('Databases/Quiz.db')
    cur_quiz_workload = db_quiz_workload.cursor()
    cur_quiz_workload.execute("UPDATE workload SET answer_5 = ? WHERE user_id = ?",
                              (message.text, message.from_user.id))
    await bot.send_message(message.from_user.id, '6) Как бы вы оценили свое общее эмоциональное состояние на данный момент по шкале 1 до 10?', parse_mode='html',
                           reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, row_width=5).add(KeyboardButton('1'), KeyboardButton('2'), KeyboardButton('3'), KeyboardButton('4'), KeyboardButton('5'), KeyboardButton('6'), KeyboardButton('7'), KeyboardButton('8'), KeyboardButton('9'), KeyboardButton('10')))
    await state.set_state(FSM_classes.Quiz.high_workload_6)


async def high_workload_6(message:types.Message, state:FSMContext):
    db_quiz_workload = sqlite3.connect('Databases/Quiz.db')
    cur_quiz_workload = db_quiz_workload.cursor()
    cur_quiz_workload.execute("UPDATE workload SET answer_6 = ? WHERE user_id = ?",
                              (message.text, message.from_user.id))
    await bot.send_message(message.from_user.id, '7) Можете ли вы описать, что вызывает у вас негативные эмоции?', parse_mode='html',
                           reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSM_classes.Quiz.high_workload_7)


async def high_workload_7(message:types.Message, state:FSMContext):
    db_quiz_workload = sqlite3.connect('Databases/Quiz.db')
    cur_quiz_workload = db_quiz_workload.cursor()
    cur_quiz_workload.execute("UPDATE workload SET answer_7 = ? WHERE user_id = ?",
                              (message.text, message.from_user.id))
    await bot.send_message(message.from_user.id, '8) Чувствуете ли вы воодушевление при взаимодействии с коллегами?', parse_mode='html',
                           reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton('Да'), KeyboardButton('Нет')))
    await state.set_state(FSM_classes.Quiz.high_workload_8)


async def high_workload_8(message:types.Message, state:FSMContext):
    db_quiz_workload = sqlite3.connect('Databases/Quiz.db')
    cur_quiz_workload = db_quiz_workload.cursor()
    cur_quiz_workload.execute("UPDATE workload SET answer_8 = ? WHERE user_id = ?",
                              (message.text, message.from_user.id))
    await bot.send_message(message.from_user.id, '9) Чувствуете ли вы, что ваш труд приносит пользу людям и/или положительно влияет на них?', parse_mode='html',
                           reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton('Да'), KeyboardButton('Нет')))
    await state.set_state(FSM_classes.Quiz.high_workload_9)


async def high_workload_9(message:types.Message, state:FSMContext):
    db_quiz_workload = sqlite3.connect('Databases/Quiz.db')
    cur_quiz_workload = db_quiz_workload.cursor()
    cur_quiz_workload.execute("UPDATE workload SET answer_9 = ? WHERE user_id = ?",
                              (message.text, message.from_user.id))
    await bot.send_message(message.from_user.id, 'Спасибо за ваши ответы! '
                                                 '\nОсновываясь на них, я постараюсь подобрать рекомендации, практики и упражнения, которые вам помогут! '
                                                 '\nСкоро к вам вернусь! До встречи!',
                           reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSM_classes.MultiDialog.menu)


def register_handlers_quiz(dp: Dispatcher):
    dp.register_message_handler(high_workload_preview, state=FSM_classes.Quiz.high_workload_pre)
    dp.register_message_handler(high_workload_1, state=FSM_classes.Quiz.high_workload_1)
    dp.register_message_handler(high_workload_1_details, state=FSM_classes.Quiz.high_workload_1_details)
    dp.register_message_handler(high_workload_2, state=FSM_classes.Quiz.high_workload_2)
    dp.register_message_handler(high_workload_2_details, state=FSM_classes.Quiz.high_workload_2_details)
    dp.register_message_handler(high_workload_3, state=FSM_classes.Quiz.high_workload_3)
    dp.register_message_handler(high_workload_4, state=FSM_classes.Quiz.high_workload_4)
    dp.register_message_handler(high_workload_5, state=FSM_classes.Quiz.high_workload_5)
    dp.register_message_handler(high_workload_6, state=FSM_classes.Quiz.high_workload_6)
    dp.register_message_handler(high_workload_7, state=FSM_classes.Quiz.high_workload_7)
    dp.register_message_handler(high_workload_8, state=FSM_classes.Quiz.high_workload_8)
    dp.register_message_handler(high_workload_9, state=FSM_classes.Quiz.high_workload_9)
