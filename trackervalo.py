import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
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

        await message.edit("Получаю данные...")

        # Настройка Selenium WebDriver
        try:
            # Инициализация WebDriver
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            driver.get(url)
            time.sleep(5)  # Ждем загрузки страницы

            # Парсинг данных
            stats = {}
            stats['Имя'] = f"{name}#{tag}"

            # Пример парсинга статистики (адаптируйте под текущую структуру сайта)
            stats_elements = driver.find_elements(By.CLASS_NAME, 'stat')
            for element in stats_elements:
                stat_name = element.find_element(By.CLASS_NAME, 'name').text.strip()
                stat_value = element.find_element(By.CLASS_NAME, 'value').text.strip()
                stats[stat_name] = stat_value

            stats_message = '\n'.join([f"{key}: {value}" for key, value in stats.items()])
            await message.edit(stats_message)

            driver.quit()

        except Exception as e:
            await message.edit(f"Произошла ошибка: {str(e)}")

        finally:
            if 'driver' in locals():
                driver.quit()
