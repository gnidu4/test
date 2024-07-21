import requests
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
        url = f"https://api.tracker.gg/api/v2/valorant/standard/profile/riot/{name}%23{tag}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            await message.edit("Получаю данные...")
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                await message.edit(f"Ошибка: не удалось получить данные. Код ответа: {response.status_code}")
                return

            data = response.json()

            stats = {}
            stats['Имя'] = f"{name}#{tag}"
            stats_data = data['data']['segments'][0]['stats']

            for stat_name, stat_info in stats_data.items():
                stats[stat_info['displayName']] = stat_info['displayValue']

            stats_message = '\n'.join([f"{key}: {value}" for key, value in stats.items()])
            await message.edit(stats_message)

        except Exception as e:
            await message.edit(f"Произошла ошибка: {str(e)}")
