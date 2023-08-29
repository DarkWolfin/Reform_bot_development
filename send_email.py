import os
import smtplib
from email.mime.text import MIMEText
from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())
import chats_id


async def send_email(message_content):
    sender = 'reform.yourself.bot@gmail.com'
    password = 'dskbkfkzyjtothro'
    recipients = ['violetta.psheunova@raiffeisen.ru', 'Yana.SCHERBAKOVA@raiffeisen.ru', 'Valeria.Guzhova@raiffeisen.ru']
    # recipients = ['qualitypecherkin@gmail.com', 'reform.yourself.bot@gmail.com']

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    msg = MIMEText(message_content)
    msg['Subject'] = 'Оповещение от бота Psychological Assistant'

    for i in range(len(recipients)):
        try:
            server.login(sender, password)
            server.sendmail(sender, recipients[i], msg.as_string())
            await bot.send_message(chat_id=chats_id.reports_chat_id, text=message_content)
            await bot.send_message(chat_id=chats_id.reports_chat_id, text='Взаимодействие с тревожной кнопкой отправлено '+ recipients[i])
        except Exception as _ex:
            await bot.send_message(chat_id=chats_id.reports_chat_id, text=f'Ошибка!!!\n{_ex}')
