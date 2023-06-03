import os
from telethon.sync import TelegramClient
from telethon import functions, types, events
from telethon.tl.types import InputMessagesFilterDocument
from telethon.sessions import MemorySession
from telethon.tl.types import InputMediaDocument


api_id = '23977087'
api_hash = '3b88f94e019f6ce1ff9c298371c8a1ff'
bot_token = '5974015198:AAHXJNMdvgShQ054kqGphV_b4k3zpUmoE4o'
source_channel_id = [-1001083653708,-1001308785417,-988880048,-1001590340657]  # ID исходных каналов
destination_channel_id = -1001844035904  # ID целевого канала


client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)
current_keyword_file_name = None
user_states = {}


@client.on(events.NewMessage(pattern=r'/setkeywords', incoming=True))
async def handle_set_keywords(event):
    if event.is_private:
        await event.respond('Please upload a .txt file.')

        user_states[event.sender_id] = 'waiting_file'



@client.on(events.NewMessage(chats=source_channel_id))
async def handle_new_message(event):
    global current_keyword_file_name
    if current_keyword_file_name is not None:
        words = []
        with open(current_keyword_file_name, 'r', encoding='utf-8') as file:

            for line in file:
                word = line.strip()
                words.append(word)
        print(words)
        if any(word in event.message.text for word in words):
            await client.send_message(destination_channel_id, event.message.text, parse_mode='html')
    else:
        await client.send_message(destination_channel_id, event.message.text, parse_mode='html')

@client.on(events.NewMessage(incoming=True))
async def handle_file(event):
    if event.media and user_states[event.sender_id] == 'waiting_file':
        file = event.message.media.document

        if file.mime_type == 'text/plain':
            path = await event.message.download_media()
            await event.respond(f'File has been downloaded to {path}')
            global current_keyword_file_name
            if current_keyword_file_name is not None:
                os.remove(current_keyword_file_name)
            current_keyword_file_name = path
        else:

            await event.respond('Please upload a .txt file.')
        del user_states[event.sender_id]

client.start()
client.run_until_disconnected()