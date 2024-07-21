import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
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

        try:
            session = HTMLSession()
            response = session.get("https://yt1s.com/en68")
            response.html.render()

            soup = BeautifulSoup(response.html.html, 'html.parser')
            form = soup.find('form', {'id': 'form-download'})

            if form:
                input_url = form.find('input', {'name': 'url'})
                input_url['value'] = video_url

                response = session.post("https://yt1s.com/api/ajaxSearch/index", data={
                    'q': video_url,
                    'vt': 'home'
                })

                data = response.json()

                if 'links' in data and 'mp4' in data['links']:
                    mp4_links = data['links']['mp4']
                    best_quality = max(mp4_links.keys(), key=lambda k: int(mp4_links[k]['size']))
                    download_link = mp4_links[best_quality]['url']

                    await message.edit(f"Ссылка для скачивания: [Скачать видео]({download_link})")
                else:
                    await message.edit("Ошибка: не удалось сгенерировать ссылку для скачивания.")
            else:
                await message.edit("Ошибка: не удалось найти форму для скачивания.")

        except Exception as e:
            await message.edit(f"Произошла ошибка: {str(e)}")

    async def __call__(self):
        try:
            import requests
            from bs4 import BeautifulSoup
            from requests_html import HTMLSession
        except ImportError:
            import pip
            pip.main(['install', 'requests', 'beautifulsoup4', 'requests_html'])
            import requests
            from bs4 import BeautifulSoup
            from requests_html import HTMLSession
