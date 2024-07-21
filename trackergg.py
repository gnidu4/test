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
        url = f"https://tracker.gg/valorant/profile/riot/{username}/overview?region=eu"

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Отладочный вывод HTML ответа для проверки структуры страницы
                with open('/mnt/data/response.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)

                # Поиск K/D Ratio
                kd_label = soup.find('span', {'title': 'K/D Ratio'})
                kd_value = kd_label.find_next('span').text.strip() if kd_label else None
                
                # Поиск текущего ранга
                rank_label = soup.find('span', text='Rank')
                rank_value = rank_label.find_next('span').text.strip() if rank_label else None
                
                # Поиск пикового ранга
                peak_rank_label = soup.find('span', text='Peak Rank')
                peak_rank_value = peak_rank_label.find_next('span').text.strip() if peak_rank_label else None

                if kd_value and rank_value and peak_rank_value:
                    await message.edit(f"Статистика игрока {args}:\n\nK/D: {kd_value}\nТекущий ранг: {rank_value}\nПиковый ранг: {peak_rank_value}")
                else:
                    await message.edit("Профиль приватный или не удалось получить данные.")
            else:
                await message.edit("Не удалось получить данные. Проверьте никнейм и попробуйте снова.")
        except Exception as e:
            await message.edit(f"Произошла ошибка: {str(e)}")
