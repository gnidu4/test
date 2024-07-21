import os
from telethon import events
from pytube import YouTube
from .. import loader, utils

@loader.tds
class YouTubeDownloaderMod(loader.Module):
    """Модуль для скачивания видео с YouTube"""
    strings = {"name": "YouTubeDownloader"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.sudo
    async def yt_cmd(self, message):
        """Скачивает видео с YouTube. Использование: .yt <ссылка на видео>"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("Пожалуйста, укажите ссылку на видео.")
            return
        
        url = args.strip()
        try:
            await message.edit("Загружаю видео...")
            yt = YouTube(url)

            # Получаем список потоков видео по возрастанию качества
            streams = yt.streams.filter(progressive=True).order_by('resolution')

            # Создаем строку с доступными качествами
            quality_list = '\n'.join([f"{i+1}. {stream.resolution}" for i, stream in enumerate(streams)])
            await message.edit(f"Выберите качество видео:\n\n{quality_list}\n\nОтветьте номером качества.")

            # Ждем ответ от пользователя
            response = await self.client.wait_for(events.NewMessage(incoming=True, from_users=message.from_id, pattern=r'^\d+$'))
            quality_choice = int(response.text.strip()) - 1

            if quality_choice < 0 or quality_choice >= len(streams):
                await message.edit("Неверный выбор качества.")
                return

            stream = streams[quality_choice]
            video_path = stream.download()
            
            await self.client.send_file(message.chat_id, video_path, caption=f"Видео: {yt.title}\nКачество: {stream.resolution}")
            os.remove(video_path)
            await message.delete()
        except Exception as e:
            await message.edit(f"Произошла ошибка: {str(e)}")
