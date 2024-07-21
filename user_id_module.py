from aiogram import types, Dispatcher
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# Глобальная переменная для хранения диспетчера
dp: Dispatcher = None

# Функция для установки диспетчера (передается из юзербота)
def setup_dispatcher(dispatcher: Dispatcher):
    global dp
    dp = dispatcher

# Обработчик для команды .id @username
@dp.message_handler(regexp=r'\.id @(\w+)')
async def id_command(message: types.Message):
    username = message.text.split('@')[1]  # Получаем юзернейм из команды
    try:
        # Получаем информацию о пользователе
        user = await message.bot.get_chat(username)
        await message.reply(f"ID пользователя @{username} - {user.id}")
    except Exception as e:
        await message.reply(f"Не удалось найти пользователя @{username}. Ошибка: {e}")

# Функция для завершения работы модуля (если требуется)
async def on_shutdown(dp: Dispatcher):
    pass


