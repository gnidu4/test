import requests
from bs4 import BeautifulSoup
from telethon import events
from .. import loader, utils

@loader.tds
class ValorantStatsMod(loader.Module):
    """Модуль для отображения статистики игрока в Valorant с сайта tracker.gg"""
    strings = {"name": "ValorantStats"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.sudo
    async def check_cmd(self, message):
        """Получает статистику игрока в Valorant. Использование: .check <имя#тег>"""
        args = utils.get_args_raw(message)
        if not args or '#' not in args:
            await message.edit("Пожалуйста, укажите имя игрока и тег в формате: имя#тег")
            return
        
        name, tag = args.split('#')
        url = f"https://tracker.gg/valorant/profile/riot/{name}%23{tag}/overview"

        try:
            await message.edit("Получаю данные...")
            response = requests.get(url)
            if response.status_code != 200:
                await message.edit(f"Ошибка: не удалось получить данные. Код ответа: {response.status_code}")
                return

            soup = BeautifulSoup(response.text, 'html.parser')

            # Парсинг данных (пример)
            stats = {}
            stats['Имя'] = f"{name}#{tag}"

            # Пример парсинга статистики
            for stat in soup.find_all('div', class_='stat'):
                stat_name = stat.find('span', class_='name').text.strip()
                stat_value = stat.find('span', class_='value').text.strip()
                stats[stat_name] = stat_value

            stats_message = '\n'.join([f"{key}: {value}" for key, value in stats.items()])
            await message.edit(stats_message)

        except Exception as e:
            await message.edit(f"Произошла ошибка: {str(e)}")
