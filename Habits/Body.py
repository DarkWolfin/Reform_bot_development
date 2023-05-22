import pickle
from Token import Token
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram import Bot, types, Dispatcher
import FSM_classes
import Markups
from Databases import habit_remind_db, habit_answerRemind_db
import asyncio
import sqlite3
import time
import aioschedule
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time
from datetime import datetime, timedelta
scheduler = AsyncIOScheduler()


bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())


async def habit_remind(message: types.message, state: FSMContext):
    await habit_remind_db(user_id=message.from_user.id, username=message.from_user.username)
    await habit_answerRemind_db(user_id=message.from_user.id, username=message.from_user.username)
    await bot.send_message(message.from_user.id, 'Что вы хотите сделать?', reply_markup=Markups.time_remind)
    await FSM_classes.HabitRemind.choose_action.set()


async def choose_actionhab(message: types.message, state: FSMContext):

    if message.text == 'Добавить напоминание':
        await bot.send_message(message.from_user.id, 'Выберите дни недели', reply_markup=Markups.day_remind)
        await FSM_classes.HabitRemind.choose_day.set()
    if message.text == 'Удалить напоминание':
        db_remind = sqlite3.connect('Databases/Current_habits.db')
        cur_remind = db_remind.cursor()
        user = cur_remind.execute(
            'SELECT user_id FROM remind WHERE user_id = ?', (message.from_user.id,))
        if user.fetchone() is None:
            await bot.send_message(message.from_user.id, 'У вас нет активных напоминаний')

        else:
            cur_remind.execute(
                "DELETE FROM remind WHERE user_id = ?", (
                    message.from_user.id,))
            db_remind.commit()
            await bot.send_message(message.from_user.id, 'Напоминание успешно удалено!')


async def habbit_choose_day(message: types.message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Выберите дни недели', reply_markup=Markups.day_remind)
    await FSM_classes.HabitRemind.choose_day.set()


async def habbit_choose_time(message: types.message, state: FSMContext):
    db_remind = sqlite3.connect('Databases/Current_habits.db')

    cur_remind = db_remind.cursor()
    global timehab
    timehab = message.text.split(':')
    if len(timehab) == 2:
        if timehab[0].isdigit() and timehab[1].isdigit():
            if int(timehab[0]) in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] and int(timehab[1]) in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]:
                cur_remind.execute(
                    "UPDATE remind SET time = ? WHERE user_id = ?", (
                        message.text, message.from_user.id))
                db_remind.commit()
                if int(timehab[1]) > 29:
                    timehab[0] = int(timehab[0]) + 1
                    timehab[1] = int(timehab[1]) - 30
                    if len(str(timehab[0])) < 2:
                        timehab[0] = '0' + str(timehab[0])
                    if len(str(timehab[1])) < 2:
                        timehab[1] = '0' + str(timehab[1])
                else:
                    timehab[1] = int(timehab[1]) + 30
                cur_remind.execute(
                    "UPDATE remind SET timeRemind = ? WHERE user_id = ?", (str(timehab[0])+':'+str(timehab[1]), message.from_user.id))
                db_remind.commit()
                await bot.send_message(message.from_user.id, 'Время успешно добавлено!')
            else:
                bot.send_message(message.from_user.id, "no")
                await FSM_classes.HabitRemind.choose_time.set()
        else:
            bot.send_message(message.from_user.id, "no")
            await FSM_classes.HabitRemind.choose_time.set()
    else:
        bot.send_message(message.from_user.id, "no")
        await FSM_classes.HabitRemind.choose_time.set()
    await bot.send_message(message.from_user.id, 'Выберите файл для напоминания', reply_markup=Markups.data_choose)
    await FSM_classes.HabitRemind.choose_data.set()


async def data_remind(message: types.Message, state: FSMContext):
    if message.text == 'Фото':
        await bot.send_message(message.from_user.id, 'Отправьте боту фотографию')
        await FSM_classes.HabitRemind.data_photo.set()
        db_remind = sqlite3.connect('Databases/Current_habits.db')
        cur_remind = db_remind.cursor()
        cur_remind.execute(
            "UPDATE remind SET type = ? WHERE user_id = ?", ('photo', message.from_user.id))
        db_remind.commit()

    if message.text == 'Видео':
        await bot.send_message(message.from_user.id, 'Отправьте боту видео')
        await FSM_classes.HabitRemind.data_video.set()
        db_remind = sqlite3.connect('Databases/Current_habits.db')
        cur_remind = db_remind.cursor()
        cur_remind.execute(
            "UPDATE remind SET type = ? WHERE user_id = ?", ('video', message.from_user.id))
        db_remind.commit()

    if message.text == 'Аудио':
        await bot.send_message(message.from_user.id, 'Отправьте боту аудио')
        await FSM_classes.HabitRemind.data_audio.set()
        db_remind = sqlite3.connect('Databases/Current_habits.db')
        cur_remind = db_remind.cursor()
        cur_remind.execute(
            "UPDATE remind SET type = ? WHERE user_id = ?", ('audio', message.from_user.id))
        db_remind.commit()

    if message.text == 'Текст':
        await bot.send_message(message.from_user.id, 'Отправьте боту текст')
        await FSM_classes.HabitRemind.data_text.set()
        db_remind = sqlite3.connect('Databases/Current_habits.db')
        cur_remind = db_remind.cursor()
        cur_remind.execute(
            "UPDATE remind SET type = ? WHERE user_id = ?", ('text', message.from_user.id))
        db_remind.commit()
