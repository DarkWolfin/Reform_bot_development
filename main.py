import os
import chats_id
from PsyTests import Psy_Weariness, Psy_selfefficacy
from AllCourses import Anxiety
from Habits import Sleep, Water, Reading, Body
from PopTests import Pop_Control, Pop_Typeperson
from PsyTests import Psy_Weariness, Psy_selfefficacy, Psy_stress
import Specialists
import Habit
import Tests
import Courses
import Practices
import Markups
import FSM_classes
import asyncio
import sqlite3
from datetime import datetime, timedelta
import admin_commands
import quick_help
import Specialists

from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aioschedule as schedule

from aiogram.utils.exceptions import BotBlocked, BotKicked

from Token import Token
from Database import db_start, data_profile, affirmation, data_feedback, pre_points_test_weariness, \
    points_test_weariness, \
    pre_answers_test_weariness, set_user_token, get_all_user_ids, save_user_action, data_FB_marathon, NEW_affirmation


async def on_startup(_):
    await db_start()


bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())


Specialists.register_handlers_specialist(dp)
quick_help.register_handlers_quick_help(dp)
Pop_Control.register_handlers_Pop_Control(dp)
Pop_Typeperson.register_handlers_Pop_typeperson(dp)

Psy_selfefficacy.register_handlers_Psy_selfefficacy(dp)
Psy_stress.register_handlers_Psy_stress(dp)
Psy_Weariness.register_handlers_Psy_Weariness(dp)


Token_Raiff = ['RCS1', 'RCS2', 'RCS3', 'RCS4', 'RCS5', 'RCS6', 'RCS7', 'RCS8', 'RCS9', 'RCS10', 'RCS11', 'RCS12', 'RCS13',
               'RCS14', 'RCS15', 'RCS16', 'RCS17', 'RCS18', 'RCS19', 'RCS20', 'RCS21', 'RCS22', 'RCS23', 'RCS24', 'RCS25', 'RCS26',
               'SME1', 'SME2', 'SME3', 'SME4', 'SME5', 'SME6', 'SME7', 'SME8', 'SME9', 'SME10', 'SME11', 'SME12', 'SME13', 'SME14', 'SME15',
               'PREM1', 'PREM2', 'PREM3', 'PREM4', 'PREM5', 'PREM6', 'PREM7', 'PREM8', 'PREM9',
               'TEST1', 'TEST2', 'TEST3', 'TEST4', 'TEST5', 'TEST00', 'TEST000',
               'admin']


@dp.message_handler(commands=['start'], state='*')
async def welcome(message: types.Message):
    await data_profile(user_id=message.from_user.id, first_name=message.from_user.first_name,
                       username=message.from_user.username)
    await FSM_classes.MultiDialog.getToken.set()
    mess = f'Здравствуйте 🖐, <b>{message.from_user.first_name}</b>! Рад, что вы заботитетсь о своем ментальном здоровье! ' \
           f'\nБот Reform - это цифровой помощник, к которому вы сможете обратиться в случае возникновения стресса, тревоги или апатии, а самое главное для того, чтобы не допустить этого!' \
           f'\n\nОн поможет вам разобраться в проблеме и предоставит инструменты для её решения.' \
           f'\nВы сможете преодолеть любые преграды на вашем пути, а бот поможет вам советом и рекомендацией в трудную минуту!'
    await bot.send_message(message.from_user.id, mess, parse_mode='html')
    await bot.send_message(message.from_user.id,
                           "Пожалуйста введите ваш личный токен доступа, присвоенный вам \nНаш бот не в открытом доступе",
                           parse_mode='html')
    await FSM_classes.MultiDialog.setToken.set()

    await log_users(message)
    await save_user_action(user_id=message.from_user.id, action='/start')


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
    await save_user_action(user_id=message.from_user.id, action='/main_menu')


@dp.message_handler(state=FSM_classes.MultiDialog.setToken)
async def set_token(message: types.Message):
    Welcome_kb = InlineKeyboardMarkup()
    Welcome_kb.add(InlineKeyboardButton(
        'Приятно познакомиться!', callback_data='Welcome_btn0'))
    if message.text in Token_Raiff:
        try:
            await set_user_token(user_id=message.from_user.id, token=message.text)
            await bot.send_message(message.from_user.id, "Спасибо! Токен установлен корректно!", parse_mode='html',
                                   reply_markup=Welcome_kb)
            await FSM_classes.MultiDialog.menu.set()
        except Exception:
            await bot.send_message(message.from_user.id, "Произошла ошибка, попробуйте ещё раз", parse_mode='html')
    else:
        await bot.send_message(message.from_user.id, "Вы ввели некорректный токен, пожалуйста введите токен, который вы получили на работе, "
                                                     "он состоит из заглавных букв английского алфавита и числа, записанных слитно (например, SME16, RCS28 и др.)", parse_mode='html')
    await log_users(message)


@dp.message_handler(state=FSM_classes.MultiDialog.tech_support)
async def inline_quick_help(message: types.Message):
    db_data = sqlite3.connect('Databases/Data_users.db')
    cur_data = db_data.cursor()
    user_support = cur_data.execute('SELECT token FROM profile WHERE user_id = ?', (message.from_user.id,)).fetchone()
    await bot.send_message(chat_id=chats_id.support_chat_id, text=f"{str(message.from_user.id)}\n{user_support[0]}\n{str(message.text)}", parse_mode='html')
    await bot.send_message(message.from_user.id, 'Ваш отчёт об ошибке успешно отправлен разработчикам! '
                                                 '\nСпасибо, что помогаете сделать бот лучше!'
                                                 '\n\nЕсли хотите сообщить ещё об одной ошибке, просто введите команду /support')


@dp.message_handler(commands=['fix_tokens'], state='*', chat_id=[417986886, chats_id.commands_chat_id])
async def fix_tokens_users(message: types.Message):
    users_fix_tokens = [860113766, 566646368, 389638229, 5203851196, 324651616, 2099691929, 487050823, 5372058587, 758920281, 397822431, 239034067, 417986886]
    for i in range(len(users_fix_tokens)):
        await bot.send_message(chat_id=users_fix_tokens[i], text='Добрый вечер! '
                                                                 '\nДля актуализации информации о текущих токенах пользователей, просим вас повторно ввести ваш токен доступа, выданный на работе, '
                                                                 'он состоит из заглавных букв английского алфавита и числа, записанных слитно (например, SME16, RCS28, PREM12 и др.)'
                                                                 '\n\nВпереди вас ждёт много интересного! Подключайтесь! '
                                                                 '\nБудем благодарны вам за помощь в тестировании!', parse_mode='html')
        state = dp.current_state(chat=users_fix_tokens[i], user=users_fix_tokens[i])
        await state.set_state(FSM_classes.MultiDialog.setToken)
        await bot.send_message(message.chat.id, text='Отправлено '+str(users_fix_tokens[i]))


@dp.message_handler(commands=['get_db'], state='*', chat_id=[417986886,chats_id.commands_chat_id])
async def get_db(message: types.Message):
    await bot.send_document(message.chat.id, open('Databases/Data_users.db', 'rb'))


@dp.message_handler(commands=['send_to_user'], state='*', chat_id=[417986886, chats_id.commands_chat_id])
async def send_to_user(message: types.Message):
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(FSM_classes.Admin.send_to_user_id)
    await bot.send_message(message.chat.id, text='Добрый день, начальник! Пришлите ID пользователя',
                           parse_mode='html')


@dp.message_handler(state=FSM_classes.Admin.send_to_user_id, chat_id=[417986886,chats_id.commands_chat_id])
async def send_to_user_id(message: types.Message):
    global send_to_user_id_remember
    send_to_user_id_remember = int(message.text)
    await bot.send_message(message.chat.id, text='Теперь напишите, что ему передать',
                           parse_mode='html')
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(FSM_classes.Admin.send_to_user_message)


@dp.message_handler(state=FSM_classes.Admin.send_to_user_message, chat_id=[417986886,chats_id.commands_chat_id])
async def send_to_user_message(message: types.Message):
    await bot.send_message(chat_id=send_to_user_id_remember, text=message.text, parse_mode='html')
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(FSM_classes.MultiDialog.menu)
    await bot.send_message(message.chat.id, 'Сообщение пользователю '+str(send_to_user_id_remember)+' успешно отправлено')


@dp.message_handler(commands=['agreement_mailing'], state='*', chat_id=[417986886, chats_id.commands_chat_id])
async def mailing_agreement(message: types.Message):
    await bot.send_message(message.chat.id,
                           text='Рассылка соглашения началась')
    text_agreement = ('Добрый день! Подскажите, вам бы было интересно получать сообщения с подборками психологических рекомендаций и аффирмаций. '
                      '\nВсего одно сообщение в день, рекомендуем попробовать')
    answer_agreement = InlineKeyboardMarkup(row_width=1, resize_keyboard=True).add(InlineKeyboardButton(text='Да, можно попробовать', callback_data='agreement_y'),
                                                                                   KeyboardButton(text='Нет', callback_data='agreement_n'))
    db_data = sqlite3.connect('Databases/Data_users.db')
    cur_data = db_data.cursor()
    users = cur_data.execute(
        'SELECT user_id FROM profile').fetchall()
    file = open('Agreement_report.txt', 'w')
    for user_agreement in range(len(users)):
        try:
            await bot.send_message(chat_id=(users[user_agreement][0]),
                                   text=text_agreement, parse_mode='html', reply_markup=answer_agreement)
            file.write(f'\nОтправлено ' + str(users[user_agreement][0]))
            await asyncio.sleep(0.1)
            db_data.commit()
        except BotBlocked:
            cur_data.execute('UPDATE profile SET user_id = 0 WHERE user_id = ?',
                             (users[user_agreement][0],))
            file.write(f'\nБот заблокирован ' + str(users[user_agreement][0]))
            db_data.commit()
    cur_data.execute('DELETE FROM profile WHERE user_id = ?', (int(0),))
    db_data.commit()
    file = open('Agreement_report.txt', 'rb')
    await bot.send_message(chat_id=message.chat.id, text='Соглашение успешно разослано!')
    await bot.send_document(message.chat.id, file)
    file.close()
    os.remove('Agreement_report.txt')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('agreement_'), state='*')
async def callback_agreement(callback_query: types.CallbackQuery):
    db_data = sqlite3.connect('Databases/Data_users.db')
    cur_data = db_data.cursor()
    db_da = sqlite3.connect('Databases/Data_users.db')
    cur_da = db_da.cursor()
    await NEW_affirmation(user_id=callback_query.from_user.id, username=callback_query.from_user.username)
    cur_data.execute("UPDATE NEW_affirmation SET token = ? WHERE user_id = ?", (
    cur_da.execute('SELECT token FROM profile WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0],
    callback_query.from_user.id))
    db_data.commit()
    if callback_query.data[-1] == 'y':
        cur_data.execute('UPDATE NEW_affirmation SET agree = ? WHERE user_id = ?', ('y', callback_query.from_user.id))
        await bot.send_message(callback_query.from_user.id, 'Спасибо вам за ответ! Очень надеемся, что вам понравится!')
    else:
        cur_data.execute('UPDATE NEW_affirmation SET agree = ? WHERE user_id = ?', ('n', callback_query.from_user.id))
        await bot.send_message(callback_query.from_user.id, 'Очень жаль, что вы не захотели, если передумаете, напишите нам в поддержку')
    db_data.commit()


@dp.message_handler(commands=['admin_mailing'], state='*', chat_id=[417986886, chats_id.commands_chat_id])
async def check_active_users(message: types.Message):
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(FSM_classes.Admin.mailing_all)
    await bot.send_message(message.chat.id, text='Здравствуйте, босс! Пришлите то, что хотите разослать!',
                           parse_mode='html')


@dp.message_handler(commands=['receiving_feedback'], state='*')
async def start_feedback(message: types.Message):
    await bot.send_message(message.chat.id, text='Введите пароль:')
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(FSM_classes.adminCommands.receiving_feedback_password)


@dp.message_handler(state=FSM_classes.adminCommands.receiving_feedback_password, chat_id=[417986886,chats_id.commands_chat_id])
async def process_feedback(message: types.Message):
    if message.text == 'ad12min3':
        await bot.send_message(message.chat.id,
                               text='Рассылка опроса началась')
        start_of_feedback = 'Добрый день! ' \
                            '\n\nНе могли бы вы уделить немного времени и поделиться вашими впечатлениями о чат-боте? (6 вопросов отнимут у вас не более 3 минут)' \
                            '\nВаш ответ поможет нам улучшить качество предоставляемых услуг. ' \
                            '\n\nПожалуйста, оцените следующие утверждения, выбрав наиболее подходящий вариант: ' \
                            '\n\n1. Взаимодействовали ли вы с чат-ботом? '
        answer_1_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(KeyboardButton('Да'), KeyboardButton('Нет'))
        db_data = sqlite3.connect('Databases/Data_users.db')
        cur_data = db_data.cursor()
        users = cur_data.execute(
            'SELECT user_id FROM profile').fetchall()
        for user_mailing in range(len(users)):
            try:
                await bot.send_message(chat_id=(users[user_mailing][0]),
                                       text=start_of_feedback, parse_mode='html', reply_markup=answer_1_keyboard)
                await data_feedback(user_id=users[user_mailing][0])
                state = dp.current_state(chat=users[user_mailing][0], user=users[user_mailing][0])
                await state.set_state(FSM_classes.Feedback.answer_1_yn)
                await asyncio.sleep(0.1)
            except BotBlocked:
                cur_data.execute('UPDATE profile SET user_id = 0 WHERE user_id = ?',
                                 (users[user_mailing][0],))
                db_data.commit()
        cur_data.execute('DELETE FROM profile WHERE user_id = ?', (int(0),))
        db_data.commit()
        await bot.send_message(message.chat.id,
                               text='Опросы успешно разосланы!')
    else:
        await bot.send_message(message.from_user.id, text='Ошибка доступа!'
                                                          '\n/receiving_feedback - ввести другой пароль '
                                                          '\n/main_menu - перейти в главное меню')


@dp.message_handler(content_types=['text'], state=FSM_classes.Feedback.answer_1_yn)
async def feedback_answer_1(message: types.Message):
    db_f = sqlite3.connect('Databases/Data_users.db')
    cur_f = db_f.cursor()
    cur_f.execute("UPDATE feedback SET answer_1_yn = ? WHERE user_id = ?", (message.text, message.from_user.id))
    db_f.commit()
    answer_2_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(KeyboardButton('Очень полезен'), KeyboardButton('Полезен, но есть недостатки'),
                                                  KeyboardButton('Есть польза, но много недостатков'), KeyboardButton('Бесполезен'), KeyboardButton('Ещё не взаимодействовал'))
    await bot.send_message(message.from_user.id,
                           text='2. Насколько был полезен для вас чат-бот?', parse_mode='html', reply_markup=answer_2_keyboard)
    await FSM_classes.Feedback.answer_2_choose.set()


@dp.message_handler(content_types=['text'], state=FSM_classes.Feedback.answer_2_choose)
async def feedback_answer_2(message: types.Message):
    db_f = sqlite3.connect('Databases/Data_users.db')
    cur_f = db_f.cursor()
    cur_f.execute("UPDATE feedback SET answer_2_choose = ? WHERE user_id = ?", (message.text, message.from_user.id))
    db_f.commit()
    answer_3_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(KeyboardButton('Общаться комфортно'), KeyboardButton('Общаться скорее комфортно, но есть недостатки'),
                                                  KeyboardButton('Большинство общения неприятно'), KeyboardButton('Неприятно общаться, так как затрагиваются личные темы'))
    await bot.send_message(message.from_user.id,
                           text='3. Как бы вы оценили уровень общения с чат-ботом на темы, связанные с вашим психологическим состоянием?', parse_mode='html', reply_markup=answer_3_keyboard)
    await FSM_classes.Feedback.answer_3_choose.set()


@dp.message_handler(content_types=['text'], state=FSM_classes.Feedback.answer_3_choose)
async def feedback_answer_2(message: types.Message):
    db_f = sqlite3.connect('Databases/Data_users.db')
    cur_f = db_f.cursor()
    cur_f.execute("UPDATE feedback SET answer_3_choose = ? WHERE user_id = ?", (message.text, message.from_user.id))
    db_f.commit()
    await bot.send_message(message.from_user.id,
                           text='4. Были ли у вас какие-либо негативные или позитивные эмоции, связанные с использованием чат-бота для психологической поддержки (прохождение тестов, использование практик, система рекомендаций)? '
                                '\nЕсли да, то будем признательны, если вы поделитесь вашим опытом', parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
    await FSM_classes.Feedback.answer_4.set()


@dp.message_handler(content_types=['text'], state=FSM_classes.Feedback.answer_4)
async def feedback_answer_2(message: types.Message):
    db_f = sqlite3.connect('Databases/Data_users.db')
    cur_f = db_f.cursor()
    cur_f.execute("UPDATE feedback SET answer_4 = ? WHERE user_id = ?", (message.text, message.from_user.id))
    db_f.commit()
    await bot.send_message(message.from_user.id,
                           text='5. Изменили ли вы что-то в текущем чат-боте? '
                                '\nЕсли да, то пожалуйста напишите', parse_mode='html')
    await FSM_classes.Feedback.answer_5.set()


@dp.message_handler(content_types=['text'], state=FSM_classes.Feedback.answer_5)
async def feedback_answer_2(message: types.Message):
    db_f = sqlite3.connect('Databases/Data_users.db')
    cur_f = db_f.cursor()
    cur_f.execute("UPDATE feedback SET answer_5 = ? WHERE user_id = ?", (message.text, message.from_user.id))
    db_f.commit()
    await bot.send_message(message.from_user.id,
                           text='6. Есть ли то, что вы бы хотели видеть в чат-боте в будущем? '
                                '\nЕсли да, то будем признательны за то, что поделились', parse_mode='html')
    await FSM_classes.Feedback.answer_6.set()


@dp.message_handler(content_types=['text'], state=FSM_classes.Feedback.answer_6)
async def feedback_answer_2(message: types.Message):
    db_f = sqlite3.connect('Databases/Data_users.db')
    cur_f = db_f.cursor()
    cur_f.execute("UPDATE feedback SET answer_6 = ? WHERE user_id = ?", (message.text, message.from_user.id))
    db_f.commit()
    await bot.send_message(message.from_user.id,
                           text='Если у вас есть пожелания или дополнительные комментарии которыми вы бы хотели поделиться? '
                                '\nЕсли нет, то напишите пожалуйста “нет”', parse_mode='html')
    await FSM_classes.Feedback.answer_extra.set()


@dp.message_handler(content_types=['text'], state=FSM_classes.Feedback.answer_extra)
async def feedback_answer_2(message: types.Message, state: FSMContext):
    db_f = sqlite3.connect('Databases/Data_users.db')
    cur_f = db_f.cursor()
    cur_f.execute("UPDATE feedback SET answer_extra = ? WHERE user_id = ?", (message.text, message.from_user.id))
    db_f.commit()
    await bot.send_message(message.from_user.id,
                           text='Спасибо вам за участие в опросе! '
                                '\nВаши ответы помогут нам сделать чат-бот психологической поддержки более эффективным и удобным для вашего использования!', parse_mode='html')
    await FSM_classes.MultiDialog.menu.set()
    await main_menu(message, state)

## Feedback marathon


@dp.message_handler(commands=['fb_marathon'], state='*')
async def start_fb_marathon(message: types.Message):
    await bot.send_message(message.chat.id, text='Введите пароль:')
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(FSM_classes.adminCommands.FB_marathon_password)


@dp.message_handler(state=FSM_classes.adminCommands.FB_marathon_password, chat_id=[417986886, chats_id.commands_chat_id])
async def process_fb_marathon(message: types.Message):
    if message.text == 'ad12min3':
        await bot.send_message(message.chat.id,
                               text='Рассылка опроса началась')
        start_of_feedback = 'Добрый вечер! ' \
                            '\n\nНе могли бы вы уделить немного времени и поделиться вашими впечатлениями о втором дне нашего пути? \nЭто поможет в будущем предоставлять вам более качественный продукт' \
                            '\n\n1) Как прошёл ваш день? (оцените по шкале от 1 до 10)'
        answer_1_keyboard = ReplyKeyboardMarkup(row_width=5, resize_keyboard=True).add(KeyboardButton('😭'), KeyboardButton('2'), KeyboardButton('3'), KeyboardButton('4'), KeyboardButton('😕'), KeyboardButton('😐'), KeyboardButton('7'), KeyboardButton('8'), KeyboardButton('9'), KeyboardButton('😃'))
        db_data = sqlite3.connect('Databases/Data_users.db')
        cur_data = db_data.cursor()
        db_da = sqlite3.connect('Databases/Data_users.db')
        cur_da = db_da.cursor()
        users = cur_data.execute(
            'SELECT user_id FROM profile').fetchall()
        file = open('Quiz_report.txt', 'w')
        for user_mailing in range(len(users)):
            try:
                await bot.send_message(chat_id=(users[user_mailing][0]),
                                       text=start_of_feedback, parse_mode='html', reply_markup=answer_1_keyboard)
                await data_FB_marathon(user_id=users[user_mailing][0])
                cur_data.execute("UPDATE FB_marathon_2 SET token = ? WHERE user_id = ?", (cur_da.execute('SELECT token FROM profile WHERE user_id = ?', (users[user_mailing][0],)).fetchone()[0], users[user_mailing][0]))
                file.write(f'\nОтправлено ' + str(users[user_mailing][0]))
                state = dp.current_state(chat=users[user_mailing][0], user=users[user_mailing][0])
                await state.set_state(FSM_classes.FB_marathon.answer_1)
                await asyncio.sleep(0.1)
                db_data.commit()
            except BotBlocked:
                cur_data.execute('UPDATE profile SET user_id = 0 WHERE user_id = ?',
                                 (users[user_mailing][0],))
                file.write(f'\nБот заблокирован ' + str(users[user_mailing][0]))
                db_data.commit()
        cur_data.execute('DELETE FROM profile WHERE user_id = ?', (int(0),))
        db_data.commit()
        file = open('Quiz_report.txt', 'rb')
        await bot.send_message(chat_id=message.chat.id, text='Опрос успешно разослан!')
        await bot.send_document(message.chat.id, file)
        file.close()
        os.remove('Quiz_report.txt')
    else:
        await bot.send_message(message.chat.id, text='Ошибка доступа!'
                                                          '\n/receiving_feedback - ввести другой пароль '
                                                          '\n/main_menu - перейти в главное меню')


@dp.message_handler(content_types=['text'], state=FSM_classes.FB_marathon.answer_1)
async def feedback_answer_1(message: types.Message):
    db_f = sqlite3.connect('Databases/Data_users.db')
    cur_f = db_f.cursor()
    cur_f.execute("UPDATE FB_marathon_2 SET answer_1 = ? WHERE user_id = ?", (message.text, message.from_user.id))
    db_f.commit()
    answer_2_keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True).add(KeyboardButton('Да'), KeyboardButton('Не уверен'), KeyboardButton('Нет'))
    await bot.send_message(message.from_user.id,
                           text='2) Принёс ли вам сегодняшний день новые и интересные события?', parse_mode='html', reply_markup=answer_2_keyboard)
    await FSM_classes.FB_marathon.answer_2.set()


@dp.message_handler(content_types=['text'], state=FSM_classes.FB_marathon.answer_2)
async def feedback_answer_2(message: types.Message):
    db_f = sqlite3.connect('Databases/Data_users.db')
    cur_f = db_f.cursor()
    cur_f.execute("UPDATE FB_marathon_2 SET answer_2 = ? WHERE user_id = ?", (message.text, message.from_user.id))
    db_f.commit()
    answer_3_keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True).add(KeyboardButton('Да'), KeyboardButton('Не уверен'),
                                                  KeyboardButton('Нет'))
    await bot.send_message(message.from_user.id,
                           text='3) Понравилась ли вам сегодняшняя подборка психологической теории?', parse_mode='html', reply_markup=answer_3_keyboard)
    await FSM_classes.FB_marathon.answer_3.set()


@dp.message_handler(content_types=['text'], state=FSM_classes.FB_marathon.answer_3)
async def feedback_answer_3(message: types.Message):
    db_f = sqlite3.connect('Databases/Data_users.db')
    cur_f = db_f.cursor()
    cur_f.execute("UPDATE FB_marathon_2 SET answer_3 = ? WHERE user_id = ?", (message.text, message.from_user.id))
    db_f.commit()
    answer_4_keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True).add(KeyboardButton('Да'), KeyboardButton('Не уверен'),
                                                  KeyboardButton('Нет'))
    await bot.send_message(message.from_user.id,
                           text='4) Интересно ли было выполнять ежедневную практику?', parse_mode='html', reply_markup=answer_4_keyboard)
    await FSM_classes.FB_marathon.answer_4.set()


@dp.message_handler(content_types=['text'], state=FSM_classes.FB_marathon.answer_4)
async def feedback_answer_4(message: types.Message):
    db_f = sqlite3.connect('Databases/Data_users.db')
    cur_f = db_f.cursor()
    cur_f.execute("UPDATE FB_marathon_2 SET answer_4 = ? WHERE user_id = ?", (message.text, message.from_user.id))
    db_f.commit()
    answer_5_keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True).add(KeyboardButton('Да'), KeyboardButton('Не уверен'),
                                                  KeyboardButton('Нет'))
    await bot.send_message(message.from_user.id,
                           text='5) Помогла ли вам ежедневная практика быть в ресурсе в течение дня?', parse_mode='html', reply_markup=answer_5_keyboard)
    await FSM_classes.FB_marathon.answer_5.set()


@dp.message_handler(content_types=['text'], state=FSM_classes.FB_marathon.answer_5)
async def feedback_answer_5(message: types.Message):
    db_f = sqlite3.connect('Databases/Data_users.db')
    cur_f = db_f.cursor()
    cur_f.execute("UPDATE FB_marathon_2 SET answer_5 = ? WHERE user_id = ?", (message.text, message.from_user.id))
    db_f.commit()
    answer_6_keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True).add(KeyboardButton('Да'), KeyboardButton('Не уверен'),
                                                  KeyboardButton('Нет'))
    await bot.send_message(message.from_user.id,
                           text='6) Удалось ли сегодня утром позитивно настроиться?', parse_mode='html', reply_markup=answer_6_keyboard)
    await FSM_classes.FB_marathon.answer_6.set()


@dp.message_handler(content_types=['text'], state=FSM_classes.FB_marathon.answer_6)
async def feedback_answer_6(message: types.Message, state: FSMContext):
    db_f = sqlite3.connect('Databases/Data_users.db')
    cur_f = db_f.cursor()
    cur_f.execute("UPDATE FB_marathon_2 SET answer_6 = ? WHERE user_id = ?", (message.text, message.from_user.id))
    db_f.commit()
    await bot.send_message(message.from_user.id,
                           text='Напишите пожалуйста, как вам общие впечатления по текущим взаимодействиям 📝 \nБудем благодарны за любую обратную связь!', parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
    await FSM_classes.FB_marathon.answer_7.set()


@dp.message_handler(content_types=['text'], state=FSM_classes.FB_marathon.answer_7)
async def feedback_answer_7(message: types.Message, state: FSMContext):
    db_f = sqlite3.connect('Databases/Data_users.db')
    cur_f = db_f.cursor()
    cur_f.execute("UPDATE FB_marathon_2 SET answer_7 = ? WHERE user_id = ?", (message.text, message.from_user.id))
    db_f.commit()
    await bot.send_message(message.from_user.id,
                           text='Спасибо вам за участие в опросе! '
                                '\nВаши ответы помогут нам сделать чат-бот психологической поддержки более эффективным и удобным для вашего использования!', parse_mode='html')
    await FSM_classes.MultiDialog.menu.set()
    await main_menu(message, state)


@dp.callback_query_handler(state=FSM_classes.MultiDialog.quick_help)
async def inline_quick_help(callback_query: types.CallbackQuery):
    await quick_help.all_way_callback_quick_help(callback_query)


@dp.message_handler(state=FSM_classes.MultiDialog.quick_help)
async def reply_quick_help(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await FSM_classes.MultiDialog.menu.set()
        await main_menu(message, state)
    await quick_help.all_way_quick_help(message)


@dp.message_handler(commands=['getuserreport'], state='*')
async def get_user_report(message: types.Message):
    await bot.send_message(message.chat.id, text='Введите пароль:')
    await FSM_classes.adminCommands.getUserReportPassword.set()


@dp.message_handler(state=FSM_classes.adminCommands.getUserReportPassword)
async def get_user_report(message: types.Message, state: FSMContext):
    if message.text == 'admin123':
        await bot.send_message(message.chat.id,
                               text='Введите id нужных юзеров через пробел или напишите слово "все"')
        await FSM_classes.adminCommands.getUserReportId.set()
    else:
        await bot.send_message(message.chat.id, text='Ошибка доступа!'
                                                          '\n/getuserreport - ввести другой пароль '
                                                          '\n/main_menu - перейти в главное меню')


@dp.message_handler(state=FSM_classes.adminCommands.getUserReportId)
async def get_user_report(message: types.Message, state: FSMContext):
    await state.set_data({"users": message.text})
    await bot.send_message(message.chat.id,
                           text='Введите дату начала и конца наблюдений через пробел в формате гггг:мм:дд')
    await FSM_classes.adminCommands.getUserReportDate.set()


@dp.message_handler(state=FSM_classes.adminCommands.getUserReportDate)
async def get_user_report(message: types.Message, state: FSMContext):
    users = await state.get_data("users")
    try:
        startDate, endDate = message.text.split(' ')
    except:
        await bot.send_message(message.chat.id, text='Ошибка при вводе даты, попробуйте ещё')
        await FSM_classes.adminCommands.getUserReportDate.set()
        return

    startDate = startDate.replace(':', '')
    endDate = endDate.replace(':', '')
    users = str(users['users']).split(' ')
    if len(users) == 1 and users[0] == 'все':
        users = await get_all_user_ids()
        users = [str(user[0]) for user in users]

    await admin_commands.createExcelFileReportCommand(startDate,endDate,users)
    with open('userData.xlsx', 'rb') as f:
        await bot.send_document(chat_id=message.from_user.id, document=InputFile(f))


@dp.message_handler(commands=['getuseractions'], state='*')
async def get_user_report(message: types.Message):
    await bot.send_message(message.chat.id, text='Введите пароль:')
    await FSM_classes.adminCommands.getUserActionPassword.set()


@dp.message_handler(state=FSM_classes.adminCommands.getUserActionPassword)
async def get_user_report(message: types.Message, state: FSMContext):
    if message.text == 'admin123':
        await bot.send_message(message.chat.id,
                               text='Введите токены нужных юзеров через пробел или напишите слово "все"')
        await FSM_classes.adminCommands.getUserActionId.set()
    else:
        await bot.send_message(message.chat.id, text='Ошибка доступа!'
                                                          '\n/getuserreport - ввести другой пароль '
                                                          '\n/main_menu - перейти в главное меню')


@dp.message_handler(state=FSM_classes.adminCommands.getUserActionId)
async def get_user_report(message: types.Message, state: FSMContext):
    await state.set_data({"users": message.text})
    await bot.send_message(message.chat.id, text='Введите дату начала и конца наблюдений через пробел')
    await FSM_classes.adminCommands.getUserActionDate.set()


@dp.message_handler(state=FSM_classes.adminCommands.getUserActionDate)
async def get_user_report(message: types.Message, state: FSMContext):
    tokens = await state.get_data("users")
    startDate, endDate = message.text.split(' ')
    tokens = str(tokens['users']).split(' ')

    if len(tokens) == 1 and tokens[0] == 'все':
        await admin_commands.createExcelFileActionsForAllUsersWithTokens(startDate, endDate)
    else:
        await admin_commands.createExcelFileActionCommand(startDate, endDate, tokens)

    with open('getUserAction.xlsx', 'rb') as f:
        await bot.send_document(chat_id=message.chat.id, document=InputFile(f))
    await FSM_classes.MultiDialog.menu.set()
    await main_menu(message, state)


@dp.message_handler(commands=['getuserreportgraph'], state='*')
async def get_user_report(message: types.Message):
    await bot.send_message(message.from_user.id, text='Введите дату формата дд:мм:гггг')
    await FSM_classes.adminCommands.getUserReportGraphDate.set()


@dp.message_handler(state=FSM_classes.adminCommands.getUserReportGraphDate)
async def get_user_report(message: types.Message, state: FSMContext):
    try:
        dateStart = datetime.strptime(message.text, '%d:%m:%Y')
        await bot.send_message(message.from_user.id, text='График вашего приема воды',reply_markup=Markups.backHabitRe)
        with open("scatter_plot.png", "rb") as f:
            photo = InputFile(f)
            await bot.send_photo(message.from_user.id, photo)
        await admin_commands.createGraphReportCommand(dateStart,message.from_user.id)
        await FSM_classes.MultiDialog.menu.set()
    except ValueError:
        await bot.send_message(message.from_user.id, text='Введена не корректная дата!\n'
                                                          'Введите дату в формате чч:мм:гггг')
        await FSM_classes.adminCommands.getUserReportGraphDate.set()


@dp.message_handler(content_types=['photo'], state=FSM_classes.Admin.mailing_all, chat_id=[417986886, chats_id.commands_chat_id])
async def mailing_photo(message: types.Message):
    await message.photo[-1].download(destination_file='mailing.jpg')
    db_user_blocked = sqlite3.connect('Databases/Data_users.db')
    cur_user_blocked = db_user_blocked.cursor()
    users = cur_user_blocked.execute('SELECT user_id FROM profile').fetchall()
    await bot.send_message(chat_id=message.chat.id, text='Получено, рассылка началась',
                           parse_mode='html')
    await FSM_classes.MultiDialog.menu.set()
    file = open('Mailing_report.txt', 'w')
    for user in range(len(users)):
        try:
            photo_mailing = open('mailing.jpg', 'rb')
            await bot.send_photo(chat_id=(users[user][0]), photo=photo_mailing, parse_mode='html')
            file.write(f'\nОтправлено '+str(users[user][0]))
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_user_blocked.execute(
                'UPDATE profile SET active = "Нет" WHERE user_id = ?', (users[user][0],))
            await bot.send_message(chat_id=message.chat.id, text='Бот заблокирован '+str(users[user][0]), parse_mode='html')
            file.write(f'\nБот заблокирован '+str(users[user][0]))
            db_user_blocked.commit()
    file = open('Mailing_report.txt', 'rb')
    await bot.send_message(chat_id=message.chat.id, text='Ваше изображение успешно отправлено! Вы молодец, босс!')
    await bot.send_document(message.chat.id, file)
    file.close()
    os.remove('Mailing_report.txt')


@dp.message_handler(content_types=['audio'], state=FSM_classes.Admin.mailing_all, chat_id=[417986886, chats_id.commands_chat_id])
async def mailing_audio(message: types.Message):
    await message.audio.download(destination_file=str(message.audio.file_name))
    db_user_blocked = sqlite3.connect('Databases/Data_users.db')
    cur_user_blocked = db_user_blocked.cursor()
    users = cur_user_blocked.execute('SELECT user_id FROM profile').fetchall()
    await bot.send_message(chat_id=message.chat.id, text='Получено, рассылка началась',
                           parse_mode='html')
    await FSM_classes.MultiDialog.menu.set()
    file = open('Mailing_report.txt', 'w')
    for user in range(len(users)):
        try:
            audio_mailing = open(str(message.audio.file_name), 'rb')
            await bot.send_audio(chat_id=(users[user][0]), audio=audio_mailing, parse_mode='html')
            file.write(f'\nОтправлено '+str(users[user][0]))
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_user_blocked.execute(
                'UPDATE profile SET active = "Нет" WHERE user_id = ?', (users[user][0],))
            await bot.send_message(chat_id=message.chat.id, text='Бот заблокирован '+str(users[user][0]), parse_mode='html')
            file.write(f'\nБот заблокирован '+str(users[user][0]))
            db_user_blocked.commit()
    os.remove(message.audio.file_name)
    file = open('Mailing_report.txt', 'rb')
    await bot.send_message(chat_id=message.chat.id, text='Ваше изображение успешно отправлено! Вы молодец, босс!')
    await bot.send_document(message.chat.id, file)
    file.close()
    os.remove('Mailing_report.txt')


@dp.message_handler(content_types=['text'], state=FSM_classes.Admin.mailing_all, chat_id=[417986886, chats_id.commands_chat_id])
async def mailing_text(message: types.Message):
    db_user_blocked = sqlite3.connect('Databases/Data_users.db')
    cur_user_blocked = db_user_blocked.cursor()
    users = cur_user_blocked.execute('SELECT user_id FROM profile').fetchall()
    await bot.send_message(chat_id=message.chat.id, text='Получено, рассылка началась',
                           parse_mode='html')
    await FSM_classes.MultiDialog.menu.set()
    file = open('Mailing_report.txt', 'w')
    for user in range(len(users)):
        try:
            await bot.send_message(chat_id=(users[user][0]),
                                   text=message.text, parse_mode='html')
            file.write(f'\nОтправлено '+str(users[user][0]))
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_user_blocked.execute(
                'UPDATE profile SET active = "Нет" WHERE user_id = ?', (users[user][0],))
            await bot.send_message(chat_id=message.chat.id, text='Бот заблокирован '+str(users[user][0]), parse_mode='html')
            file.write(f'\nБот заблокирован '+str(users[user][0]))
            db_user_blocked.commit()
    file = open('Mailing_report.txt', 'rb')
    await bot.send_message(chat_id=message.chat.id, text='Ваше сообщение успешно отправлено! Вы молодец, босс!')
    await bot.send_document(message.chat.id, file)
    file.close()
    os.remove('Mailing_report.txt')


@dp.message_handler(commands=['smart_mailing'], state='*', chat_id=[417986886, chats_id.commands_chat_id])
async def smart_mailing(message: types.Message):
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.set_state(FSM_classes.Admin.smart_mailing)
    global text_smart_mailing
    global keyboards_
    text_smart_mailing = []
    keyboards_ = ['Доброе утро! Расскажи поподробнее', 'Продолжай', 'Дальше', 'Продолжай']
    await bot.send_message(message.chat.id, text='Смело отправляйте мне 5 кусков текста разными сообщениями и я запомню их последовательно',
                           parse_mode='html')


@dp.message_handler(content_types=['text'], state=FSM_classes.Admin.smart_mailing, chat_id=[417986886, chats_id.commands_chat_id])
async def smart_mailing_text_recording(message: types.Message):
    text_smart_mailing.append(str(message.text))
    if len(text_smart_mailing) <= 4:
        await bot.send_message(message.chat.id, text='Получил часть № '+str(len(text_smart_mailing)))
    else:
        await bot.send_message(message.chat.id, text='Получил часть № '+str(len(text_smart_mailing)))
        db_user_blocked = sqlite3.connect('Databases/Data_users.db')
        cur_user_blocked = db_user_blocked.cursor()
        users = cur_user_blocked.execute('SELECT user_id FROM profile').fetchall()
        await bot.send_message(chat_id=message.chat.id, text='Получено, рассылка началась',
                               parse_mode='html')
        await FSM_classes.MultiDialog.menu.set()
        file = open('Smart_mailing_report.txt', 'w')
        for user in range(len(users)):
            try:
                await bot.send_message(chat_id=(users[user][0]),
                                       text=text_smart_mailing[0], parse_mode='html',
                                       reply_markup=InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text=str(keyboards_[0]), callback_data='smart_mailing_continue1')))
                file.write(f'\nОтправлено ' + str(users[user][0]))
                await asyncio.sleep(0.1)
            except BotBlocked:
                cur_user_blocked.execute(
                    'UPDATE profile SET active = "Нет" WHERE user_id = ?', (users[user][0],))
                await bot.send_message(chat_id=message.chat.id, text='Бот заблокирован ' + str(users[user][0]),
                                       parse_mode='html')
                file.write(f'\nБот заблокирован ' + str(users[user][0]))
                db_user_blocked.commit()
        file = open('Smart_mailing_report.txt', 'rb')
        await bot.send_message(chat_id=message.chat.id, text='Рассылка успешно завершена')
        await bot.send_document(message.chat.id, file)
        file.close()
        os.remove('Smart_mailing_report.txt')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('smart_mailing_continue'), state='*')
async def smart_mailing_continue(callback_query: types.CallbackQuery, state: FSMContext):
    if int(callback_query.data[-1]) < 4:
        await bot.send_message(callback_query.from_user.id, text=text_smart_mailing[int(callback_query.data[-1])], parse_mode='html',
                           reply_markup=InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton(text=str(keyboards_[int(callback_query.data[-1])]), callback_data='smart_mailing_continue'+str(int(int(callback_query.data[-1])+1)))))
    else:
        await bot.send_message(callback_query.from_user.id, text=text_smart_mailing[int(callback_query.data[-1])], parse_mode='html')
        await bot.send_message(chat_id=chats_id.reports_chat_id,
                               text=f"{str(callback_query.from_user.id)}\nПользователь прочитал ежедневную рассылку",
                               parse_mode='html')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('Welcome_btn'), state=FSM_classes.MultiDialog.menu)
async def mailing(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data[-1] == '0':
        enterIn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
            KeyboardButton('Чувствую проблему'),
            KeyboardButton('Пройти тест'))
        await bot.send_message(callback_query.from_user.id,
                               'Как вы себя чувствуете?'
                               '\n\nНажмите "Чувствую проблему", чтобы мгновенно получить рекомендации, которые помогут вам справиться с текущим состоянием '
                               'или нажмите "Пройти тест" для того, чтобы пройти текущему состоянию или пройти тест, состоящий из 36 вопросов для того, чтобы начать '
                               'наше знакомство и получить индивидуальную подборку рекомендаций, упражнений и практик для улучшения состояния!',
                               parse_mode='html', reply_markup=enterIn)


@dp.message_handler(commands=['practices'], state='*')
async def practices(message: types.Message):
    await FSM_classes.MultiDialog.practices.set()
    await Practices.type_practices(message)
    await save_user_action(user_id=message.from_user.id, action='/practices')


@dp.message_handler(commands=['support'], state='*')
async def support(message: types.Message):
    await bot.send_message(message.from_user.id,
                           text='Пожалуйста, опишите ошибку с которой вы столкнулись и отправьте одним сообщением')
    await FSM_classes.MultiDialog.tech_support.set()
    await save_user_action(user_id=message.from_user.id, action='/support')


@dp.message_handler(commands=['test'], state='*')
async def test(message: types.message, state: FSMContext):
    await FSM_classes.MultiDialog.tests.set()
    await Tests.pretest(message, state)
    await log_users(message)
    await save_user_action(user_id=message.from_user.id, action='/test')


@dp.message_handler(commands=['courses'], state='*')
async def courses(message: types.Message, state: FSMContext):
    await FSM_classes.MultiDialog.courses.set()
    await Courses.precourse(message, state)
    await log_users(message)
    await save_user_action(user_id=message.from_user.id, action='/courses')


@dp.message_handler(commands=['contacts'], state='*')
async def contacts(message: types.Message):
    await bot.send_message(message.from_user.id, 'Здравствуйте! '
                                                 'Меня зовут Reform. Я оказываю психологическую поддержку.'
                                                 'Мои возможности пока что ограничены, но меня совершенствуют с каждым днём.'
                                                 'Если у вас есть вопросы или вы обнаружили ошибку, вы можете обратиться к @APecherkin.',
                           parse_mode='html', reply_markup=Markups.cont)
    await log_users(message)
    await save_user_action(user_id=message.from_user.id, action='/contacts')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('Main_menu'), state='*')
async def main_menu_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await FSM_classes.HabitSleep.none.set()
    await FSM_classes.MultiDialog.menu.set()
    await bot.send_message(callback_query.from_user.id, 'Вы в главном меню. Не знаете что делать дальше?'
                                                        '\n\n🧘‍♀️ Практики помогут вам разгрузиться после тяжёлого дня или успокоиться'
                                                        '\n📝 Пройдите тесты, чтобы определить актуальное состояние и выявить проблему'
                                                        '\n💪 Трекер привычек поможет внедрить и поддерживать полезные навыки'
                                                        '\n🌳 Чувствуете себя не очень? Разберитесь поподробнее в себе и выявите проблему'
                                                        '\n💬 Также вы можете обсудить проблему и получить рекомендации от специалиста'
                                                        '\nВыберите, что вас интересует',
                           parse_mode='html', reply_markup=Markups.main_kb)


@dp.message_handler(state=FSM_classes.MultiDialog.practices)
async def reply_practices(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await main_menu(message, state)
    await Practices.allreply_practices(message)
    await log_users(message)


@dp.message_handler(state=FSM_classes.MultiDialog.specialist)
async def reply_specialist(message: types.Message, state: FSMContext):
    if message.text == 'Перейти':
        await Specialists.choose_specialist(message, state)
    if message.text == 'Вернуться в главное меню':
        await FSM_classes.MultiDialog.menu.set()
        await main_menu(message, state)
    await Specialists.test_holms(message, state)
    await log_users(message)


@dp.message_handler(state=FSM_classes.MultiDialog.tests)
async def reply_tests(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await FSM_classes.MultiDialog.menu.set()
        await main_menu(message, state)
    await Tests.type_test(message, state)
    await log_users(message)


@dp.message_handler(state=(
        FSM_classes.MultiDialog.test_weariness or FSM_classes.MultiDialog.test_control or FSM_classes.MultiDialog.test_selfefficacy or FSM_classes.MultiDialog.test_typeperson or FSM_classes.MultiDialog.test_stress))
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


@dp.message_handler(state=FSM_classes.HabitWater.choose_action)
async def reply_habit_water(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await main_menu(message, state)
    await Water.choose_habit_action(message, state)
    await log_users(message)


@dp.message_handler(state=FSM_classes.HabitWater.choose_amount_of_portion)
async def reply_habit_water(message: types.Message, state: FSMContext):
    await Water.choose_habit_water_portions(message, state)
    await log_users(message)


@dp.message_handler(state=FSM_classes.HabitWater.choose_schedule)
async def reply_habit_water(message: types.Message, state: FSMContext):
    await Water.choose_habit_water_schedule(message, state)
    await log_users(message)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('answerWater'), state='*')
async def reply_habit_water(callback_query: types.CallbackQuery, state: FSMContext):
    await Water.answer_water_schedule(callback_query, state)
    await FSM_classes.MultiDialog.menu.set()
    await log_users(callback_query.message)


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
    await save_user_action(user_id=message.from_user.id, action=message.text)
    if message.text == 'Вернуться в главное меню':
        await main_menu(message, state)
        await log_users(message)

    if message.text == 'Чувствую проблему':
        await FSM_classes.MultiDialog.quick_help.set()
        await bot.send_message(message.from_user.id, text='Выберите, что вы чувствуете, чтобы разобраться в проблеме поподробнее', reply_markup=quick_help.quick_help_menu)
        await log_users(message)
        await quick_help.all_way_quick_help(message)

    if message.text == 'Пройти тест':
        await FSM_classes.MultiDialog.test_weariness.set()
        await pre_points_test_weariness(user_id=message.from_user.id, username=message.from_user.username)
        await pre_answers_test_weariness(user_id=message.from_user.id, username=message.from_user.username)
        async with state.proxy() as data:
            data['count'] = 0
        async with state.proxy() as data:
            data['points'] = 0
        await points_test_weariness(state, user_id=message.from_user.id)
        await state.finish()
        await bot.send_message(message.from_user.id, text=Psy_Weariness.weariness_questions[0], reply_markup=Psy_Weariness.answers)
        db_weariness = sqlite3.connect('Databases/Result_Tests/PSY_Weariness.db')
        cur_weariness = db_weariness.cursor()
        cur_weariness.execute("UPDATE answers SET countOfAnswers = 0 WHERE user_id = ?", (message.from_user.id,))
        db_weariness.commit()

    if message.text == '🧘‍♀️ Практики':
        await FSM_classes.MultiDialog.practices.set()
        await Practices.type_practices(message)
        await log_users(message)

    if message.text == '📝 Тесты':
        await FSM_classes.MultiDialog.tests.set()
        await Tests.pretest(message, state)
        await log_users(message)

    if message.text == '💪 Привычки':
        await FSM_classes.MultiDialog.habits.set()
        await Habit.prehabits(message, state)
        await log_users(message)

    if message.text == '😨 Тревожная кнопка':
        await FSM_classes.MultiDialog.quick_help.set()
        await bot.send_message(message.from_user.id,
                               text='Выберите, что вы чувствуете, чтобы разобраться в проблеме поподробнее',
                               reply_markup=quick_help.quick_help_menu)
        await log_users(message)
        await quick_help.all_way_quick_help(message)

    if message.text == '💬 Обсудить проблему':
        await FSM_classes.MultiDialog.specialist.set()
        await Specialists.choose_specialist(message, state)
        await log_users(message)

    if message.text == '📥 Контакты':
        await contacts(message)
        await log_users(message)

    if message.text == '⚙️ Техподдержка':
        await bot.send_message(message.from_user.id, text='Пожалуйста, опишите ошибку с которой вы столкнулись и отправьте одним сообщением')
        await FSM_classes.MultiDialog.tech_support.set()
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
    users_affirmation = cur_data.execute(
        'SELECT user_id FROM NEW_affirmation WHERE agree = ?', ('y',)).fetchall()
    for user_miling in range(len(users_affirmation)):
        try:
            await bot.send_message(chat_id=(users_affirmation[user_miling][0]),
                                   text=message.text, parse_mode='html')
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_data.execute('UPDATE NEW_affirmation SET user_id = 0 WHERE user_id = ?',
                             (users_affirmation[user_miling][0],))
            db_data.commit()
    cur_data.execute('DELETE FROM NEW_affirmation WHERE user_id = ?', (int(0),))
    db_data.commit()


@dp.channel_post_handler(content_types=['photo'])
async def affirmation_mailing_photo(message: types.Message):
    await message.photo[-1].download(destination_file='affirmation.jpg')
    db_data = sqlite3.connect('Databases/Data_users.db')
    cur_data = db_data.cursor()
    users_affirmation = cur_data.execute(
        'SELECT user_id FROM NEW_affirmation WHERE agree = ?', ('y',)).fetchall()
    await asyncio.sleep(1)
    for user_miling in range(len(users_affirmation)):
        try:
            photo = open('affirmation.jpg', 'rb')
            await bot.send_photo(chat_id=(users_affirmation[user_miling][0]),
                                 photo=photo, parse_mode='html')
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_data.execute('UPDATE NEW_affirmation SET user_id = 0 WHERE user_id = ?',
                             (users_affirmation[user_miling][0],))
            db_data.commit()
    os.remove('affirmation.jpg')
    cur_data.execute('DELETE FROM NEW_affirmation WHERE user_id = ?', (int(0),))
    db_data.commit()


async def scheduler_sleep_message_wakeup():
    db_scheduler_sleep = sqlite3.connect('Databases/Current_habits.db')
    cur_scheduler = db_scheduler_sleep.cursor()
    cur_scheduler_check = db_scheduler_sleep.cursor()
    now = datetime.utcnow() + timedelta(hours=3, minutes=0)
    users_wakeup = cur_scheduler.execute(
        'SELECT user_id FROM sleep WHERE wakeup = ?', (now.strftime('%H:%M'),)).fetchall()
    for user_wakeup in range(len(users_wakeup)):
        print(users_wakeup[user_wakeup][0])
        if cur_scheduler_check.execute('SELECT active FROM sleep WHERE user_id = ?', (users_wakeup[user_wakeup][0],)).fetchone()[0] == str(1):
            try:
                await bot.send_message(chat_id=users_wakeup[user_wakeup][0], text='Пора вставать! '
                                                                                  '\nНачинать никогда не поздно! А всё начинается с небольших изменений!')
                await asyncio.sleep(0.1)
            except BotBlocked:
                cur_scheduler.execute(
                    'UPDATE sleep SET user_id = 0 WHERE user_id = ?', (users_wakeup[user_wakeup][0],))
                db_scheduler_sleep.commit()
    cur_scheduler.execute('DELETE FROM sleep WHERE user_id = ?', (int(0),))
    db_scheduler_sleep.commit()


async def scheduler_sleep_message_bedtime():
    db_scheduler_sleep = sqlite3.connect('Databases/Current_habits.db')
    cur_scheduler = db_scheduler_sleep.cursor()
    cur_scheduler_check = db_scheduler_sleep.cursor()
    now = datetime.utcnow() + timedelta(hours=3, minutes=0)
    users_bedtime = cur_scheduler.execute(
        'SELECT user_id FROM sleep WHERE bedtime = ?', (now.strftime('%H:%M'),)).fetchall()
    for user_bedtime in range(len(users_bedtime)):
        if cur_scheduler_check.execute('SELECT active FROM sleep WHERE user_id = ?', (users_bedtime[user_bedtime][0],)).fetchone()[0] == str(1):
            try:
                await bot.send_message(chat_id=users_bedtime[user_bedtime][0],
                                       text='Вы просили напомнить, что вам пора ложиться спать!'
                                            '\nЗавтра вас ждёт отличный день! '
                                            '\nПомните, великое начинется с малого!')
                await asyncio.sleep(0.1)
            except BotBlocked:
                cur_scheduler.execute(
                    'UPDATE sleep SET user_id = 0 WHERE user_id = ?', (users_bedtime[user_bedtime][0],))
                db_scheduler_sleep.commit()
    cur_scheduler.execute('DELETE FROM sleep WHERE user_id = ?', (int(0),))
    db_scheduler_sleep.commit()


async def scheduler_water_message():
    db_scheduler_water = sqlite3.connect('Databases/Current_habits.db')
    cur_scheduler_water = db_scheduler_water.cursor()
    now = datetime.utcnow() + timedelta(hours=3, minutes=0)
    time_in_min_now = int(now.strftime('%H:%M').split(':')[0]) * 60 + int(now.strftime('%H:%M').split(':')[1])
    today = datetime.today()
    weekday = today.weekday()

    if weekday < 5:
        users = cur_scheduler_water.execute(
            'SELECT user_id FROM water WHERE interval != 0 AND schedule IN ("weekdays", "both")').fetchall()
    if weekday >= 5:
        users = cur_scheduler_water.execute(
            'SELECT user_id FROM water WHERE interval != 0 AND schedule IN ("weekends", "both")').fetchall()

    if time_in_min_now in range(600, 1381):
        for user in users:
            interval = cur_scheduler_water.execute(
                'SELECT interval FROM water WHERE user_id = ?', (user[0],)).fetchone()
            amount_of_portions = cur_scheduler_water.execute(
                'SELECT amountOfPortions FROM water WHERE user_id = ?', (user[0],)).fetchone()

            if time_in_min_now % interval[0] == 0:
                try:
                    await bot.send_message(chat_id=user[0], text='Пора пить воду!'
                                                                 '\nОбъем приёма воды - ' + str(
                        round(2000 / amount_of_portions[0])) + ' мл.')
                    await asyncio.sleep(0.1)
                except BotBlocked:
                    cur_scheduler_water.execute(
                        'UPDATE water SET user_id = 0 WHERE user_id = ?', (users[user[0]][0],))
                    db_scheduler_water.commit()
                cur_scheduler_water.execute('DELETE FROM water WHERE user_id = ?', (int(0),))
                db_scheduler_water.commit()
            if time_in_min_now == 1380:
                today = datetime.today()
                tableName = 'date_' + str(today)[0:10].replace('-', '')
                cur_scheduler_water.execute(f'ALTER TABLE waterDates ADD COLUMN {tableName} TEXT')
                await bot.send_message(chat_id=user[0], text='Получилось ли выполнить норму?',
                                       reply_markup=Markups.waterAnswers)


async def scheduler_sleep():
    schedule.every(1).minute.do(scheduler_sleep_message_wakeup)
    schedule.every(1).minute.do(scheduler_sleep_message_bedtime)
    now = datetime.utcnow() + timedelta(hours=3, minutes=0)
    time_in_min_now = int(now.strftime('%H:%M').split(':')[0]) * 60 + int(now.strftime('%H:%M').split(':')[1])
    if time_in_min_now >= 600 and time_in_min_now <= 1380:
        schedule.every(1).minute.do(scheduler_water_message)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)


async def log_users(message: types.Message):
    now = datetime.now()
    botlogfile = open('LogsBot', 'a')
    print(now.strftime('%d-%m-%Y %H:%M'), ' Пользователь - ' + message.from_user.first_name,
          message.from_user.id, 'Написал - ' + message.text, file=botlogfile)
    botlogfile.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler_sleep())
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
