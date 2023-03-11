import asyncio
import os
import random
import sqlite3
import sys
import time
from datetime import datetime, timedelta


from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from asyncio import exceptions
import aioschedule as schedule

from aiogram.utils.exceptions import BotBlocked

from Token import Token
from Databases import db_start, data_profile, affirmation

async def on_startup(_):
    await db_start()
    # asyncio.create_task(scheduler_sleep())

import FSM_classes
import Markups
import Practices
import Courses
import Tests
import Habit
import Specialists
from PsyTests import Psy_Weariness, Psy_selfefficacy
from PopTests import Pop_Control, Pop_Typeperson
from Habits import Sleep, Water, Reading, Body
from AllCourses import Anxiety

bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())

Anxiety.register_handlers_course_Anxiety(dp)
Psy_Weariness.register_handlers_Psy_Weariness(dp)
Psy_selfefficacy.register_handlers_Psy_selfefficacy(dp)
Pop_Control.register_handlers_Pop_Control(dp)
Pop_Typeperson.register_handlers_Pop_typeperson(dp)



@dp.message_handler(commands=['admin_mailing'], state='*', chat_id=417986886)
async def check_active_users(message: types.Message):
    await FSM_classes.Admin.mailing_all.set()
    await bot.send_message(message.from_user.id, text='Здравствуйте, босс! Пришлите то, что хотите разослать!', parse_mode='html')


@dp.message_handler(content_types=['photo'], state=FSM_classes.Admin.mailing_all)
async def mailing_photo(message: types.Message):
    await message.photo[-1].download(destination_file='mailing.jpg')
    db_user_blocked = sqlite3.connect('Databases/Data_users.db')
    cur_user_blocked = db_user_blocked.cursor()
    users = cur_user_blocked.execute('SELECT user_id FROM profile').fetchall()
    await FSM_classes.MultiDialog.menu.set()
    for user in range(len(users)):
        try:
            photo_mailing = open('mailing.jpg', 'rb')
            await bot.send_photo(chat_id=(users[user][0]), photo=photo_mailing, parse_mode='html')
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_user_blocked.execute('UPDATE profile SET active = "Нет" WHERE user_id = ?', (users[user][0],))
            db_user_blocked.commit()


@dp.message_handler(content_types=['text'], state=FSM_classes.Admin.mailing_all)
async def mailing_text(message: types.Message):
    db_user_blocked = sqlite3.connect('Databases/Data_users.db')
    cur_user_blocked = db_user_blocked.cursor()
    users = cur_user_blocked.execute('SELECT user_id FROM profile').fetchall()
    await FSM_classes.MultiDialog.menu.set()
    for user in range(len(users)):
        try:
            await bot.send_message(chat_id=(users[user][0]),
                                   text=message.text, parse_mode='html')
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_user_blocked.execute('UPDATE profile SET active = "Нет" WHERE user_id = ?', (users[user][0],))
            db_user_blocked.commit()



@dp.message_handler(commands=['start'], state='*')
async def welcome(message: types.Message):
    await data_profile(user_id=message.from_user.id, first_name=message.from_user.first_name,
                       username=message.from_user.username)
    await FSM_classes.MultiDialog.menu.set()
    Welcome_kb = InlineKeyboardMarkup()
    Welcome_kb.add(InlineKeyboardButton('Приятно познакомиться!', callback_data='Welcome_btn0'))
    mess = f'Здравствуйте 🖐, <b>{message.from_user.first_name}</b>! Рад, что вы заботитетсь о своем ментальном здоровье! ' \
           f'\nБот Reform - это цифровой помощник, к которому ты сможешь обратиться в случае возникновения стресса, тревоги или апатии, а самое главное для того, чтобы не допустить этого!' \
           f'\n\nОн поможет вам разобраться в проблеме и предоставит инструменты для её решения.' \
           f'\nВы сможете преодолеть любые преграды на вашем пути, а бот поможет вам советом и рекомендацией в трудную минуту!'
    await bot.send_message(message.from_user.id, mess, parse_mode='html', reply_markup=Welcome_kb)
    await log_users(message)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('Welcome_btn'), state=FSM_classes.MultiDialog.menu)
async def mailing(callback_query: types.CallbackQuery, state:FSMContext):
    if callback_query.data[-1] == '0':
        agree_mailing_kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Да, хочу попробовать', callback_data='Welcome_btny'),
                                                      InlineKeyboardButton('Нет, ни в коем случае', callback_data='Welcome_btnn'))
        await bot.send_message(callback_query.from_user.id, 'Хотите ли вы получать ежедневные мотивационные подборки и аффирмации для более эффективного взаимодействия с ботом?'
                                                            '\nОтписаться можно в любой момент',
                           parse_mode='html', reply_markup=agree_mailing_kb)
    if callback_query.data[-1] == 'y':
        await affirmation(user_id=callback_query.from_user.id, first_name=callback_query.from_user.first_name,
                           username=callback_query.from_user.username)
        enterIn = InlineKeyboardMarkup(resize_keyboard=True, row_width=1).add(
            InlineKeyboardButton('Начнём!', callback_data='Main_menu'))
        await bot.send_message(callback_query.from_user.id,
                               'Отлично! Теперь мы можем приступить к нашему с вами взаимодействию',
                               parse_mode='html', reply_markup=enterIn)
    if callback_query.data[-1] == 'n':
        enterIn = InlineKeyboardMarkup(resize_keyboard=True, row_width=1).add(
            InlineKeyboardButton('Продолжить!', callback_data='Main_menu'))
        await bot.send_message(callback_query.from_user.id,
                               'Очень жаль, что вы не хотите. Данные подборки созданы для того, чтобы повысить ваш эффект от взаимодействия с ботом!'
                               '\nЕсли вы передумаете, вы можете нажать /start и изменить свой выбор',
                               parse_mode='html', reply_markup=enterIn)


@dp.message_handler(commands=['main_menu'], state='*')
async def main_menu(message: types.Message, state: FSMContext):
    await FSM_classes.HabitSleep.none.set()
    await FSM_classes.MultiDialog.menu.set()
    await bot.send_message(message.from_user.id, 'Вы в главном меню! Не знаете, что делать дальше?'
                                                 '\n\n🧘‍♀️ Практики помогут вам разгрузиться после тяжёлого дня или успокоиться'
                                                 '\n📝 Пройдите тесты, чтобы определить актуальное состояние и выявить проблему'
                                                 '\n💪 Трекер привычек поможет внедрить и поддерживать полезные навыки'
                                                 '\n🎬 Проходите курсы, узнавайте лучше себя, что поможет вам справиться с жизненными трудностями'
                                                 '\n💬 Также вы можете обсудить проблему и получить рекомендации от специалиста'
                                                 '\nВыберите, что вас интересует',
                           parse_mode='html', reply_markup=Markups.main_kb)
    await log_users(message)



@dp.message_handler(commands=['practices'], state='*')
async def practices(message: types.Message):
    await FSM_classes.MultiDialog.practices.set()
    await Practices.type_practices(message)


@dp.message_handler(commands=['test'], state='*')
async def test(message: types.message, state: FSMContext):
    await FSM_classes.MultiDialog.tests.set()
    await Tests.pretest(message, state)
    await log_users(message)



@dp.message_handler(commands=['courses'], state='*')
async def courses(message: types.Message, state: FSMContext):
    await FSM_classes.MultiDialog.courses.set()
    await Courses.precourse(message, state)
    await log_users(message)



@dp.message_handler(commands=['contacts'], state='*')
async def contacts(message: types.Message):
    await bot.send_message(message.from_user.id, 'Здравствуйте! '
                                                 'Меня зовут Reform. Я оказываю психологическую поддержку.'
                                                 'Мои возможности пока что ограничены, но меня совершенствуют с каждым днём.'
                                                 'Если у вас есть вопросы или вы обнаружили ошибку, вы можете обратиться к @APecherkin.',
                           parse_mode='html', reply_markup=Markups.cont)
    await log_users(message)



@dp.callback_query_handler(lambda c: c.data and c.data.startswith('fullversion'), state=FSM_classes.MultiDialog)
async def fullversion_callback(callback_query: types.CallbackQuery, state:FSMContext):
    await bot.send_message(callback_query.from_user.id, 'Полный доступ доступен в платной версии.'
                                                     '\nВ платной версии:'
                                                     '❇️25 медитаций'
                                                     '❇️10 дыхательных практик'
                                                     '❇️Таймер Помодоро'
                                                     '❇️Система ежедневных напоминаний и мотиваций'
                                                     '❇️Рекомендации по сну, питанию и отдыху от ведущих специалистов'
                                                     '\n\nОформить подписку за 499 рублей в месяц?', parse_mode='html')



@dp.callback_query_handler(lambda c: c.data and c.data.startswith('Main_menu'), state='*')
async def main_menu_callback(callback_query: types.CallbackQuery, state:FSMContext):
    await FSM_classes.HabitSleep.none.set()
    await FSM_classes.MultiDialog.menu.set()
    await bot.send_message(callback_query.from_user.id, 'Вы в главном меню. Не знаете что делать дальше?'
                                                 '\n\n🧘‍♀️ Практики помогут вам разгрузиться после тяжёлого дня или успокоиться'
                                                 '\n📝 Пройдите тесты, чтобы определить актуальное состояние и выявить проблему'
                                                 '\n💪 Трекер привычек поможет внедрить и поддерживать полезные навыки'
                                                 '\n🎬 Проходите курсы, узнавайте лучше себя, что поможет вам справиться с жизненными трудностями'
                                                 '\n💬 Также вы можете обсудить проблему и получить рекомендации от специалиста'
                                                 '\nВыберите, что вас интересует',
                           parse_mode='html', reply_markup=Markups.main_kb)



@dp.message_handler(state=FSM_classes.MultiDialog.practices)
async def reply_practices(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await main_menu(message,state)
    await Practices.allreply_practices(message)
    await log_users(message)



@dp.message_handler(state=FSM_classes.MultiDialog.tests)
async def reply_tests(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await FSM_classes.MultiDialog.menu.set()
        await main_menu(message, state)
    await Tests.type_test(message, state)
    await log_users(message)



@dp.message_handler(state=(FSM_classes.MultiDialog.test_weariness or FSM_classes.MultiDialog.test_control or FSM_classes.MultiDialog.test_selfefficacy or FSM_classes.MultiDialog.test_typeperson))
async def reply_alltests(message: types.Message, state: FSMContext):
    if message.text == 'Прервать тест и выйти в меню':
        await FSM_classes.MultiDialog.menu.set()
        await main_menu(message, state)
        await log_users(message)


@dp.message_handler(state=FSM_classes.MultiDialog.courses)
async def reply_courses(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в меню':
        await main_menu(message, state)
    await Courses.type_course(message, state)
    await log_users(message)


@dp.message_handler(state=FSM_classes.MultiDialog.course_anxiety)
async def reply_anxiety(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в меню':
        await FSM_classes.MultiDialog.menu.set()
        await main_menu(message, state)
        await log_users(message)


@dp.callback_query_handler(state=FSM_classes.MultiDialog.course_anxiety)
async def reply_anxiety(callback_query: types.CallbackQuery, state: FSMContext):
    await Anxiety.Course_Anxiety(callback_query, state)

@dp.message_handler(state=FSM_classes.MultiDialog.habits)
async def reply_habits(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await main_menu(message, state)
    await Habit.choose_habit(message, state)
    await log_users(message)


@dp.message_handler(state=FSM_classes.HabitSleep.choose_action)
async def reply_habit_sleep(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await main_menu(message, state)
    await Sleep.choose_habit_action(message, state)
    await log_users(message)


@dp.message_handler(state=FSM_classes.HabitSleep.choose_wakeup)
async def reply_habit_sleep(message: types.Message, state: FSMContext):
    await Sleep.choose_habit_sleep_wakeup(message, state)
    await log_users(message)



@dp.message_handler(state=FSM_classes.HabitSleep.choose_bedtime)
async def reply_habit_sleep(message: types.Message, state: FSMContext):
    await Sleep.choose_habit_sleep_bedtime(message, state)
    await log_users(message)




@dp.message_handler(state=FSM_classes.MultiDialog.specialist)
async def reply_specialist(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await main_menu(message, state)
    await Specialists.choose_specialist(message, state)
    await log_users(message)

@dp.message_handler(state='*')
async def reply_all(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await main_menu(message, state)
        await log_users(message)

    if message.text == '🧘‍♀️ Практики':
        await FSM_classes.MultiDialog.practices.set()
        await Practices.type_practices(message)
        await log_users(message)

    if message.text == '📝 Тесты':
        await FSM_classes.MultiDialog.tests.set()
        await Tests.pretest(message, state)
        await log_users(message)

    if message.text == '💪 Мои привычки':
        await FSM_classes.MultiDialog.habits.set()
        await Habit.prehabits(message, state)
        await log_users(message)

    if message.text == '🎓 Курсы':
        await FSM_classes.MultiDialog.courses.set()
        await Courses.precourse(message, state)
        await log_users(message)

    if message.text == '💬 Обсудить проблему':
        await FSM_classes.MultiDialog.specialist.set()
        await Specialists.choose_specialist(message, state)
        await log_users(message)

    if message.text == '📥 Контакты':
        await contacts(message)
        await log_users(message)

    if message.text == 'Что ты умеешь?':
        back = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Вернуться в главное меню')
        back.add(btn1)
        await bot.send_message(message.from_user.id,
                               'Я могу оценить ваше состояние и подобрать индивидуальные упражнения, которые помогут справиться с психологическими проблемами. '
                               '\n\nВыберите раздел с практиками, если хотите разгрузиться или чувствуете себя не важно. '
                               '\nВ разделе с курсами вы можете углубиться в интересующую вас проблему и решить её с помощью специальных методик разработанных специалистами.'
                               '\nВ разделе музыка вы можете найти для себя подходящую мелодию и расслабиться'
                               '\nТакже, если вы не знаете в чём проблема, но чувствуете себя не очень, то можете пройти тесты и лучше понять себя'
                               '\n\n Приятного использования и жизни в гармонии со своим ментальным здоровьем!',
                               parse_mode='html', reply_markup=back)
        await log_users(message)





@dp.channel_post_handler(content_types=['text'])
async def affirmation_mailing_text(message: types.Message):
    db_data = sqlite3.connect('Databases/Data_users.db')
    cur_data = db_data.cursor()
    users_affirmation = cur_data.execute('SELECT user_id FROM affirmation').fetchall()
    for user_miling in range(len(users_affirmation)):
        try:
            await bot.send_message(chat_id=(users_affirmation[user_miling][0]),
                               text=message.text, parse_mode='html')
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_data.execute('UPDATE affirmation SET user_id = 0 WHERE user_id = ?',
                             (users_affirmation[user_miling][0],))
            db_data.commit()
    cur_data.execute('DELETE FROM affirmation WHERE user_id = ?', (int(0),))
    db_data.commit()


@dp.channel_post_handler(content_types=['photo'])
async def affirmation_mailing_photo(message: types.Message):
    await message.photo[-1].download(destination_file='affirmation.jpg')
    db_data = sqlite3.connect('Databases/Data_users.db')
    cur_data = db_data.cursor()
    users_affirmation = cur_data.execute('SELECT user_id FROM affirmation').fetchall()
    await asyncio.sleep(1)
    for user_miling in range(len(users_affirmation)):
        try:
            photo = open('affirmation.jpg', 'rb')
            await bot.send_photo(chat_id=(users_affirmation[user_miling][0]),
                                   photo=photo, parse_mode='html')
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_data.execute('UPDATE affirmation SET user_id = 0 WHERE user_id = ?', (users_affirmation[user_miling][0],))
            db_data.commit()
    cur_data.execute('DELETE FROM affirmation WHERE user_id = ?', (int(0),))
    db_data.commit()



async def scheduler_sleep_message_wakeup():
    db_scheduler_sleep = sqlite3.connect('Databases/Current_habits.db')
    cur_scheduler = db_scheduler_sleep.cursor()
    now = datetime.utcnow() + timedelta(hours=3, minutes=0)
    users_wakeup = cur_scheduler.execute('SELECT user_id FROM sleep WHERE wakeup = ?', (now.strftime('%H:%M'),)).fetchall()
    for user_wakeup in range(len(users_wakeup)):
        try:
            await bot.send_message(chat_id=users_wakeup[user_wakeup][0], text='Пора вставать! '
                                                      '\nНачинать никогда не поздно! А всё начинается с небольших изменений!')
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_scheduler.execute('UPDATE sleep SET user_id = 0 WHERE user_id = ?', (users_wakeup[user_wakeup][0],))
            db_scheduler_sleep.commit()
    cur_scheduler.execute('DELETE FROM sleep WHERE user_id = ?', (int(0),))
    db_scheduler_sleep.commit()

async def scheduler_sleep_message_bedtime():
    db_scheduler_sleep = sqlite3.connect('Databases/Current_habits.db')
    cur_scheduler = db_scheduler_sleep.cursor()
    now = datetime.utcnow() + timedelta(hours=3, minutes=0)
    users_bedtime = cur_scheduler.execute('SELECT user_id FROM sleep WHERE bedtime = ?', (now.strftime('%H:%M'),)).fetchall()
    for user_bedtime in range(len(users_bedtime)):
        try:
            await bot.send_message(chat_id=users_bedtime[user_bedtime][0], text='Вы просили напомнить, что вам пора ложиться спать!'
                                                            '\nЗавтра вас ждёт отличный день! '
                                                            '\nПомните, великое начинется с малого!')
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_scheduler.execute('UPDATE sleep SET user_id = 0 WHERE user_id = ?', (users_bedtime[user_bedtime][0],))
            db_scheduler_sleep.commit()
    cur_scheduler.execute('DELETE FROM sleep WHERE user_id = ?', (int(0),))
    db_scheduler_sleep.commit()

async def scheduler_sleep():
    schedule.every(1).minute.do(scheduler_sleep_message_wakeup)
    schedule.every(1).minute.do(scheduler_sleep_message_bedtime)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(10)

async def log_users(message: types.Message):
    now = datetime.now()
    botlogfile = open('LogsBot', 'a')
    print(now.strftime('%d-%m-%Y %H:%M'), ' Пользователь - ' + message.from_user.first_name, message.from_user.id, 'Написал - ' + message.text, file=botlogfile)
    botlogfile.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler_sleep())
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)

