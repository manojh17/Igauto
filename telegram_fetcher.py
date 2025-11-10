import os
import csv
from telethon import TelegramClient
from config import api_id, api_hash, channel_id, media_temp_folder

client = TelegramClient("my_account", api_id, api_hash)

async def fetch_video(message_id):
    await client.start()

    msg = await client.get_messages(channel_id, ids=message_id)

    if not msg or not msg.video:
        return None, None

    # create folder
    if not os.path.exists(media_temp_folder):
        os.makedirs(media_temp_folder)

    filename = f"{media_temp_folder}/{message_id}.mp4"

    # download
    await msg.download_media(file=filename)
    
    caption = msg.message or ""

    return filename, caption
