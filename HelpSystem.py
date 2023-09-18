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

import quick_help
from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())

import Markups
import FSM_classes
from Database import help_system_good, help_system_norm, help_system_bad, help_system_agreement


bad_condition_questions = ['Есть ли задачи, которые вызывают у вас беспокойство или стресс?',
                           'Удается ли вам эффективно справляться со своей рабочей нагрузкой',
                           'У вас достаточно времени на личную жизнь и отдых вне работы?',
                           'Удается лм вам открыто и свободно общаться с вашими коллегами?',
                           'Возникают ли у вас конфликты или напряженные ситуации?',
                           'Удобное ли у вас рабочее место?',
                           'У вас есть личные проблемы или события, которые вас беспокоят или тревожат в настоящее время?',
                           'Существует ли что-то, что вызывает у вас беспокойство или тревожит в настоящее время?']

async def choose_helpsystem(message: types.Message, state: FSMContext):
    if message.text == 'Хорошо 😀':
        await help_system_good(user_id=message.from_user.id)
        await bot.send_message(message.from_user.id, 'Это замечательно!', reply_markup=ReplyKeyboardRemove())
        await bot.send_message(message.from_user.id,'Желаете попробовать практику благодарности? Рассказать поподробнее?', InlineKeyboardMarkup(row_width=2). add(InlineKeyboardButton('Да', callback_data='try_practice_gy'), InlineKeyboardButton('Нет', callback_data='try_practice_gn')))
        await state.set_state(FSM_classes.HelpSystem.good_condition)
    elif message.text == 'Нормально 🙂':
        await help_system_norm(user_id=message.from_user.id)
        await bot.send_message(message.from_user.id, 'Я рад, что у вас всё хорошо! Но что-то всё-таки вас беспокоит..', reply_markup=ReplyKeyboardRemove())
        await bot.send_message(message.from_user.id, 'Вы бы хотели улучшить ваше состояние?', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Да', callback_data='norm_condition_0_y'), InlineKeyboardButton('Нет, меня всё устраивает', callback_data='norm_condition_0_n')))
        await state.set_state(FSM_classes.HelpSystem.norm_condition)
    elif message.text == 'Плохо 😢':
        await help_system_bad(user_id=message.from_user.id)
        await bot.send_message(message.from_user.id, 'Понимаю, что ваши ощущения важны, и я готов помочь! '
                                                     '\nДавайте разберёмся с чем связано ваше плохое самочувствие?'
                                                     '\n\nЯ задам вам несколько вопросов, отвечайте "Да", если вас это беспокоит!',
                               reply_markup=ReplyKeyboardRemove())
        await state.set_state(FSM_classes.HelpSystem.bad_condition)
        await bot.send_message(message.from_user.id, 'Есть ли задачи, которые вызывают у вас беспокойство или стресс?', reply_markup=InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Да', callback_data='bad_condition_1_0_y'), InlineKeyboardButton('Нет', callback_data='bad_condition_1_0_n')))


async def norm_condition(callback_query: types.CallbackQuery, state: FSMContext):
    db_helpsys = sqlite3.connect('Databases/Help_system.db')
    cur_helpsys = db_helpsys.cursor()
    if callback_query.data.startswith('norm_condition_0_'):
        cur_helpsys.execute("UPDATE norm SET better = ? WHERE user_id = ?", (callback_query.data[-1], callback_query.from_user.id))
        if callback_query.data[-1] == 'y':
            await bot.send_message(callback_query.from_user.id, 'Регулярные физические упражнения, такие как занятия спортом, йога или даже ежедневные прогулки, могут улучшить физическое и эмоциональное состояние. '
                                                            '\nУдается ли вам их выполнять?', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Нет, но хотелось бы это исправить', callback_data='norm_condition_1_i'), InlineKeyboardButton('Да', callback_data='norm_condition_1_y'), InlineKeyboardButton('Нет, меня всё устраивает', callback_data='norm_condition_1_n')))
        else:
            await bot.send_message(callback_query.from_user.id, 'Очень жаль, что вам это неинтересно((')
            await state.set_state(FSM_classes.MultiDialog.menu)
        db_helpsys.commit()

    elif callback_query.data[-3] == '1':
        if callback_query.data[-1] == 'y':
            await bot.send_message(callback_query.from_user.id,'Отлично, тогда идем дальше!')
            await bot.send_message(callback_query.from_user.id, 'Уравновешенное питание с разнообразными продуктами может оказать положительное воздействие на ваше здоровье и настроение! '
                                                                '\nСтарайтесь употреблять свежие фрукты и овощи, богатые белком продукты и здоровые жиры!'
                                                                '\nУдается ли вам это?', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Нет, но хотелось бы это исправить', callback_data='norm_condition_3_i'), InlineKeyboardButton('Да', callback_data='norm_condition_3_y'), InlineKeyboardButton('Нет, меня всё устраивает', callback_data='norm_condition_3_n')))
            cur_helpsys.execute("UPDATE norm SET sport = ? WHERE user_id = ?",
                                ('Да', callback_query.from_user.id))
        elif callback_query.data[-3] == 'n':
            await bot.send_message(callback_query.from_user.id, 'Принято, тогда идем дальше!')
            await bot.send_message(callback_query.from_user.id,
                                   'Уравновешенное питание с разнообразными продуктами может оказать положительное воздействие на ваше здоровье и настроение! '
                                   '\nСтарайтесь употреблять свежие фрукты и овощи, богатые белком продукты и здоровые жиры!'
                                   '\nУдается ли вам это?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                    InlineKeyboardButton('Нет, но хотелось бы это исправить', callback_data='norm_condition_3_i'),
                    InlineKeyboardButton('Да', callback_data='norm_condition_3_y'),
                    InlineKeyboardButton('Нет, меня всё устраивает', callback_data='norm_condition_3_n')))
            cur_helpsys.execute("UPDATE norm SET sport = ? WHERE user_id = ?",
                                ('Нет', callback_query.from_user.id))
        else:
            await bot.send_message(callback_query.from_user.id, 'Как вы думаете, в чём причина этого?', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Не хватает времени', callback_data='norm_condition_2_t'), InlineKeyboardButton('Нет мотивации', callback_data='norm_condition_2_m'), InlineKeyboardButton('Всё вместе', callback_data='norm_condition_2_b')))
            cur_helpsys.execute("UPDATE norm SET sport = ? WHERE user_id = ?",
                                ('Улучшить', callback_query.from_user.id))
        db_helpsys.commit()

    elif callback_query.data[-3] == '2':
        if callback_query.data[-1] == 't':
            await bot.send_message(callback_query.from_user.id, 'Даже если у вас ограничено время, есть несколько способов внедрить регулярные физические упражнения в вашу повседневную жизнь:'
                                                                '\n\n1. - <b>Краткие интенсивные тренировки:</b> Вы можете проводить короткие, но интенсивные тренировки, которые занимают всего несколько минут, но способствуют улучшению физической формы и здоровья.'
                                                                '\n2. - <b>Интеграция в рутину:</b> Используйте моменты из вашей обыденной жизни для физической активности. Например, используйте лестницу вместо лифта, делайте упражнения во время перерывов на работе или даже во время просмотра телевизора.'
                                                                '\n3. - <b>Прогулки:</b> Ежедневные прогулки, даже небольшие, могут быть отличным способом поддерживать активность. Вы можете пройти больше шагов, выбирая пешеходные маршруты вместо автомобиля или общественного транспорта.'
                                                                '\n4. - <b>Медитация и йога:</b> Практикуйте короткие медитации или мини-йога-сессии для физической и эмоциональной релаксации. Даже несколько минут в день могут оказать положительное воздействие.'
                                                                '\n5. - <b>Планирование:</b> Запишите физическую активность в свой расписание и придерживайтесь этого плана. Это поможет вам выделить время для занятий спортом или других видов физической активности.'
                                                                '\n\nПомните, что даже небольшие изменения в вашей повседневной жизни могут привести к улучшению физического и эмоционального состояния. <b>Главное - постоянство и регулярность!</b>', parse_mode='html')
            await asyncio.sleep(4)
            await bot.send_message(callback_query.from_user.id, 'Для начала, мы можем начать с небольших утренних упражнений и разминки в течение рабочего дня, которые можно интегрировать в рабочий ритм. '
                                                                '\nВы бы хотели попробовать подобную практику?', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Да', callback_data='agreement_mailing_help_s_n_y'), InlineKeyboardButton('Нет, меня всё устраивает', callback_data='agreement_mailing_help_s_n_n')))
            cur_helpsys.execute("UPDATE norm SET cause_sport = ? WHERE user_id = ?",
                                ('Время', callback_query.from_user.id))
        if callback_query.data[-1] == 'm':
            await bot.send_message(callback_query.from_user.id,
                                   'Для начала, мы можем начать с небольших утренних упражнений и разминки в течение рабочего дня, которые можно интегрировать в рабочий ритм. '
                                   '\nВы бы хотели попробовать подобную практику?',
                                   reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                       InlineKeyboardButton('Да', callback_data='agreement_mailing_help_s_n_y'),
                                       InlineKeyboardButton('Нет, меня всё устраивает',
                                                            callback_data='agreement_mailing_help_s_n_n')))
            cur_helpsys.execute("UPDATE norm SET cause_sport = ? WHERE user_id = ?",
                                ('Мотивация', callback_query.from_user.id))
        if callback_query.data[-1] == 'b':
            await bot.send_message(callback_query.from_user.id,
                                   'Даже если у вас ограничено время, есть несколько способов внедрить регулярные физические упражнения в вашу повседневную жизнь:'
                                   '\n\n1. - <b>Краткие интенсивные тренировки:</b> Вы можете проводить короткие, но интенсивные тренировки, которые занимают всего несколько минут, но способствуют улучшению физической формы и здоровья.'
                                   '\n2. - <b>Интеграция в рутину:</b> Используйте моменты из вашей обыденной жизни для физической активности. Например, используйте лестницу вместо лифта, делайте упражнения во время перерывов на работе или даже во время просмотра телевизора.'
                                   '\n3. - <b>Прогулки:</b> Ежедневные прогулки, даже небольшие, могут быть отличным способом поддерживать активность. Вы можете пройти больше шагов, выбирая пешеходные маршруты вместо автомобиля или общественного транспорта.'
                                   '\n4. - <b>Медитация и йога:</b> Практикуйте короткие медитации или мини-йога-сессии для физической и эмоциональной релаксации. Даже несколько минут в день могут оказать положительное воздействие.'
                                   '\n5. - <b>Планирование:</b> Запишите физическую активность в свой расписание и придерживайтесь этого плана. Это поможет вам выделить время для занятий спортом или других видов физической активности.'
                                   '\n\nПомните, что даже небольшие изменения в вашей повседневной жизни могут привести к улучшению физического и эмоционального состояния. <b>Главное - постоянство и регулярность!</b>',
                                   parse_mode='html')
            await asyncio.sleep(4)
            await bot.send_message(callback_query.from_user.id,
                                   'Для начала, мы можем начать с небольших утренних упражнений и разминки в течение рабочего дня, которые можно интегрировать в рабочий ритм. '
                                   '\nВы бы хотели попробовать подобную практику, реализованную в качестве рассылок с упражнениями и советами по их выполнению?',
                                   reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                       InlineKeyboardButton('Да', callback_data='agreement_mailing_help_s_n_y'),
                                       InlineKeyboardButton('Нет, меня всё устраивает',
                                                            callback_data='agreement_mailing_help_s_n_n')))
            cur_helpsys.execute("UPDATE norm SET cause_sport = ? WHERE user_id = ?",
                                ('Оба', callback_query.from_user.id))
        db_helpsys.commit()

    elif callback_query.data[-3] == '3':
        if callback_query.data[-1] == 'y':
            await bot.send_message(callback_query.from_user.id, 'Отлично, тогда идем дальше!')
            await bot.send_message(callback_query.from_user.id,
                                   'Уделяйте внимание качеству сна! Регулярный и полноценный сон способствует восстановлению энергии и улучшению настроения!'
                                   '\nУдается ли вам хорошо спать и высыпаться?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                    InlineKeyboardButton('Да', callback_data='norm_condition_4_y'),
                    InlineKeyboardButton('Нет', callback_data='norm_condition_4_n')))
            cur_helpsys.execute("UPDATE norm SET food = ? WHERE user_id = ?",
                                ('Да', callback_query.from_user.id))
        elif callback_query.data[-1] == 'n':
            await bot.send_message(callback_query.from_user.id, 'Принятно, тогда идем дальше!')
            await bot.send_message(callback_query.from_user.id,
                                   'Уделяйте внимание качеству сна! Регулярный и полноценный сон способствует восстановлению энергии и улучшению настроения!'
                                   '\nУдается ли вам хорошо спать и высыпаться?',
                                   reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                       InlineKeyboardButton('Да', callback_data='norm_condition_4_y'),
                                       InlineKeyboardButton('Нет',
                                                            callback_data='norm_condition_4_n')))
            cur_helpsys.execute("UPDATE norm SET food = ? WHERE user_id = ?",
                                ('Нет', callback_query.from_user.id))
        else:
            await bot.send_message(callback_query.from_user.id, 'Поддерживать здоровое и сбалансированное питание может быть сложной задачей, но есть несколько стратегий, которые могут помочь вам придерживаться этого:'
                                                                '\n\n1. - <b>Постепенные изменения:</b> Начните с малого. Внесите постепенные изменения в свой рацион, добавляя больше свежих фруктов, овощей и белковых продуктов, а также уменьшая потребление процессированных продуктов и сахара.'
                                                                '\n2. - <b>Планирование:</b> Заранее планируйте свои приемы пищи. Можете составлять меню на неделю и делать список продуктов перед походом в магазин. Это поможет избежать импульсивных покупок и соблюдать план питания.'
                                                                '\n3. - <b>Умеренность:</b> Не нужно сразу избегать любимых продуктов. Разрешайте себе употреблять их в разумных количествах, чтобы избежать чувства лишения.'
                                                                '\n4. - <b>Пить воду:</b> Постарайтесь употреблять достаточное количество воды в течение дня. Иногда чувство голода может быть вызвано обезвоживанием.'
                                                                '\n5. - <b>Поддержка и мотивация:</b> Обсудите свои пищевые привычки с друзьями или семьей. Может быть, они могут вас поддержать или даже присоединиться к вам в этом усилии.'
                                                                '\n6. - <b>Поиск альтернатив:</b> Ищите заменители нежелательных продуктов. Например, замените жареную картошку на запеченные сладкие картофели, а газированные напитки на воду с лимоном.'
                                                                '\n7. - <b>Самомотивация:</b> Постоянно напоминайте себе о целях, которые вы хотите достичь, благодаря уравновешенному питанию. Самомотивация может быть мощным стимулом.'
                                                                '\n\nПомните, что никто не совершенен, и иногда допускать "грехи" в питании вполне нормально. Главное - стремиться к улучшению своих пищевых привычек и делать это постепенно!',
                                   parse_mode='html')
            await asyncio.sleep(5)
            await bot.send_message(callback_query.from_user.id, 'Для начала, мы можем начать с небольших информационных рассылок и опросов о вашем питании и привычках. '
                                                                 '\nВы бы хотели попробовать подобную практику?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                       InlineKeyboardButton('Да', callback_data='agreement_mailing_help_f_n_y'),
                                       InlineKeyboardButton('Нет, меня всё устраивает',
                                                            callback_data='agreement_mailing_help_f_n_n')))
            cur_helpsys.execute("UPDATE norm SET food = ? WHERE user_id = ?",
                                ('Улучшить', callback_query.from_user.id))
        db_helpsys.commit()

    elif callback_query.data[-3] == '4':
        if callback_query.data[-1] == 'y':
            cur_helpsys.execute('UPDATE norm SET sleep = ? WHERE user_id = ?', ('Да', callback_query.from_user.id))
            await bot.send_message(callback_query.from_user.id, 'Отлично, тогда продолжим!')
            await asyncio.sleep(1)
            await bot.send_message(callback_query.from_user.id, 'Вы слышали, что для крепкого и здорового сна помогают практики управления стрессом, такие как медитация, глубокое дыхание и релаксация?'
                                                                '\n\nЭти навыки могут помочь вам справляться с ежедневными вызовами. Их вы можете найти в разделе /practices')
            await bot.send_message(callback_query.from_user.id, 'Удавалось ли вам выполнять рекомендации, которые были предложены на марфоне?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                            InlineKeyboardButton('Да, хочу продолжения!', callback_data='norm_condition_5_y'),
                                            InlineKeyboardButton('Да, но хочу чего-то другого', callback_data='norm_condition_5_y'),
                                            InlineKeyboardButton('Нет, но хотелось бы попробовать', callback_data='norm_condition_5_y'),
                                            InlineKeyboardButton('Нет, мне это не интересно', callback_data='norm_condition_5_n')))
        elif callback_query.data[-1] == 'n':
            cur_helpsys.execute('UPDATE norm SET sleep = ? WHERE user_id = ?', ('Нет', callback_query.from_user.id))
            await bot.send_message(callback_query.from_user.id, 'Тогда попробуем это исправить!')
            await asyncio.sleep(1)
            await bot.send_message(callback_query.from_user.id, 'Вы слышали, что для крепкого и здорового сна помогают практики управления стрессом, такие как медитация, глубокое дыхание и релаксация?'
                                                                '\n\nЭти навыки могут помочь вам справляться с ежедневными вызовами. Их вы можете найти в разделе /practices')
            await bot.send_message(callback_query.from_user.id, 'Удавалось ли вам выполнять рекомендации, которые были предложены на марфоне?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                            InlineKeyboardButton('Да, хочу продолжения!', callback_data='norm_condition_5_y'),
                                            InlineKeyboardButton('Да, но хочу чего-то другого', callback_data='norm_condition_5_y'),
                                            InlineKeyboardButton('Нет, но хотелось бы попробовать', callback_data='norm_condition_5_y'),
                                            InlineKeyboardButton('Нет, мне это не интересно', callback_data='norm_condition_5_n')))
        db_helpsys.commit()

    elif callback_query.data[-3] == '5':
        if callback_query.data[-1] == 'y':
            cur_helpsys.execute('UPDATE norm SET marathon = ? WHERE user_id = ?', ('Понравился', callback_query.from_user.id))
            await bot.send_message(callback_query.from_user.id, 'Рады это слышать!'
                                                                '\nИменно поэтому хотим представить вам нашу новую систему поддержки, взаимодействующую с вами каждый день, которая будет предоставлять вам советы и рекомендации по улучшению психологического состояния, а также подборки с новыми упражнениями и практиками!'
                                                                '\nХотите попробовать?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                    InlineKeyboardButton('Да, можно попробовать', callback_data='agreement_mailing_help_m_n_y'),
                    InlineKeyboardButton('Нет, не хочу', callback_data='agreement_mailing_help_m_n_n')))
        elif callback_query.data[-1] == 'n':
            cur_helpsys.execute('UPDATE norm SET marathon = ? WHERE user_id = ?', ('Не понравился', callback_query.from_user.id))
            await bot.send_message(callback_query.from_user.id, 'Очень жаль, что вам неинтересна тема заботы о своём психологическом здоровье(('
                                                                '\nХорошего вам вечера!')
            await FSM_classes.MultiDialog.menu.set()
        db_helpsys.commit()


async def bad_condition(callback_query: types.CallbackQuery, state: FSMContext):
    db_helpsys = sqlite3.connect('Databases/Help_system.db')
    cur_helpsys = db_helpsys.cursor()
    if callback_query.data[-3] == '0':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        if callback_query.data[-1] == 'y':
            if int(callback_query.data[-5]) in [1,2,3]:
                cur_helpsys.execute('UPDATE bad SET type_problem = ? WHERE user_id = ?', ('Высокая нагрузка', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id, 'Понимаю, что высокая рабочая нагрузка может быть очень тяжелой(( '
                                                                    '\nВажно, чтобы вы не чувствовали себя одинокими в этой ситуации и знали, что можете рассчитывать на поддержку!')
                await bot.send_message(callback_query.from_user.id,'Используйте методы управления стрессом, такие как медитация, глубокое дыхание и релаксационные техники, чтобы снизить уровень стресса и улучшить концентрацию!'
                                                                   '\nВажно находить на это время!')
                await asyncio.sleep(2)
                await bot.send_message(callback_query.from_user.id,'Чтобы улучшить ваше состояние, хотим предложить поддержку, содержащую в себе практики и упражнения для разгрузки, а также общие советы по поддержке. '
                               '\nХотите попробовать?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                    InlineKeyboardButton('Да, можно попробовать', callback_data='bad_condition_1_1_y'),
                    InlineKeyboardButton('Нет, не хочу', callback_data='bad_condition_1_1_n')))

            elif int(callback_query.data[-5]) in [4,5]:
                cur_helpsys.execute('UPDATE bad SET type_problem = ? WHERE user_id = ?', ('Коллеги', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Понимаю, что взаимодействие с коллегами может иногда вызывать трудности! '
                                       '\nВажно помнить, что это нормальная часть рабочей жизни, и с ней можно справиться! '
                                       '\nВот несколько советов, которые могут помочь вам улучшить отношения и справиться со сложностями с коллегами:')
                await bot.send_message(callback_query.from_user.id,'Попробуйте начать разговор с коллегой и выразить свои мысли и чувства открыто и конструктивно. '
                                                                   '\nОбмен мнениями может помочь разрешить конфликты!'
                                                                   '\n\nПостарайтесь внимательно выслушать точку зрения коллеги и понять его или ее сторону. '
                                                                   '\nИногда простое понимание может уменьшить напряжение!'
                                                                   '\n\nУлучшите свои навыки общения, учитывая, как ваш стиль общения может влиять на других. '
                                                                   '\nПостарайтесь быть ясным, уважительным и дружелюбным!'
                                                                   '\n\nЕсли возникают конфликты, попробуйте их решить. '
                                                                   '\nОбсудите проблему с коллегой или обратитесь за помощью к руководству или HR-специалистам!'
                                                                   '\n\nИщите общие интересы и цели с коллегами, чтобы создать более позитивное рабочее взаимодействие!'
                                                                   '\n\nПостарайтесь воспринимать коллег как часть команды, работающей на общий успех. '
                                                                   '\nСовместное достижение целей может укрепить отношения!'
                                                                   '\n\nНаучитесь управлять стрессом и конфликтами. '
                                                                   '\nДыхательные упражнения и методы релаксации могут помочь справляться с эмоциональными вызовами!')
                await bot.send_message(callback_query.from_user.id,' Если сложности с коллегами продолжаются, также стоит обратиться за поддержкой к вашему руководству или специалистам по персоналу!'
                                                                   '\nМы сформировали запрос и с вами свяжуться для помощи с решением вопроса!')
                await FSM_classes.MultiDialog.menu.set()

            elif int(callback_query.data[-5]) == 6:
                cur_helpsys.execute('UPDATE bad SET type_problem = ? WHERE user_id = ?', ('Рабочее место', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Давайте попробуем разобраться в этом вопросе подробнее! '
                                       '\nМогли бы вы уточнить, что именно на вашем рабочем месте вызывает беспокойство и неудовлетворение?')
                await bot.send_message(callback_query.from_user.id,
                                       'Постарайтесь делать короткие перерывы каждый час, чтобы расслабиться и растянуться! '
                                       '\nДаже небольшая физическая активность, такая как прогулка или упражнения на месте, могут помочь поддерживать энергию и концентрацию!')
                await asyncio.sleep(2)
                await bot.send_message(callback_query.from_user.id,
                                       'Чтобы улучшить ваше состояние, хотим предложить поддержку, содержащую в себе практики и упражнения для разгрузки, а также общие советы по поддержке. '
                                       '\nХотите попробовать?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                        InlineKeyboardButton('Да, можно попробовать', callback_data='bad_condition_1_3_y'),
                        InlineKeyboardButton('Нет, не хочу', callback_data='bad_condition_1_3_n')))

            else:
                cur_helpsys.execute('UPDATE bad SET type_problem = ? WHERE user_id = ?', ('Психологический дискомфорт', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id, 'Хотите ли проработать проблему?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                        InlineKeyboardButton('Да, можно попробовать', callback_data='bad_condition_1_4_y'),
                        InlineKeyboardButton('Нет, не хочу', callback_data='bad_condition_1_4_n')))
            db_helpsys.commit()

        elif callback_query.data[-1] == 'n':
            if int(callback_query.data[-5]) == 8:
                cur_helpsys.execute('UPDATE bad SET type_problem = ? WHERE user_id = ?', ('Все ответы "нет"', callback_query.from_user.id))
                await FSM_classes.MultiDialog.quick_help.set()
                await bot.send_message(callback_query.from_user.id,
                                       text='Выберите, что вы чувствуете, чтобы разобраться в проблеме поподробнее',
                                       reply_markup=quick_help.quick_help_menu)
            else:
                await bot.send_message(callback_query.from_user.id,
                                   text=bad_condition_questions[int(callback_query.data[-5])+1],
                                   reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                       InlineKeyboardButton('Да', callback_data='bad_condition_'+str(int(callback_query.data[-5])+1)+'_0_y'),
                                       InlineKeyboardButton('Нет', callback_data='bad_condition_'+str(int(callback_query.data[-5])+1)+'_0_n')))

    #Высокая нагрузка
    if callback_query.data[-3] == '1':
        if callback_query.data[-5] == '1':
            cur_helpsys.execute("UPDATE agreement SET state = ? WHERE user_id = ?",('Плохо', callback_query.from_user.id))
            cur_helpsys.execute('UPDATE agreement SET subject = ? WHERE user_id = ?',
                                ('Высокая нагрузка', callback_query.from_user.id))
            if callback_query.data[-1] == 'y':
                cur_helpsys.execute("UPDATE agreement SET choice = ? WHERE user_id = ?",
                                    ('Да', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id, 'Мы поддерживаем ваш выбор!'
                                                                    '\nЗабота о своём психологическом здоровье - это важно!')
            if callback_query.data[-1] == 'n':
                cur_helpsys.execute("UPDATE agreement SET choice = ? WHERE user_id = ?",
                                    ('Нет', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id, 'Очень жаль, что вам неинтересна тема заботы о своём психологическом здоровье((')
            await asyncio.sleep(1)
            await bot.send_message(callback_query.from_user.id,
                                   'Одним из решений вашей проблемы также может быть перераспределение задачи или использование дополнительных ресурсов! '
                                   '\nВаш руководитель в скором времени сможет обсудить с вами данный вопрос! '
                                   '\n\nСпасибо, что поделились!')
            db_helpsys.commit()
            await FSM_classes.MultiDialog.menu.set()

    #Рабочее место
    if callback_query.data[-3] == '3':
        if callback_query.data[-5] == '1':
            cur_helpsys.execute("UPDATE agreement SET state = ? WHERE user_id = ?",('Плохо', callback_query.from_user.id))
            cur_helpsys.execute('UPDATE agreement SET subject = ? WHERE user_id = ?',
                                ('Рабочее место', callback_query.from_user.id))
            if callback_query.data[-1] == 'y':
                cur_helpsys.execute("UPDATE agreement SET choice = ? WHERE user_id = ?",
                                    ('Да', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id, 'Мы поддерживаем ваш выбор!'
                                                                    '\nЗабота о своём психологическом здоровье - это важно!')
            if callback_query.data[-1] == 'n':
                cur_helpsys.execute("UPDATE agreement SET choice = ? WHERE user_id = ?",
                                    ('Нет', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id, 'Очень жаль, что вам неинтересна тема заботы о своём психологическом здоровье((')
            await asyncio.sleep(1)
            await bot.send_message(callback_query.from_user.id,
                                   'Убедитесь, что ваше рабочее место удобно и эффективно организовано. '
                                   '\nЭргономические настройки, правильное освещение и удобное кресло могут сделать большую разницу в вашем комфорте.'
                                   '\nВсего ли вам хватает? Все ли для вас удобно и доступно?',
                                   reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                       InlineKeyboardButton('Да', callback_data='bad_condition_2_3_y'),
                                       InlineKeyboardButton('Нет', callback_data='bad_condition_2_3_n')))
        elif callback_query.data[-5] == '2':
            cur_helpsys.execute('UPDATE bad SET 3_workplace = ? WHERE user_id = ?',
                                (callback_query.data[-1], callback_query.from_user.id))
            await bot.send_message(callback_query.from_user.id, 'Питайтесь сбалансировано и употребляйте достаточное количество воды! '
                                                                '\nЗдоровое питание может помочь поддерживать уровень энергии на работе!'
                                                                '\n\nВам удается придерживаться сбалансированного питания?',
                                   reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                       InlineKeyboardButton('Да', callback_data='bad_condition_3_3_y'),
                                       InlineKeyboardButton('Нет', callback_data='bad_condition_3_3_n')))
        elif callback_query.data[-5] == '3':
            cur_helpsys.execute('UPDATE bad SET 3_food = ? WHERE user_id = ?',
                                (callback_query.data[-1], callback_query.from_user.id))
            await bot.send_message(callback_query.from_user.id, 'Попробуйте методы управления стрессом, такие как дыхательные упражнения, медитация или просто глубокий вдох и выдох в моменты напряжения. '
                                                                '\nЭто поможет снизить уровень стресса и повысить психологический комфорт!'
                                                                '\n\nНайти их вы сможете в разделе "Практики" или набрав команду /practices')
            await asyncio.sleep(2)
            await bot.send_message(callback_query.from_user.id,
                                   'Удавалось ли вам выполнять рекомендации, которые были предложены на марфоне?',
                                   reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                       InlineKeyboardButton('Да, хочу продолжения!',
                                                            callback_data='bad_condition_4_3_y'),
                                       InlineKeyboardButton('Да, но хочу чего-то другого',
                                                            callback_data='bad_condition_4_3_y'),
                                       InlineKeyboardButton('Нет, но хотелось бы попробовать',
                                                            callback_data='bad_condition_4_3_y'),
                                       InlineKeyboardButton('Нет, мне это не интересно',
                                                            callback_data='bad_condition_4_3_n')))
        elif callback_query.data[-5] == '4':
            if callback_query.data[-1] == 'y':
                cur_helpsys.execute('UPDATE bad SET 3_marathon = ? WHERE user_id = ?',
                                    ('Понравился', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id, 'Рады это слышать!'
                                                                    '\nИменно поэтому хотим представить вам нашу новую систему поддержки, взаимодействующую с вами каждый день, которая будет предоставлять вам советы и рекомендации по улучшению психологического состояния, а также подборки с новыми упражнениями и практиками!'
                                                                    '\nХотите попробовать?',
                                       reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                           InlineKeyboardButton('Да, можно попробовать',
                                                                callback_data='agreement_mailing_help_m_b_y'),
                                           InlineKeyboardButton('Нет, не хочу',
                                                                callback_data='agreement_mailing_help_m_b_n')))
            elif callback_query.data[-1] == 'n':
                cur_helpsys.execute('UPDATE bad SET 3_marathon = ? WHERE user_id = ?',
                                    ('Не понравился', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Очень жаль, что вам неинтересна тема заботы о своём психологическом здоровье(('
                                       '\nХорошего вам вечера!')
                await FSM_classes.MultiDialog.menu.set()

        db_helpsys.commit()

    # Психологический дискомфорт
    if callback_query.data[-3] == '4':
        if callback_query.data[-5] == '1':
            cur_helpsys.execute('UPDATE bad SET 4_elaboration = ? WHERE user_id = ?',
                                (callback_query.data[-1], callback_query.from_user.id))
            if callback_query.data[-1] == 'y':
                await bot.send_message(callback_query.from_user.id, 'Данный раздел научит вас прорабатывать катастрофические мысли. '
                                                                    '\nЗапишите пугающую мысль, ответьте последовательно на предложенные вопросы. В завершении в будущем сможете сохранить получившуюся карточку (вы сможете просматривать ее время от времени).'
                                                                    '\n\nВозвращайтесь к этой технике каждый раз, когда почувствуете тревогу!')
                await bot.send_message(callback_query.from_user.id,
                                       'Запишите на листочке, что вас тревожит', reply_markup=ReplyKeyboardRemove())
                await bot.send_message(callback_query.from_user.id, 'Есть ли сейчас в вашей жизни обстоятельства, которые указывают, что это произойдет?', reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                       InlineKeyboardButton('Да', callback_data='bad_condition_2_4_y'),
                                       InlineKeyboardButton('Нет', callback_data='bad_condition_2_4_n')))
            else:
                await FSM_classes.MultiDialog.quick_help.set()
                await bot.send_message(callback_query.from_user.id,
                                       text='Хорошо, тогда выберите, что вы чувствуете, чтобы разобраться в проблеме поподробнее',
                                       reply_markup=quick_help.quick_help_menu)
        if callback_query.data[-5] == '2':
            if callback_query.data[-1] == 'y':
                cur_helpsys.execute('UPDATE bad SET 4_elaboration = ? WHERE user_id = ?',
                                ('Да', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Такой исход вероятен?',
                                       reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                           InlineKeyboardButton('Да', callback_data='bad_condition_3_4_y'),
                                           InlineKeyboardButton('Нет', callback_data='bad_condition_3_4_n')))

            elif callback_query.data[-1] == 'n':
                cur_helpsys.execute('UPDATE bad SET 4_elaboration = ? WHERE user_id = ?',
                                    ('Нет', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id, 'Нет смысла бояться того, что не может произойти в действительности! '
                                                                    '\nСправиться вам смогут помочь психологические практики, которые вы сможете найти в разделе /practices')
                await bot.send_message(callback_query.from_user.id, 'Обязательно напишите, что вы теперь об этом думаете!')

        if callback_query.data[-5] == '3':
            if callback_query.data[-1] == 'y':
                cur_helpsys.execute('UPDATE bad SET 4_probability = ? WHERE user_id = ?',
                                ('Да', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Возможно ли что-то сделать чтобы снизить последствия?',
                                       reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                           InlineKeyboardButton('Да', callback_data='bad_condition_4_4_y'),
                                           InlineKeyboardButton('Нет', callback_data='bad_condition_4_4_n')))

            elif callback_query.data[-1] == 'n':
                cur_helpsys.execute('UPDATE bad SET 4_probability = ? WHERE user_id = ?',
                                    ('Нет', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id, 'Нет смысла бояться того, что не может произойти в действительности!'
                                                                    '\nСправиться вам может помочь "Терапия спокойствием", в достижении которой вы можете воспользоваться практиками /practices')
                await bot.send_message(callback_query.from_user.id, 'Обязательно напишите, что вы теперь об этом думаете!')

        if callback_query.data[-5] == '4':
            if callback_query.data[-1] == 'y':
                cur_helpsys.execute('UPDATE bad SET 4_actions = ? WHERE user_id = ?',
                                ('Да', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Отравляет ли вашу жизнь этот страх?',
                                       reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                           InlineKeyboardButton('Да', callback_data='bad_condition_5_4_y'),
                                           InlineKeyboardButton('Нет', callback_data='bad_condition_5_4_n')))

            elif callback_query.data[-1] == 'n':
                cur_helpsys.execute('UPDATE bad SET 4_actions = ? WHERE user_id = ?',
                                    ('Нет', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Если это случится, это можно будет исправить?',
                                       reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                           InlineKeyboardButton('Да', callback_data='bad_condition_5_4_u'),
                                           InlineKeyboardButton('Нет', callback_data='bad_condition_5_4_m')))

        if callback_query.data[-5] == '5':
            if callback_query.data[-1] == 'y':
                cur_helpsys.execute('UPDATE bad SET 4_ruin = ? WHERE user_id = ?',
                                ('Да', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Часто ли эта мысль приходит в вашу голову?',
                                       reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                           InlineKeyboardButton('Да', callback_data='bad_condition_6_4_y'),
                                           InlineKeyboardButton('Нет', callback_data='bad_condition_6_4_n')))

            elif callback_query.data[-1] == 'n':
                cur_helpsys.execute('UPDATE bad SET 4_ruin = ? WHERE user_id = ?',
                                    ('Нет', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Иногда бояться чего-то это норма! '
                                       '\nЧувствовать меньше напряжения вам поможет релаксация, в помощь вам раздел с практиками /practices')

            elif callback_query.data[-1] == 'u':
                cur_helpsys.execute('UPDATE bad SET 4_correct = ? WHERE user_id = ?',
                                    ('Да', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Значит это поправимо и вам по силам!'
                                       '\nХотим представить вам нашу новую систему поддержки, взаимодействующую с вами каждый день, которая будет предоставлять вам советы и рекомендации по улучшению психологического состояния, а также подборки с новыми упражнениями и практиками!'
                                        '\nНапример, вечерняя практика "Дневник мыслей" поможет проанализировать прошедший день, осознать свои эмоции и действия, а также улучшить самосознание и эмоциональное состояние!'
                                       '\nХотите попробовать?',
                                       reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                           InlineKeyboardButton('Да, можно попробовать',
                                                                callback_data='agreement_mailing_help_p_b_y'),
                                           InlineKeyboardButton('Нет, не хочу',
                                                                callback_data='agreement_mailing_help_p_b_n')))

            elif callback_query.data[-1] == 'm':
                cur_helpsys.execute('UPDATE bad SET 4_correct = ? WHERE user_id = ?',
                                ('Нет', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Если этого же боялся бы ваш близкий человек, вы бы поддержали его страх?',
                                       reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                           InlineKeyboardButton('Да', callback_data='bad_condition_6_4_u'),
                                           InlineKeyboardButton('Нет', callback_data='bad_condition_6_4_m')))

        if callback_query.data[-5] == '6':
            if callback_query.data[-1] == 'y':
                cur_helpsys.execute('UPDATE bad SET 4_thought = ? WHERE user_id = ?',
                                    ('Да', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Умеете ли вы с ней справляться?',
                                       reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                           InlineKeyboardButton('Да', callback_data='bad_condition_7_4_y'),
                                           InlineKeyboardButton('Нет', callback_data='bad_condition_7_4_n')))

            elif callback_query.data[-1] == 'n':
                cur_helpsys.execute('UPDATE bad SET 4_thought = ? WHERE user_id = ?',
                                    ('Нет', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Иногда бояться чего-то это норма! Чувствовать меньше напряжения вам помогут разгружающие практики!'
                                       '\n\nИменно поэтому хотим представить вам нашу новую систему поддержки, взаимодействующую с вами каждый день, которая будет предоставлять вам советы и рекомендации по улучшению психологического состояния, а также подборки с новыми упражнениями и практиками!'
                                       '\nНапример, вечерняя практика "Дневник мыслей" поможет проанализировать прошедший день, осознать свои эмоции и действия, а также улучшить самосознание и эмоциональное состояние!'
                                       '\nХотите попробовать?',
                                       reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                           InlineKeyboardButton('Да, можно попробовать',
                                                                callback_data='agreement_mailing_help_p_b_y'),
                                           InlineKeyboardButton('Нет, не хочу',
                                                                callback_data='agreement_mailing_help_p_b_n')))

            elif callback_query.data[-1] == 'u':
                cur_helpsys.execute('UPDATE bad SET 4_close = ? WHERE user_id = ?',
                                    ('Да', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Отравляет и ограничивает ли вашу жизнь этот страх?',
                                       reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                           InlineKeyboardButton('Да', callback_data='bad_condition_7_4_u'),
                                           InlineKeyboardButton('Нет', callback_data='bad_condition_7_4_m')))

            elif callback_query.data[-1] == 'm':
                cur_helpsys.execute('UPDATE bad SET 4_close = ? WHERE user_id = ?',
                                    ('Нет', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id, 'Если ваш близкий человек не должен переживать, то почему вы должны?'
                                                                    '\nРешение страхов и трудностей может потребовать различных методов и подходов в каждом конкретном случае. '
                                                                    '\nИногда поддержка близких людей может быть источником вдохновения и сил для борьбы со своими собственными страхами. '
                                                                    '\nОднако важно также понимать, что каждый человек имеет свои собственные страхи и собственный путь их преодоления.'
                                                                    '\n\nПредлагаем попробовать улучшить ваше состояние с помощью набора вечерних разгружающих практик, мотивирующих утренних и динамичные дневные практики.')
                await bot.send_message(callback_query.from_user.id,
                                       'Именно поэтому хотим представить вам нашу новую систему поддержки, взаимодействующую с вами каждый день, которая будет предоставлять вам советы и рекомендации по улучшению психологического состояния, а также подборки с новыми упражнениями и практиками!'
                                        '\nНапример, вечерняя практика "Дневник мыслей" поможет проанализировать прошедший день, осознать свои эмоции и действия, а также улучшить самосознание и эмоциональное состояние!'
                                       '\nХотите попробовать?',
                                       reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                           InlineKeyboardButton('Да, можно попробовать',
                                                                callback_data='agreement_mailing_help_p_b_y'),
                                           InlineKeyboardButton('Нет, не хочу',
                                                                callback_data='agreement_mailing_help_p_b_n')))

        if callback_query.data[-5] == '7':
            if callback_query.data[-1] == 'y':
                cur_helpsys.execute('UPDATE bad SET 4_success = ? WHERE user_id = ?',
                                    ('Да', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Вы на верном пути! Вам могут помочь наши дневник юлагодарностей, релаксация и терапия спокойствием!'
                                       '\n\nИменно поэтому хотим представить вам нашу новую систему поддержки, взаимодействующую с вами каждый день, которая будет предоставлять вам советы и рекомендации по улучшению психологического состояния, а также подборки с новыми упражнениями и практиками!'
                                       '\nНапример, вечерняя практика "Дневник мыслей" поможет проанализировать прошедший день, осознать свои эмоции и действия, а также улучшить самосознание и эмоциональное состояние!'
                                       '\nХотите попробовать?',
                                       reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                           InlineKeyboardButton('Да, можно попробовать',
                                                                callback_data='agreement_mailing_help_p_b_y'),
                                           InlineKeyboardButton('Нет, не хочу',
                                                                callback_data='agreement_mailing_help_p_b_n')))

            elif callback_query.data[-1] == 'n':
                cur_helpsys.execute('UPDATE bad SET 4_success = ? WHERE user_id = ?',
                                    ('Нет', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Похоже у вас не получается самостоятельно справится с этой катастрофической мыслью(( '
                                       '\nРекомендуем обратиться к специалисту!')
                await state.set_state(FSM_classes.MultiDialog.menu)

            elif callback_query.data[-1] == 'u':
                cur_helpsys.execute('UPDATE bad SET 4_barrier = ? WHERE user_id = ?',
                                    ('Да', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Часто ли эта мысль приходит в вашу голову?',
                                       reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                           InlineKeyboardButton('Да', callback_data='bad_condition_8_4_u'),
                                           InlineKeyboardButton('Нет', callback_data='bad_condition_8_4_m')))

            elif callback_query.data[-1] == 'm':
                cur_helpsys.execute('UPDATE bad SET 4_barrier = ? WHERE user_id = ?',
                                    ('Нет', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Иногда бояться чего-то это норма! Чувствовать меньше напряжения вам помогут разгружающие практики!'
                                       '\n\nИменно поэтому хотим представить вам нашу новую систему поддержки, взаимодействующую с вами каждый день, которая будет предоставлять вам советы и рекомендации по улучшению психологического состояния, а также подборки с новыми упражнениями и практиками!'
                                       '\nНапример, вечерняя практика "Дневник мыслей" поможет проанализировать прошедший день, осознать свои эмоции и действия, а также улучшить самосознание и эмоциональное состояние!'
                                       '\nХотите попробовать?',
                                       reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                           InlineKeyboardButton('Да, можно попробовать',
                                                                callback_data='agreement_mailing_help_p_b_y'),
                                           InlineKeyboardButton('Нет, не хочу',
                                                                callback_data='agreement_mailing_help_p_b_n')))

        if callback_query.data[-5] == '8':
            if callback_query.data[-1] == 'u':
                cur_helpsys.execute('UPDATE bad SET 4_thought = ? WHERE user_id = ?',
                                    ('Да', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Умеете ли вы с ней справляться?',
                                       reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                           InlineKeyboardButton('Да', callback_data='bad_condition_9_4_u'),
                                           InlineKeyboardButton('Нет', callback_data='bad_condition_9_4_m')))

            elif callback_query.data[-1] == 'm':
                cur_helpsys.execute('UPDATE bad SET 4_thought = ? WHERE user_id = ?',
                                    ('Нет', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Иногда бояться чего-то это норма! Чувствовать меньше напряжения вам помогут разгружающие практики!'
                                       '\n\nИменно поэтому хотим представить вам нашу новую систему поддержки, взаимодействующую с вами каждый день, которая будет предоставлять вам советы и рекомендации по улучшению психологического состояния, а также подборки с новыми упражнениями и практиками!'
                                       '\nНапример, вечерняя практика "Дневник мыслей" поможет проанализировать прошедший день, осознать свои эмоции и действия, а также улучшить самосознание и эмоциональное состояние!'
                                       '\nХотите попробовать?',
                                       reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                           InlineKeyboardButton('Да, можно попробовать',
                                                                callback_data='agreement_mailing_help_p_b_y'),
                                           InlineKeyboardButton('Нет, не хочу',
                                                                callback_data='agreement_mailing_help_p_b_n')))

        if callback_query.data[-5] == '9':
            if callback_query.data[-1] == 'u':
                cur_helpsys.execute('UPDATE bad SET 4_success = ? WHERE user_id = ?',
                                    ('Да', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Вы на верном пути! Вам могут помочь наши дневник юлагодарностей, релаксация и терапия спокойствием!'
                                       '\n\nИменно поэтому хотим представить вам нашу новую систему поддержки, взаимодействующую с вами каждый день, которая будет предоставлять вам советы и рекомендации по улучшению психологического состояния, а также подборки с новыми упражнениями и практиками!'
                                       '\nНапример, вечерняя практика "Дневник мыслей" поможет проанализировать прошедший день, осознать свои эмоции и действия, а также улучшить самосознание и эмоциональное состояние!'
                                       '\nХотите попробовать?',
                                       reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                           InlineKeyboardButton('Да, можно попробовать',
                                                                callback_data='agreement_mailing_help_p_b_y'),
                                           InlineKeyboardButton('Нет, не хочу',
                                                                callback_data='agreement_mailing_help_p_b_n')))

            elif callback_query.data[-1] == 'm':
                cur_helpsys.execute('UPDATE bad SET 4_success = ? WHERE user_id = ?',
                                    ('Нет', callback_query.from_user.id))
                await bot.send_message(callback_query.from_user.id,
                                       'Похоже у вас не получается самостоятельно справится с этой катастрофической мыслью(( '
                                       '\nРекомендуем обратиться к специалисту!')
                await state.set_state(FSM_classes.MultiDialog.menu)

        db_helpsys.commit()


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
        await bot.send_message(callback_query.from_user.id, 'Давайте расскажу вам поподробнее о практике "Благодарность». '
                                                            '\n\nБлагодарному человеку легче наслаждаться позитивными ощущениями и справляться со стрессовыми ситуациями, легче поддерживать хорошие отношения с другими и в целом ощущать себя.'
                                                            '\nЧтобы благодарность оказала влияние на ваше благополучие, прежде всего необходимо испытывать ее регулярно в какой бы то ни было форме. '
                                                            '\nЕсли вам удастся хоть раз запустить этот позитивный цикл и поддерживать его с помощью осознанного отношения, он будет снова и снова приносить вам пользу!', parse_mode='html')
        await asyncio.sleep(2)
        await bot.send_message(callback_query.from_user.id, 'Вы можете завести дневник благодарности, куда будете записывать то, за что вы благодарите (даже самые незначительные на первый взгляд вещи или ситуации) '
                                                            '\nПока пьете утренний кофе или чистите зубы, вы можете мысленно сосредоточиться на моментах для благодарности!')
        await asyncio.sleep(2)
        await bot.send_message(callback_query.from_user.id, 'Попробуйте записать эти действия и поступки в свой дневник, или заметки в смартфоне. '
                                                            '\nТак у вас всегда будет возможность увидеть свои достижения и что день был проведен с пользой!')
        await asyncio.sleep(4)
        await bot.send_message(callback_query.from_user.id,
                               'Чтобы ваше состояние оставалось всегда в норме, хотим предложить поддержку, содержащую в себе практики и упражнения для разгрузки, а также общие советы по поддержке. '
                               '\nХотите попробовать?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton('Да, можно попробовать', callback_data='agreement_mailing_help_0_g_y'),
                InlineKeyboardButton('Нет, не хочу', callback_data='agreement_mailing_help_0_g_n')))
    else:
        if callback_query.data[-2] == 'g':
            cur_helpsys.execute("UPDATE good SET try_practice = ? WHERE user_id = ?", ('Нет', callback_query.from_user.id))
            await bot.send_message(callback_query.from_user.id,
                                   'Чтобы ваше состояние оставалось всегда в норме, хотим предложить поддержку, содержащую в себе практики и упражнения для разгрузки, а также общие советы по поддержке. '
                                   '\nХотите попробовать?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                    InlineKeyboardButton('Да, можно попробовать', callback_data='agreement_mailing_help_0_g_y'),
                    InlineKeyboardButton('Нет, не хочу', callback_data='agreement_mailing_help_0_g_n')))
        elif callback_query.data[-2] == 'n':
            cur_helpsys.execute("UPDATE norm SET try_practice = ? WHERE user_id = ?", ('Нет', callback_query.from_user.id))
            await bot.send_message(callback_query.from_user.id,
                                   'Чтобы ваше состояние оставалось всегда в норме, хотим предложить поддержку, содержащую в себе практики и упражнения для разгрузки, а также общие советы по поддержке. '
                                   '\nХотите попробовать?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                    InlineKeyboardButton('Да, можно попробовать', callback_data='agreement_mailing_help_0_n_y'),
                    InlineKeyboardButton('Нет, не хочу', callback_data='agreement_mailing_help_0_n_n')))
        else:
            cur_helpsys.execute("UPDATE bad SET try_practice = ? WHERE user_id = ?", ('Нет', callback_query.from_user.id))
            await bot.send_message(callback_query.from_user.id,
                                   'Чтобы ваше состояние оставалось всегда в норме, хотим предложить поддержку, содержащую в себе практики и упражнения для разгрузки, а также общие советы по поддержке. '
                                   '\nХотите попробовать?', reply_markup=InlineKeyboardMarkup(row_width=1).add(
                    InlineKeyboardButton('Да, можно попробовать', callback_data='agreement_mailing_help_0_b_y'),
                    InlineKeyboardButton('Нет, не хочу', callback_data='agreement_mailing_help_0_b_n')))
        db_helpsys.commit()


async def agreement_mailing_help(callback_query: types.CallbackQuery, state: FSMContext):
    await help_system_agreement(user_id=callback_query.from_user.id)
    db_helpsys = sqlite3.connect('Databases/Help_system.db')
    cur_helpsys = db_helpsys.cursor()
    if callback_query.data[-3] == 'g':
        cur_helpsys.execute("UPDATE agreement SET state = ? WHERE user_id = ?", ('Хорошо', callback_query.from_user.id))
    elif callback_query.data[-3] == 'n':
        cur_helpsys.execute("UPDATE agreement SET state = ? WHERE user_id = ?",('Нормально', callback_query.from_user.id))
        if callback_query.data[-5] == 's':
            cur_helpsys.execute('UPDATE agreement SET subject = ? WHERE user_id = ?', ('Физическая активность', callback_query.from_user.id))
        elif callback_query.data[-5] == 'f':
            cur_helpsys.execute('UPDATE agreement SET subject = ? WHERE user_id = ?', ('Питание', callback_query.from_user.id))
        elif callback_query.data[-5] == 'm':
            cur_helpsys.execute('UPDATE agreement SET subject = ? WHERE user_id = ?', ('Марафон', callback_query.from_user.id))
    else:
        cur_helpsys.execute("UPDATE agreement SET state = ? WHERE user_id = ?", ('Плохо', callback_query.from_user.id))
        if callback_query.data[-5] == 'm':
            cur_helpsys.execute('UPDATE agreement SET subject = ? WHERE user_id = ?', ('Марафон', callback_query.from_user.id))
        if callback_query.data[-5] == 'p':
            cur_helpsys.execute('UPDATE agreement SET subject = ? WHERE user_id = ?', ('Практика на проработку', callback_query.from_user.id))
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
    dp.register_callback_query_handler(try_practice, lambda c: c.data and c.data.startswith('try_practice_'))
    dp.register_callback_query_handler(norm_condition, lambda c: c.data and c.data.startswith('norm_condition_'))
    dp.register_callback_query_handler(agreement_mailing_help, lambda c: c.data and c.data.startswith('agreement_mailing_help_'))
