import os
from telethon import events
from yt_dlp import YoutubeDL
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
            await message.edit("Получаю информацию о видео...")
            ydl_opts = {
                'format': 'best',
                'quiet': True,
                'no_warnings': True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_title = info_dict.get('title', 'Video')
                formats = info_dict.get('formats', [])

            # Создаем строку с доступными качествами
            quality_list = '\n'.join([
                f"{i+1}. {format['format']} - {format.get('format_note', 'N/A')}" 
                for i, format in enumerate(formats)
            ])
            await message.edit(f"Выберите качество видео:\n\n{quality_list}\n\nОтветьте номером качества.")

            def response_filter(event):
                return event.sender_id == message.sender_id and event.text.isdigit()

            response = await self.client.wait_event(events.NewMessage(chats=message.chat_id, func=response_filter))
            quality_choice = int(response.text.strip()) - 1

            if quality_choice < 0 or quality_choice >= len(formats):
                await message.edit("Неверный выбор качества.")
                return

            format_id = formats[quality_choice]['format_id']
            ydl_opts['format'] = format_id

            await message.edit("Скачиваю видео...")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            video_file = ydl.prepare_filename(info_dict)
            await self.client.send_file(message.chat_id, video_file, caption=f"Видео: {video_title}\nКачество: {formats[quality_choice].get('format_note', 'N/A')}")
            os.remove(video_file)
            await message.delete()
        except Exception as e:
            await message.edit(f"Произошла ошибка: {str(e)}")
