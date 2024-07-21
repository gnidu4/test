import requests
from telethon import events
from .. import loader, utils

@loader.tds
class YouTubeDownloadMod(loader.Module):
    """Модуль для генерации ссылки на скачивание видео с YouTube"""
    strings = {"name": "YouTubeDownload"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.sudo
    async def yt_cmd(self, message):
        """Получает ссылку для скачивания видео с YouTube. Использование: .yt <ссылка на видео>"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("Пожалуйста, укажите ссылку на видео.")
            return
        
        video_url = args.strip()
        await message.edit("Генерирую ссылку для скачивания...")

        # Пример использования y2mate API для генерации ссылки на скачивание
        try:
            response = requests.get(f"https://api.y2mate.is/api/video?url={video_url}")
            if response.status_code != 200:
                await message.edit(f"Ошибка: не удалось получить данные. Код ответа: {response.status_code}")
                return
            
            data = response.json()

            if "url" in data:
                download_link = data["url"]
                await message.edit(f"Ссылка для скачивания: [Скачать видео]({download_link})")
            else:
                await message.edit("Ошибка: не удалось сгенерировать ссылку для скачивания.")
        
        except Exception as e:
            await message.edit(f"Произошла ошибка: {str(e)}")
