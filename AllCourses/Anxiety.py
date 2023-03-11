from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())

from Databases import course_anxiety_db

import Markups
import FSM_classes

async def pre_course_anxiety(message: types.Message, state: FSMContext):
    Anxiety_kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Начать курс', callback_data='Anxiety1'))
    await bot.send_message(message.from_user.id,
                           text='Добро пожаловать на курс "Борьба с тревогой"',
                           parse_mode='html', reply_markup=Markups.backCourseRe)
    await bot.send_message(message.from_user.id,
                           text='Наша главная задача - сбросить эмоциональное напряжение и обеспечить гармонизацию для нашего организма.',
                           parse_mode='html', reply_markup=Anxiety_kb)


async def Course_Anxiety(callback_query: types.CallbackQuery, state: FSMContext):
    point = callback_query.data[-1]
    if point == '1':
        btn1 = InlineKeyboardButton('Приступить к практике', callback_data='Anxiety2')
        Anxiety_kb = InlineKeyboardMarkup(row_width=1)
        Anxiety_kb.add(btn1)
        await bot.send_message(callback_query.from_user.id, 'В первую очередь нам нужно успокоиться, чтобы чувствовать себя комфортно и защищенно. '
                                                            '\nДля этого необходимо выполнить дыхательную практику. '
                                                            '\nПодобное упражнение поможет успокоить эмоции и разгрузить нервную систему.',
                               parse_mode='html', reply_markup=Anxiety_kb)
    if point == '2':
        btn1 = InlineKeyboardButton('Упражнение выполнено!', callback_data='Anxiety3')
        Anxiety_kb = InlineKeyboardMarkup(row_width=1)
        Anxiety_kb.add(btn1)
        await bot.send_message(callback_query.from_user.id,
                               "Вдох, выдох и пауза примерно равны друг другу по длительности, комфортный ритм – примерно 4 секунд")
        ExVisualAudio2 = open('Exercises/Дыхание квадрат.mp3', 'rb')
        photo = open('Exercises/Квадрат дыхания.jpg', 'rb')
        await bot.send_photo(callback_query.from_user.id, photo)
        await bot.send_audio(callback_query.from_user.id, ExVisualAudio2, reply_markup=Anxiety_kb)
    if point == '3':
        btn1 = InlineKeyboardButton('Продолжить', callback_data='Anxiety4')
        Anxiety_kb = InlineKeyboardMarkup(row_width=1)
        Anxiety_kb.add(btn1)
        await bot.send_message(callback_query.from_user.id, 'Тревожность - это естественная реакция на угрожающие ситуации и является своего рода функцией выживания. '
                                                            'Тревожность может ощущаться в разной степени интенсивности, от неясного беспокойства до сильных телесных симптомов или панических атак, '
                                                            'когда возникает ощущение, что вы можете упасть в обморок. Эпизод тревожности всегда проходит, но может вернуться.',
                               parse_mode='html', reply_markup=Anxiety_kb)
    if point == '4':
        btn1 = InlineKeyboardButton('1', callback_data='Anxiety5')
        btn2 = InlineKeyboardButton('2', callback_data='Anxiety5')
        btn3 = InlineKeyboardButton('3', callback_data='Anxiety5')
        btn4 = InlineKeyboardButton('4', callback_data='Anxiety5')
        btn5 = InlineKeyboardButton('5', callback_data='Anxiety5')
        btn6 = InlineKeyboardButton('6', callback_data='Anxiety5')
        btn7 = InlineKeyboardButton('7', callback_data='Anxiety5')
        btn8 = InlineKeyboardButton('8', callback_data='Anxiety5')
        btn9 = InlineKeyboardButton('9', callback_data='Anxiety5')
        btn10 = InlineKeyboardButton('10', callback_data='Anxiety5')
        Anxiety_kb = InlineKeyboardMarkup(row_width=5)
        Anxiety_kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10)
        await bot.send_message(callback_query.from_user.id, 'Давайте определим ваше актуальное состояние. '
                                                            '\nДля этого по 10-ти бальной шкале оцените свое состояние, где 1 - не ощущаю беспокойства, а 10 - паническая атака.',
                               parse_mode='html', reply_markup=Anxiety_kb)
    if point == '5':
        btn1 = InlineKeyboardButton('Продолжай', callback_data='Anxiety6')
        Anxiety_kb = InlineKeyboardMarkup(row_width=1)
        Anxiety_kb.add(btn1)
        await bot.send_message(callback_query.from_user.id, 'Спасибо за ответ! '
                                                            '\nКогда возникает тревожность, кажется, что это никогда не пройдёт, и бывают мысли «я схожу с ума». '
                                                            '\nВ этот момент важно помнить, что это не так! '
                                                            'Через некоторое время тревожность всегда проходит, и это не опасное состояние, даже если вы в этом уверены во время эпизода.',
                               parse_mode='html', reply_markup=Anxiety_kb)
    if point == '6':
        btn1 = InlineKeyboardButton('Дальше', callback_data='Anxiety7')
        Anxiety_kb = InlineKeyboardMarkup(row_width=1)
        Anxiety_kb.add(btn1)
        await bot.send_message(callback_query.from_user.id, 'Тревожность может быть вызвана, например, мыслью или чувством, которое вас пугает или заставляет вас чувствовать себя под угрозой, бессильным, несчастным или никому не нужным. '
                                                            '\nИногда тревожность может быть связана с высокими требованиями, чувством стыда или вины. Часто может возникать мысль, что вы странный и с вами что-то не так.'
                                                            '\nТревожность также может начаться, если вы чувствуете себя обманутым или покинутым. '
                                                            '\nТакже может возникнуть, если вы рискуете потерять что-либо важное для себя, например, безопасность, статус или любовь',
                               parse_mode='html', reply_markup=Anxiety_kb)
    if point == '7':
        btn1 = InlineKeyboardButton('Поработаем с мыслями', callback_data='Anxiety8')
        Anxiety_kb = InlineKeyboardMarkup(row_width=1)
        Anxiety_kb.add(btn1)
        await bot.send_message(callback_query.from_user.id, 'Страх и тревога - нормальные и естественные эмоциональные состояния.'
                                                            'Страх ориентирован на настоящий момент, тревога - на будущее.'
                                                            '\n\nЕсть ошибки мышления и поведенческие стратегии, которые превращают тревогу в проблему, влияющую на повседневную жизнь.'
                                                            '\n\nЗнакомство со своей тревогой, триггерами, проявлениями - важное условие для изменения этих неэффективных стратегий.',
                               parse_mode='html', reply_markup=Anxiety_kb)
    if point == '8':
        btn1 = InlineKeyboardButton('Хорошо, приступим!', callback_data='Anxiety9')
        Anxiety_kb = InlineKeyboardMarkup(row_width=1)
        Anxiety_kb.add(btn1)
        await bot.send_message(callback_query.from_user.id, 'Теперь нам необходимо поработать с вашими мыслями. '
                                                            'Ориентировочное время выполнения 20 минут',
                               parse_mode='html', reply_markup=Anxiety_kb)
    if point == '9':
        btn1 = InlineKeyboardButton('Да', callback_data='Anxietya')
        btn2 = InlineKeyboardButton('Не думаю', callback_data='Anxietyb')
        Anxiety_kb = InlineKeyboardMarkup(row_width=1)
        Anxiety_kb.add(btn1, btn2)
        await bot.send_message(callback_query.from_user.id, 'Вспомните ситуацию, которая вызвала у вас чувство тревоги в последнее время '
                                                            '\nПонаблюдайте за собой. В каких ситуациях вы заметили у себя тревожные мысли? '
                                                            'И какая у вас при этом была реакция?'
                                                            '\nТеперь скажите, подвластна ли контролю ситуация которая вызывает у вас тревогу?',
                               parse_mode='html', reply_markup=Anxiety_kb)
    if point == 'a':
        btn1 = InlineKeyboardButton('Продолжай', callback_data='Anxietyc')
        Anxiety_kb = InlineKeyboardMarkup(row_width=1)
        Anxiety_kb.add(btn1)
        await bot.send_message(callback_query.from_user.id, 'В этом случае поможем работать над тем, что находится в зоне контроля',
                               parse_mode='html', reply_markup=Anxiety_kb)
    if point == 'b':
        btn1 = InlineKeyboardButton('Продолжай', callback_data='Anxietyc')
        Anxiety_kb = InlineKeyboardMarkup(row_width=1)
        Anxiety_kb.add(btn1)
        await bot.send_message(callback_query.from_user.id, 'В этом случае нам нужно научиться принимать то, что мы не контролируем',
                               parse_mode='html', reply_markup=Anxiety_kb)
    if point == 'c':
        btn1 = InlineKeyboardButton('Да, узнать больше о подписке', callback_data='Anxietyd')
        btn2 = InlineKeyboardButton('Нет', callback_data='Anxietye')
        Anxiety_kb = InlineKeyboardMarkup(row_width=1)
        Anxiety_kb.add(btn1, btn2)
        await bot.send_message(callback_query.from_user.id, 'Полный доступ доступен в платной версии. '
                                                            '\n\nВ полной версии:'
                                                            '\n❇️ 25 медитаций'
                                                            '\n❇️ 10 дыхательных практик'
                                                            '\n❇️ Таймер Помодоро'
                                                            '\n❇️ Система ежедневных напоминаний и мотивациных подборок'
                                                            '\n❇️ Рекомендации по сну, питанию и отдыху от ведущих специалистов'
                                                            '\n❇️ Заинтересовала ли вас полная версия? '
                                                            '\n❇️ Хотели бы вы оформить подписку?',
                               parse_mode='html', reply_markup=Anxiety_kb)
    if point == 'd':
        btn1 = InlineKeyboardButton('Перейти в главное меню', callback_data='Main_menu')
        Anxiety_kb = InlineKeyboardMarkup()
        Anxiety_kb.add(btn1)
        await bot.send_message(callback_query.from_user.id, 'Отлично! Скоро будет продолжение и мы вас оповестим!',
                               parse_mode='html', reply_markup=Anxiety_kb)
        await course_anxiety_db(user_id=callback_query.from_user.id, username=callback_query.from_user.username, interested='Да')

    if point == 'e':
        btn1 = InlineKeyboardButton('Перейти в главное меню', callback_data='Main_menu')
        Anxiety_kb = InlineKeyboardMarkup()
        Anxiety_kb.add(btn1)
        await bot.send_message(callback_query.from_user.id, 'Жаль, что вам не понравилось((( '
                                                            '\nСкоро будет продолжение и мы покажем вам контент, который точно понравится!',
                               parse_mode='html', reply_markup=Anxiety_kb)
        await course_anxiety_db(user_id=callback_query.from_user.id, username=callback_query.from_user.username, interested='Нет')


def register_handlers_course_Anxiety(dp: Dispatcher):
    dp.register_callback_query_handler(Course_Anxiety, text=['Anxiety1', 'Anxiety2', 'Anxiety3', 'Anxiety4', 'Anxiety5', 'Anxiety6', 'Anxiety7', 'Anxiety8', 'Anxiety9', 'Anxietya', 'Anxietyb', 'Anxietyc', 'Anxietyd', 'Anxietye'])

