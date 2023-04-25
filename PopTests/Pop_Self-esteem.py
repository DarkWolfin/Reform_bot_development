import asyncio
import sqlite3

from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())

from Databases import pre_points_test_selfesteem, points_test_selfesteem

import Markups
import FSM_classes

selfesteem_questions = ['1. Как часто вас терзают мысли, что вам не следовало говорить или делать что-то?'
                     '\n\nA) очень часто'
                     '\nБ) иногда',
                     '2. Если вы общаетесь с блестящим и остроумным человеком, вы:'
                     '\n\nA) постараетесь победить его в остроумии'
                     '\nБ) не будете ввязываться в соревнование, а отдадите ему должное и выйдете из разговора',
                     '3. Выберите одно из мнений, наиболее вам близкое:'
                     '\n\nA) то, что многим кажется везением, на самом деле, результат упорного труда'
                     '\nБ) успехи зачастую зависят от счастливого стечения обстоятельств'
                     '\nВ) в сложной ситуации главное - не упорство или везение, а человек, который сможет одобрить или утешить',
                     '4. Вам показали шарж или пародию на вас. Вы:'
                     '\n\nA) рассмеетесь и обрадуетесь тому, что в вас есть что-то оригинальное'
                     '\nБ) тоже попытаетесь найти что-то смешное в вашем партнере и высмеять его'
                     '\nВ) обидитесь, но не подадите вида',
                     '5. Вы всегда спешите, вам не хватает времени или вы беретесь за выполнение заданий, превышающих возможности одного человека?'
                     '\n\nA) Да'
                     '\nБ) Нет'
                     '\nВ) Не знаю',
                     '6. Вы выбираете духи в подарок подруге. Купите.'
                     '\n\nA) духи, которые нравятся вам'
                     '\nБ) духи, которым, как вы думаете, будет рада подруга, хотя вам лично они не нравятся'
                     '\nВ) духи, которые рекламировали в недавней телепередаче.',
                     '7. Вы любите представлять себе различные ситуации, в которых вы ведете себя совершенно иначе, чем в жизни?'
                     '\n\nA) да'
                     '\nБ) нет'
                     '\nВ) не знаю',
                     '8. Задевает ли вас, когда ваши коллеги (особенно молодые) добиваются большего успеха чем вы?'
                     '\n\nA) да'
                     '\nБ) нет'
                     '\nВ) иногда',
                     '9. Доставляет ли вам удовольствие возражать кому-либо?'
                     '\n\nA) да'
                     '\nБ) нет'
                     '\nВ) не знаю',
                     '10. Закройте глаза и попытайтесь представить себе 3 цвета:'
                     '\n\nA) голубой'
                     '\nБ) желтый'
                     '\nВ) красный']


# Keyboards
selfesteem_answer0 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='selfesteem_answer_0'),
    InlineKeyboardButton('Б', callback_data='selfesteem_answer_1'))

selfesteem_answer1 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='selfesteem_answer_0'),
    InlineKeyboardButton('Б', callback_data='selfesteem_answer_1'))

selfesteem_answer2 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='selfesteem_answer_0'),
    InlineKeyboardButton('Б', callback_data='selfesteem_answer_1'),
    InlineKeyboardButton('В', callback_data='selfesteem_answer_2'))

selfesteem_answer3 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='selfesteem_answer_0'),
    InlineKeyboardButton('Б', callback_data='selfesteem_answer_1'),
    InlineKeyboardButton('В', callback_data='selfesteem_answer_2'))

selfesteem_answer4 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='selfesteem_answer_0'),
    InlineKeyboardButton('Б', callback_data='selfesteem_answer_1'),
    InlineKeyboardButton('В', callback_data='selfesteem_answer_2'))

selfesteem_answer5 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='selfesteem_answer_0'),
    InlineKeyboardButton('Б', callback_data='selfesteem_answer_1'),
    InlineKeyboardButton('В', callback_data='selfesteem_answer_2'))

selfesteem_answer6 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='selfesteem_answer_0'),
    InlineKeyboardButton('Б', callback_data='selfesteem_answer_1'),
    InlineKeyboardButton('В', callback_data='selfesteem_answer_2'))

selfesteem_answer7 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='selfesteem_answer_0'),
    InlineKeyboardButton('Б', callback_data='selfesteem_answer_1'),
    InlineKeyboardButton('В', callback_data='selfesteem_answer_2'))

selfesteem_answer8 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='selfesteem_answer_0'),
    InlineKeyboardButton('Б', callback_data='selfesteem_answer_1'),
    InlineKeyboardButton('В', callback_data='selfesteem_answer_0'))

selfesteem_answer9 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='selfesteem_answer_0'),
    InlineKeyboardButton('Б', callback_data='selfesteem_answer_1'),
    InlineKeyboardButton('В', callback_data='selfesteem_answer_2'))

selfesteem_answer_keyboards = [selfesteem_answer0, selfesteem_answer1, selfesteem_answer2, selfesteem_answer3, selfesteem_answer4, selfesteem_answer5, selfesteem_answer6, selfesteem_answer7, selfesteem_answer8, selfesteem_answer9]


async def pretest_selfesteem(message: types.message, state: FSMContext):
    await FSM_classes.MultiDialog.test_selfesteem.set()
    await pre_points_test_selfesteem(user_id=message.from_user.id, username=message.from_user.username)
    async with state.proxy() as data:
        data['count'] = 0
    async with state.proxy() as data:
        data['points'] = 0
    await points_test_selfesteem(state, user_id=message.from_user.id)
    await state.finish()
    await bot.send_message(message.from_user.id, '50-38 баллов. Вы довольны собой и уверены в себе. У вас большая потребность доминировать над людьми, любите подчеркивать свое "я", выделять свое мнение. Вам безразлично то, что о вас говорят, но сами вы имеете склонность критиковать других. Чем больше у вас баллов, тем больше вам подходит определение: "Вы любите себя, но не любите других". Но у вас есть один недостаток: слишком серьезно к себе относитесь, не принимаете никакой критической информации. И даже если результаты теста вам не понравятся, скорее всего, вы "защититесь" утверждением "все вокруг календари". А жаль...'
                                                 '\n37-24 балла. Вы живете в согласии с собой, знаете себя и можете себе доверять. Обладаете ценным умением находить выход из трудных ситуаций как личного характера, так и во взаимоотношениях с людьми. Формулу вашего отношения к себе и окружающим можно выразить словами: "Доволен собой, доволен другими". У вас нормальная здоровая самооценка, вы умеете быть для себя поддержкой и источником силы и, что самое главное, не за счет других.'
                                                 '\n\n23-10 баллов. Очевидно, вы недовольны собой, вас мучают сомнения и неудовлетворенность своим интеллектом, способностями, достижениями, своей внешностью, возрастом, полом... Остановитесь! Кто сказал, что любить себя плохо? Кто внушил вам, что думающий человек должен быть постоянно собой недоволен? Разумеется, никто не требует от вас самодовольства, но вы должны принимать себя, уважать себя, поддерживать в себе этот огонек.', reply_markup=types.ReplyKeyboardRemove())
    await asyncio.sleep(5)
    await bot.send_message(message.from_user.id, text=selfesteem_questions[0], reply_markup=selfesteem_answer0)
