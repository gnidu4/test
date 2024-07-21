import requests
from bs4 import BeautifulSoup
from .. import loader, utils

@loader.tds
class ValorantStatsModule(loader.Module):
    """Модуль для получения статистики игрока в Valorant с сайта tracker.gg"""
    strings = {"name": "ValorantStatsModule"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    async def nickcmd(self, message):
        """Команда: .nick <никнейм#тег> - Получить статистику игрока в Valorant"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("Пожалуйста, укажите никнейм игрока в формате Example#1234.")
            return

        username = args.replace("#", "%23")
        url = f"https://tracker.gg/valorant/profile/riot/{username}/overview"

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Поиск элементов на странице
                kd_element = soup.find('span', {'title': 'K/D Ratio'})
                current_rank_element = soup.find('div', class_='valorant-highlighted-stat__value', string='Current Rank')
                peak_rank_element = soup.find('div', class_='valorant-highlighted-stat__value', string='Peak Rank')

                # Извлечение данных
                kd = kd_element.find_next('span').text.strip() if kd_element else None
                current_rank = current_rank_element.find_next('span').text.strip() if current_rank_element else None
                peak_rank = peak_rank_element.find_next('span').text.strip() if peak_rank_element else None

                if kd and current_rank and peak_rank:
                    await message.edit(f"Статистика игрока {args}:\n\nK/D: {kd}\nТекущий ранг: {current_rank}\nПиковый ранг: {peak_rank}")
                else:
                    await message.edit("Профиль приватный или не удалось получить данные.")
            else:
                await message.edit("Не удалось получить данные. Проверьте никнейм и попробуйте снова.")
        except Exception as e:
            await message.edit(f"Произошла ошибка: {str(e)}")
