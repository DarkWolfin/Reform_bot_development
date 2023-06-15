from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aioschedule as schedule

from aiogram.utils.exceptions import BotBlocked

from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())


quick_help_menu = ReplyKeyboardMarkup(row_width=1).add(
    KeyboardButton('🤯 Истерика'),
    KeyboardButton('😢 Грусть'),
    KeyboardButton('😠 Раздражение'),
    KeyboardButton('😔 Упадок сил'),
    KeyboardButton('🙄 Безразличие'),
    KeyboardButton('😩 Отчаяние'),
    KeyboardButton('😧 Страх'))

hysterics0 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='hysterics0'))
sadness0 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='sadness0'))
irritation0 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='irritation0'))
prostration0 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='prostration0'))
indifference0 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='indifference0'))
despair0 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='despair0'))
fear0 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='fear0'))

async def all_way_quick_help(message:types.Message):
    if message.text == '🤯 Истерика':
        await bot.send_message(message.from_user.id,
                               text='Я знаю, что ты стараешься и уделяешь много внимания клиентам. \nСегодня у тебя трудный день, однако не стоит заполнять себя этими мыслями',
                               reply_markup=hysterics0)
    if message.text == '😢 Грусть':
        await bot.send_message(message.from_user.id,
                               text='Я знаю, что ты стараешься и уделяешь много внимания клиентам. \nСегодня у тебя трудный день, однако не стоит заполнять себя этими мыслями',
                               reply_markup=sadness0)
    if message.text == '😠 Раздражение':
        await bot.send_message(message.from_user.id,
                               text='У тебя сегодня были по-настоящему трудные беседы с клиентами. \nНе забывай, ты делаешь важную работу, и твои усилия очень ценятся',
                               reply_markup=irritation0)
    if message.text == '😔 Упадок сил':
        await bot.send_message(message.from_user.id,
                               text='Работа в call-центре может быть очень истощающей. \nНе забывай, ты делаешь большое количество звонков, чтобы помогать людям, это очень важная работа',
                               reply_markup=prostration0)
    if message.text == '🙄 Безразличие':
        await bot.send_message(message.from_user.id,
                               text='Тебе может казаться, что некоторые вопросы повторяются, а время потрачено зря. \nПомни, что каждый звонок очень важен для клиентов',
                               reply_markup=indifference0)
    if message.text == '😩 Отчаяние':
        await bot.send_message(message.from_user.id,
                               text='Понимаю, что ты встречаешься с "трудными" и порой не очень дружелюбными клиентами. \nДавай вместе посмотрим на возможные пути решения',
                               reply_markup=despair0)
    if message.text == '😧 Страх':
        await bot.send_message(message.from_user.id,
                               text='Понимаю, что ты встречаешься с "трудными" и порой не очень дружелюбными клиентами. \nДавай вместе посмотрим на возможные пути решения',
                               reply_markup=fear0)


hysterics1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='hysterics1'))
sadness1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='sadness1'))
irritation1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='irritation1'))
prostration1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='prostration1'))
indifference1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='indifference1'))
despair1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='despair1'))
fear1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='fear1'))

hysterics2 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='hysterics2'))
sadness2 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='sadness2'))
irritation2 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='irritation2'))
prostration2 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='prostration2'))
indifference2 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='indifference2'))
despair2 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='despair2'))
fear2 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='fear2'))

async def all_way_callback_quick_help(callback_query: types.CallbackQuery):
    if callback_query.data[:-1] == 'hysteric':
        if callback_query.data[-1] == '0':
            await bot.send_message(callback_query.from_user.id,
                                   text='Самое важное сейчас - успокоиться. Глубоко вдохни и постепенно начинай выравнивать своё дыхание',
                                   reply_markup=hysterics1)
        if callback_query.data[-1] == '1':
            await bot.send_message(callback_query.from_user.id,
                                   text='Я понимаю, что сейчас ситуация накаляется.Давай сфокусируемся на том, что можно сделать, чтобы помочь решить проблему',
                                   reply_markup=hysterics2)
    elif callback_query.data[:-1] == 'sadness':
        if callback_query.data[-1] == '0':
            await bot.send_message(callback_query.from_user.id,
                                   text='Грусть - это нормальное чувство, не нужно это скрывать, ты не одинок. Если нужно, найди место, где ты сможешь отдохнуть и восстановиться',
                                   reply_markup=sadness1)
        if callback_query.data[-1] == '1':
            await bot.send_message(callback_query.from_user.id,
                                   text='Ты очень отзывчивый человек, и твоя эмпатия помогает клиентам почувствовать себя важными',
                                   reply_markup=sadness2)
    elif callback_query.data[:-1] == 'irritation':
        if callback_query.data[-1] == '0':
            await bot.send_message(callback_query.from_user.id,
                                   text='Попробуй найти способ расслабиться, дыши глубоко и делай небольшие паузы. Помни, что клиенты могут испытывать свои трудности, и твоя поддержка им очень важна',
                                   reply_markup=irritation1)
        if callback_query.data[-1] == '1':
            await bot.send_message(callback_query.from_user.id,
                                   text=' Ты важная часть команды, и я готов помочь тебе разобраться с любыми трудностями, с которыми ты сталкиваешься. Можем вместе обсудить пути борьбы с раздражением',
                                   reply_markup=irritation2)
    elif callback_query.data[:-1] == 'prostration':
        if callback_query.data[-1] == '0':
            await bot.send_message(callback_query.from_user.id,
                                   text='Ты уже проделал много работы и справился со многими вызовами. Позволь себе небольшую паузу, чтобы отдохнуть и восстановить энергию. Помни, что ты ценен и твоя работа имеет значение',
                                   reply_markup=prostration1)
        if callback_query.data[-1] == '1':
            await bot.send_message(callback_query.from_user.id,
                                   text='Знаю, что иногда бывает сложно поддерживать позитивный настрой, но не забывай, что важно заботиться о своем благополучии. Если ты не против, я помогу тебе найти способы восстановления энергии и поддержания баланса в течение дня',
                                   reply_markup=prostration2)
    elif callback_query.data[:-1] == 'indifference':
        if callback_query.data[-1] == '0':
            await bot.send_message(callback_query.from_user.id,
                                   text='Если тебе кажется, что потерял интерес или мотивацию, попробуй вспомнить, какое влияние ты оказываешь на клиентов и их проблемы. Необходимо придать своей работе новый смысл и постараться найти в ней радость и удовлетворение',
                                   reply_markup=indifference1)
        if callback_query.data[-1] == '1':
            await bot.send_message(callback_query.from_user.id,
                                   text='Сейчас тебе может казаться, что каждый звонок одинаковый. Но помни, что твоя работа имеет значение для каждого клиента, которому ты помогаешь. Давай найдем способы, чтобы каждый звонок был для тебя интересным, а значимость твоей работы была наглядна видна',
                                   reply_markup=indifference2)
    elif callback_query.data[:-1] == 'despair':
        if callback_query.data[-1] == '0':
            await bot.send_message(callback_query.from_user.id,
                                   text='Время от времени мы можем чувствовать отчаяние, особенно когда сталкиваемся с трудностями. Помни, что даже в трудных ситуациях есть решения',
                                   reply_markup=despair1)
        if callback_query.data[-1] == '1':
            await bot.send_message(callback_query.from_user.id,
                                   text='Знай, я здесь, чтобы поддержать тебя, и вместе найти способы преодолеть трудные моменты. Помни, что ты не один и всегда можешь обратиться за поддержкой!',
                                   reply_markup=despair2)
    elif callback_query.data[:-1] == 'fear':
        if callback_query.data[-1] == '0':
            await bot.send_message(callback_query.from_user.id,
                                   text='Страх может быть естественной реакцией на сложные ситуации. Постепенно преодолевай свои страхи, шаг за шагом',
                                   reply_markup=fear1)
        if callback_query.data[-1] == '1':
            await bot.send_message(callback_query.from_user.id,
                                   text='Знай, я здесь, чтобы поддержать тебя, и вместе найти способы преодолеть трудные моменты. Помни, что ты не один и всегда можешь обратиться за поддержкой!',
                                   reply_markup=fear2)


def register_handlers_Psy_Weariness(dp: Dispatcher):
    dp.register_callback_query_handler(
        all_way_callback_quick_help, text=['hysterics0', 'sadness0', 'irritation0', 'prostration0', 'indifference0', 'despair0', 'fear0'])

