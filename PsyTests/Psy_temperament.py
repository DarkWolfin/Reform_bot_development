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

from Databases import db_start, data_profile, pre_points_test_temperament, points_test_temperament

import Markups
import FSM_classes


temperament_questions = [
    '1. Часто ли Вы испытываете тягу к новым впечатлениям, к тому чтобы отвлечься, испытать сильные ощущения?',
    '2. Часто ли вы чувствуете, что нуждаетесь в друзьях, которые могут вас понять, одобрить или посочувствовать?',
    '3. Считаете ли вы себя беззаботным человеком?',
    '4. Очень ли трудно вам отказываться от своих намерений?',
    '5. Обдумываете ли вы свои дела не спеша и предпочитаете подождать, прежде чем действовать?',
    '6. Всегда ли вы сдерживаете свои обещания, даже если вам это невыгодно?',
    '7. Часто ли у вас бывают спады и подъемы настроения?',
    '8. Быстро ли вы обычно действуете и говорите, не затрачиваете ли много времени на обдумывание?',
    '9. Возникало ли у вас когда-нибудь чувство, что вы несчастны, хотя никакой серьезной причины на это не было?',
    '10. Верно ли, что "на спор" вы способны решиться на все?',
    '11. Смущаетесь ли вы, когда хотите познакомиться с человеком противоположного пола, который вам симпатичен?',
    '12. Бывает ли когда-нибудь, что, разозлившись, вы выходите из себя?',
    '13. Часто ли действуете необдуманно, под влиянием момента?',
    '14. Часто ли вас беспокоят мысли о том, что вам не следовало чего-либо делать или говорить?',
    '15. Предпочитаете ли вы чтение книг встречам с людьми?',
    '16. Верно ли, что вас легко задеть?',
    '17. Любите ли вы часто бывать в компании?',
    '18. Бывают ли у вас такие мысли, которыми вам не хотелось делиться с другими людьми?',
    '19. Верно ли, что иногда вы настолько полны энергии, что все горит в руках, а иногда вы чувствуете сильную вялость?',
    '20. Стараетесь ли вы ограничить круг своих знакомств небольшим числом самых близких людей?',
    '21. Много ли вы мечтаете?',
    '22. Когда на вас кричат, отвечаете ли тем же?',
    '23. Считаете ли вы свои привычки хорошими?',
    '24. Часто ли у вас появляется чувство, что вы чем-то виноваты?',
    '25. Способны ли вы иногда дать волю своим чувств и беззаботно развлечься с веселой компанией?',
    '26. Можно ли сказать, что часто у вас нервы бывают натянуты до предела?',
    '27. Слывете ли вы за человека веселого и живого?',
    '28. После того, как дело сделано, часто ли вы мысленно возвращаетесь к нему и думаете, что могли бы сделать лучше?',
    '29. Чувствуете ли вы себя неспокойно, находясь в большой компании?',
    '30. Бывает ли, что вы передаете слухи?',
    '31. Бывает ли, что вам не спится из-за того, что в голову лезут разные мысли?',
    '32. Что вы предпочитаете, если хотите что-либо узнать: найти это в книге или спросить у друзей?',
    '33. Бывают ли у вас сильные сердцебиения?',
    '34. Нравится ли вам работа, требующая сосредоточения?',
    '35. Бывают ли у вас приступы дрожи?',
    '36. Всегда ли вы говорите только правду?',
    '37. Бывает ли вам неприятно находиться в компании, где все подшучивают друг над другом?',
    '38. Раздражительны ли вы?',
    '39. Нравится ли вам работа, требующая быстрого действия?',
    '40. Верно ли, что вам часто не дают покоя мысли о разных неприятностях и "ужасах", которые могли бы произойти, хотя все кончилось благополучно?',
    '41. Верно ли, что вы неторопливы в движениях и несколько медлительны?',
    '42. Опаздывали ли вы когда-нибудь на работу или встречу с кем-то?',
    '43. Часто ли вам снятся кошмары?',
    '44. Верно ли что вы так любите поговорить, что не упускаете любого удобного случая побеседовать с новым человеком?',
    '45. Беспокоят ли вас какие-либо боли?',
    '46. Огорчились бы вы, если бы не смогли долго видеться с друзьями?',
    '47. Можете ли вы назвать себя нервным человеком?',
    '48. Есть ли среди ваших знакомых такие, которые вам явно не нравятся?',
    '49. Могли бы вы сказать, что вы уверенный в себе человек?',
    '50. Легко ли вас задевает критика ваших недостатков, или вашей работы?',
    '51. Трудно ли вам получить настоящее удовольствие от мероприятий, в которых участвует много народу?',
    '52. Беспокоит ли вас чувство, что вы чем-то хуже других?',
    '53. Сумели бы вы внести оживление в скучную компанию?',
    '54. Бывает ли, что вы говорите о вещах, в которых совсем не разбираетесь?',
    '55. Беспокоитесь ли вы о своем здоровье?',
    '56. Любите ли вы подшутить над другими?',
    '57. Страдаете ли вы бессонницей?'
]

temperament_answer = InlineKeyboardMarkup(resize_keyboard=True, row_width=1). add(
    InlineKeyboardButton('Да', callback_data='temperament_answer_y'),
    InlineKeyboardButton('Нет', callback_data='temperament_answer_n')
)


async def pretest_temperament(message: types.message, state: FSMContext):
    await FSM_classes.MultiDialog.test_temperament.set()
    await pre_points_test_temperament(user_id=message.from_user.id, username=message.from_user.username)
    async with state.proxy() as data:
        data['count'] = 0
    async with state.proxy() as data:
        data['points_extra'] = 0
    async with state.proxy() as data:
        data['points_neuro'] = 0
    await points_test_temperament(state, user_id=message.from_user.id)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Тест поможет узнать Ваш темперамент.'
                                                 '\nС помощью методики Айзенка определяют экстраверсию и нейротизм – свойства, лежащие в основе темперамента.'
                                                 '\nВ опроснике Айзенка 57 вопросов. На них необходимо ответить "да" или "нет".', reply_markup=types.ReplyKeyboardRemove())
    await asyncio.sleep(3)
    await bot.send_message(message.from_user.id, text=temperament_questions[0], reply_markup=temperament_answer)


async def answer_temperament(callback_query: types.CallbackQuery):
    point = callback_query.data[-1]
    db_temperament = sqlite3.connect('Databases/Result_Tests/PSY_Temperament.db')
    cur_temperament = db_temperament.cursor()
    one = int(1)
    cur_temperament.execute("UPDATE points SET count = (count + ?) WHERE user_id = ?", (one, callback_query.from_user.id))
    if (int(cur_temperament.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) in [1, 3, 8, 10, 13, 17, 22, 25, 27, 39, 44, 46, 49, 53]) and (point == 'y'):
        cur_temperament.execute("UPDATE points SET points_extra = points_extra + ? WHERE user_id = ?", (one, callback_query.from_user.id))
    elif (int(cur_temperament.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) in [5, 15, 20, 29, 32, 34, 37, 41, 51]) and (point == 'n'):
        cur_temperament.execute("UPDATE points SET points_extra = points_extra + ? WHERE user_id = ?", (one, callback_query.from_user.id))
    elif (int(cur_temperament.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) in [2, 4, 7, 9, 11, 14, 16, 19, 21, 23, 26, 28, 31, 33, 35, 38, 40, 43, 45, 47, 50, 52, 55, 57]) and (point == 'y'):
        cur_temperament.execute("UPDATE points SET points_neuro = points_neuro + ? WHERE user_id = ?", (one, callback_query.from_user.id))
    db_temperament.commit()
    if (int(cur_temperament.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) != 57):
        await bot.edit_message_text(chat_id=callback_query.from_user.id, text=temperament_questions[int(cur_temperament.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0])], message_id=callback_query.message.message_id, reply_markup=temperament_answer)
    else:
        if (int(cur_temperament.execute('SELECT points_extra FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) <= 12) and (int(cur_temperament.execute('SELECT points_neuro FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) <= 13):
            await bot.send_message(callback_query.from_user.id, 'Флегматик.'
                                                                '\nВы характеризуетесь сравнительно низким уровнем активности поведения, новые формы которого вырабатываются медленно, но являются стойкими.'
                                                                'Обладаете медлительностью и спокойствием в действиях, мимике и речи, ровностью, постоянством, глубиной чувств и настроений.'
                                                                'Вы настойчивый и упорный «труженик жизни», редко выходите из себя, не склонны к аффектам, рассчитав свои силы, доводите дело до конца, равны в отношениях, в меру общительны, не любите попусту болтать. Экономите силы, попусту их не тратите.'
                                                                'В зависимости от условий в одних случаях Вы можете характеризоваться «положительными» чертами — выдержкой, глубиной мыслей, постоянством, основательностью и т. д., в других — вялостью, безучастностью к окружающему, ленью и безволием, бедностью и слабостью эмоций, склонностью к выполнению одних лишь привычных действий.', reply_markup=Markups.backIn)
        elif (int(cur_temperament.execute('SELECT points_extra FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) <= 12) and (int(cur_temperament.execute('SELECT points_neuro FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) > 13):
            await bot.send_message(callback_query.from_user.id, 'Меланхолик.'
                                                                'У Вас реакция часто не соответствует силе раздражителя, присутствует глубина и устойчивость чувств при слабом их выражении.'
                                                                '\nВам трудно долго на чем-то сосредоточиться. Сильные воздействия часто вызывают у Вас продолжительную тормозную реакцию (опускаются руки).'
                                                                'Вам свойственны сдержанность и приглушенность моторики и речи, застенчивость, робость, нерешительность.'
                                                                'В нормальных условиях Вы — человек глубокий, содержательный, можете быть хорошим тружеником, успешно справляться с жизненными задачами.'
                                                                'При неблагоприятных условиях можете превратиться в замкнутого, боязливого, тревожного, ранимого человека, склонного к тяжелым внутренним переживаниям таких жизненных обстоятельств, которые вовсе этого не заслуживают.', reply_markup=Markups.backIn)
        elif (int(cur_temperament.execute('SELECT points_extra FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) > 12) and (int(cur_temperament.execute('SELECT points_neuro FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) <= 13):
            await bot.send_message(callback_query.from_user.id, 'Сангвиник.'
                                                                '\nВы быстро приспосабливается к новым условиям, быстро сходитесь с людьми, общительны. Чувства легко возникают и сменяются, эмоциональные переживания, как правило, неглубоки.'
                                                                'Мимика богатая, подвижная, выразительная. Вы несколько непоседливы, нуждаетесь в новых впечатлениях, недостаточно регулируете свои импульсы, не умеете строго придерживаться выработанного распорядка, жизни, системы в работе.'
                                                                'В связи с этим не можете успешно выполнять дело, требующее равной затраты сил, длительного и методичного напряжения, усидчивости, устойчивости внимания, терпения.'
                                                                'При отсутствии серьезных целей, глубоких мыслей, творческой деятельности вырабатываются поверхностность и непостоянство.', reply_markup=Markups.backIn)
        elif (int(cur_temperament.execute('SELECT points_extra FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) > 12) and (int(cur_temperament.execute('SELECT points_neuro FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) > 13):
            await bot.send_message(callback_query.from_user.id, 'Холерик.'
                                                                '\nВы отличаетесь повышенной возбудимостью, действия прерывисты.'
                                                                'Вам свойственны резкость и стремительность движений, сила, импульсивность, яркая выраженность эмоциональных переживаний.'
                                                                'Вследствие неуравновешенности, увлекшись делом, склонны действовать изо всех сил, истощаться больше, чем следует. Имея общественные интересы, Ваш темперамент проявляет в инициативности, энергичности, принципиальности.'
                                                                'При отсутствии духовной жизни Ваш холерический темперамент часто проявляется в раздражительности, эффективности, несдержанности, вспыльчивости, неспособности к самоконтролю при эмоциональных обстоятельствах.', reply_markup=Markups.backIn)

def register_handlers_Psy_temperament(dp : Dispatcher):
    dp.register_callback_query_handler(answer_temperament, text=['temperament_answer_y', 'temperament_answer_n'])
