import FSM_classes
import Markups
from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import PopTests
import PsyTests

from Token import Token
from Storage import storage

bot = Bot(Token)
dp = Dispatcher(bot, storage=storage)


async def pretest(message: types.message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           'В этом разделе находятся психологические и интересные популярные тесты.'
                           '\n\nПсихологические тесты предназначены для определения уровня тревожности, стресса и депрессии. '
                           '\nЭти тесты позволят определить Ваше психологическое состояние с помощью шкал и метрик, соответствующим состояниям тревожности, стресса и депрессии.'
                           '\n\nПопулярные тесты помогут лучше понять себя, получить заряд позитива и настроить себя на нужный лад.'
                           '\nВыберите тип, который Вас интересует, чтобы перейти к списку тестов', reply_markup=Markups.type_of_tests)


async def type_test(message: types.message, state: FSMContext):

    if message.text == 'Психологические тесты':
        await bot.send_message(message.from_user.id,
                               'Вам доступны тесты "Хроническая усталость" и "Личная самоэффекстивность".'
                               '\nОстальные тесты доступны с подпиской (если интересуют подробности, нажмите на закрытый тест)'
                               '\nСоветуем Вам сначала пройти бесплатные тесты, чтобы оценить их пользу',
                               reply_markup=Markups.psy_tests)
    if message.text == 'Популярные тесты':
        await bot.send_message(message.from_user.id,
                               'Вам доступны тесты "Управляю ли я своей жизнью?" и "Мои скрытые таланты и способности".'
                               '\nОстальные тесты доступны с подпиской (если интересуют подробности, нажмите на закрытый тест)'
                               '\nСоветуем Вам сначала пройти бесплатные тесты и почуствовать, насколько интересно узнавать новое о себе',
                               reply_markup=Markups.pop_tests)

    if message.text == 'Хроническая усталость':
        await FSM_classes.MultiDialog.test_weariness.set()
        await PsyTests.Psy_Weariness.pretest_weariness(message, state)
    if message.text == 'Устойчивость к стрессу':
        await FSM_classes.MultiDialog.test_stress.set()
        await PsyTests.Psy_stress.pretest_stress(message, state)
    if message.text == 'Личная самоэффективность':
        await FSM_classes.MultiDialog.test_selfefficacy.set()
        await PsyTests.Psy_selfefficacy.pretest_selfefficacy(message, state)

    if message.text == 'Управляю ли я своей жизнью?':
        await FSM_classes.MultiDialog.test_control.set()
        await PopTests.Pop_Control.pretest_control(message, state)
    if message.text == 'Мой тип личности':
        await FSM_classes.MultiDialog.test_typeperson.set()
        await PopTests.Pop_Typeperson.pretest_typeperson(message, state)
