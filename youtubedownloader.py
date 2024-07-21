from telethon import events
from pytube import YouTube
import os

# Функция для скачивания видео с YouTube
def download_youtube_video(url, resolution='720p'):
    yt = YouTube(url)
    stream = yt.streams.filter(res=resolution).first()
    if not stream:
        raise ValueError(f"Видео в разрешении {resolution} не найдено")
    return stream.download()

# Обработчик команды .yt
async def handler(event):
    # Получаем URL видео из сообщения
    message = event.message.message
    url = event.pattern_match.group(1)

    if not url:
        await event.reply("Пожалуйста, предоставьте ссылку на видео. Пример: .yt https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        return

    try:
        await event.reply("Скачиваю видео, пожалуйста, подождите...")
        video_path = download_youtube_video(url)
        await event.reply("Видео скачано, отправляю его вам...")
        await event.client.send_file(event.chat_id, video_path)
        os.remove(video_path)
    except Exception as e:
        await event.reply(f"Произошла ошибка при скачивании видео: {str(e)}")

# Регистрация модуля
def mod_load(client):
    client.add_event_handler(handler, events.NewMessage(pattern=r'\.yt (.+)'))
    print("Модуль YouTube Downloader успешно загружен!")

def mod_unload(client):
    client.remove_event_handler(handler, events.NewMessage(pattern=r'\.yt (.+)'))
    print("Модуль YouTube Downloader успешно выгружен!")