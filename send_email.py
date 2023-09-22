import os
import smtplib
from email.mime.text import MIMEText
from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Token import Token
from Storage import storage
bot = Bot(Token)
dp = Dispatcher(bot, storage=storage)
import chats_id


async def send_email(message_content):
    sender = 'reform.yourself.bot@gmail.com'
    password = 'dskbkfkzyjtothro'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    msg = MIMEText(message_content)
    msg['Subject'] = 'Оповещение от бота Psychological Assistant'
    await bot.send_message(chat_id=chats_id.reports_chat_id, text=message_content)

    for i in range(len(chats_id.recipients)):
        try:
            server.login(sender, password)
            server.sendmail(sender, chats_id.recipients[i], msg.as_string())
        except Exception as _ex:
            await bot.send_message(chat_id=chats_id.reports_chat_id, text=f'Возникла ошибка при отправке сообщения на почту '+chats_id.recipients[i]+'\n{_ex}')

