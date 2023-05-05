import asyncio
import sqlite3
import time
import aioschedule
import pandas as pd


from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime, timedelta

from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())

from Databases import prehabit_water_db
import Markups
import FSM_classes


async def habit_water(message: types.message, state: FSMContext):
    await prehabit_water_db(user_id=message.from_user.id, username=message.from_user.username)
    await bot.send_message(message.from_user.id, 'Хотите настроить привычку или удалить её?', reply_markup=Markups.tune_habit)
    await FSM_classes.HabitWater.choose_action.set()

async def choose_habit_action(message: types.message, state: FSMContext):

    if message.text == 'Настроить привычку':
        await bot.send_message(message.from_user.id, 'Напишите сколько раз в день вы хотели бы пить воду.'
                                                     '\nНорма воды в день - 2 литра, выберите на сколько порций эту норму разделить (от 2 до 8)')
        await FSM_classes.HabitWater.choose_amount_of_portion.set()

    if message.text == 'Удалить привычку':
        db_waterHabit = sqlite3.connect('Databases/Current_habits.db')
        cur_waterHabit = db_waterHabit.cursor()
        habbit = cur_waterHabit.execute('SELECT interval FROM water WHERE user_id = ? AND interval != 0',(message.from_user.id,)).fetchone()

        if habbit is not None:
            cur_waterHabit.execute('DELETE FROM water WHERE user_id = ?', (message.from_user.id,))
            await bot.send_message(message.from_user.id, 'Ваша привычка успешно удалена!')
            db_waterHabit.commit()
        else:
            await bot.send_message(message.from_user.id, 'У вас не настроена данная привычка!')


async def choose_habit_water_portions(message: types.message, state: FSMContext):
    db_waterHabit = sqlite3.connect('Databases/Current_habits.db')
    cur_waterHabit = db_waterHabit.cursor()
    if int(message.text) in range(2,9):
        cur_waterHabit.execute("UPDATE water SET amountOfPortions = ? WHERE user_id = ?", (int(message.text), message.from_user.id))

        await bot.send_message(message.from_user.id, 'Вы выбрали колличество приёмов воды: ' + message.text)
        await bot.send_message(message.from_user.id, 'Хотите работать над приемом воды по будням или выходным?',reply_markup=Markups.chooseScheduleWater)
        interval = int(round((1380-600)/int(message.text)))
        cur_waterHabit.execute("UPDATE water SET interval = ? WHERE user_id = ?",
                                      (interval, message.from_user.id))
        db_waterHabit.commit()
        await FSM_classes.HabitWater.choose_schedule.set()
    else:
        await bot.send_message(message.from_user.id,
                               'Ошибка! Напишите колличество порций одной цифрой от 2 до 8!')
        await FSM_classes.HabitWater.choose_amount_of_portion.set()



async def choose_habit_water_schedule(message: types.message, state: FSMContext):
    db_waterHabit = sqlite3.connect('Databases/Current_habits.db')
    cur_waterHabit = db_waterHabit.cursor()
    if message.text == 'Будние':
        cur_waterHabit.execute("UPDATE water SET schedule = ? WHERE user_id = ?",('weekdays', message.from_user.id))
        db_waterHabit.commit()
    elif message.text == 'Выходные':
        cur_waterHabit.execute("UPDATE water SET schedule = ? WHERE user_id = ?",('weekends', message.from_user.id))
        db_waterHabit.commit()
    elif message.text == 'Вся неделя':
        cur_waterHabit.execute("UPDATE water SET schedule = ? WHERE user_id = ?",('both', message.from_user.id))
        db_waterHabit.commit()
    else:
        await bot.send_message(message.from_user.id,
                               'Ошибка при вводе данных',reply_markup=Markups.chooseScheduleWater)
        await FSM_classes.HabitWater.choose_schedule.set()
    await bot.send_message(message.from_user.id,
                           'Вы успешно начали работу над приёмом воды!', reply_markup=Markups.backHabitRe)
    await FSM_classes.MultiDialog.menu.set()

async def answer_water_schedule(callback_query: types.CallbackQuery, state: FSMContext):
    db_waterHabit = sqlite3.connect('Databases/Current_habits.db')
    cur_waterHabit = db_waterHabit.cursor()
    today = datetime.today()
    tableName = 'date_' + str(today)[0:10].replace('-','')
    db_mark = callback_query.data[-1]
    cur_waterHabit.execute(f'ALTER TABLE water ADD COLUMN {tableName} TEXT')
    cur_waterHabit.execute(f'UPDATE water SET {tableName} = ? WHERE user_id = ?', (db_mark,callback_query.from_user.id))
    db_waterHabit.commit()

async def createExcelFile(startDate,endDate,users):
    db_waterHabit = sqlite3.connect('Databases/Current_habits.db')
    cur_waterHabit = db_waterHabit.cursor()
    df = pd.DataFrame(columns=['user_id'])
    date_start = datetime.strptime(startDate, "%Y%m%d")
    date_end = datetime.strptime(endDate, "%Y%m%d")
    days = []
    current_date = date_start

    while current_date <= date_end:
        days.append(str(current_date.date()).replace('-', ''))
        current_date += timedelta(days=1)
    for i, user in enumerate(users):
        df.loc[i, 'user_id'] = user
        for j, day in enumerate(days):
            cur_waterHabit.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name='water' AND sql LIKE '%date_{day}%'")
            if cur_waterHabit.fetchone() is not None:
                answer = cur_waterHabit.execute(f"SELECT date_{day} FROM water WHERE user_id = ?", (user,)).fetchone()
                answer = answer[0]
            else:
                answer = 'No data'
            date_obj = datetime.strptime(day, '%Y%m%d')
            date_formatted = date_obj.strftime('%d:%m:%Y')
            df.loc[i, str(date_formatted)] = answer if answer else None
    db_waterHabit.close()
    df.to_excel('userData.xlsx', index=False)

