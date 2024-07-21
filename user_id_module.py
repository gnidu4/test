from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

# Глобальная переменная для хранения диспетчера
dp: Dispatcher = None

# Функция для установки диспетчера (передается из юзербота)
def setup_dispatcher(dispatcher: Dispatcher):
    global dp
    dp = dispatcher

    # Проверяем, что диспетчер установлен корректно
    if dp is None:
        raise ValueError("Dispatcher is not set properly")

    # Регистрация обработчика
    dp.add_handler(types.MessageHandler(Text(equals='.id @username', ignore_case=True), id_command))

# Обработчик для команды .id @username
async def id_command(message: types.Message):
    username = message.text.split('@')[1]  # Получаем юзернейм из команды
    try:
        # Получаем информацию о пользователе
        user = await message.bot.get_chat(username)
        await message.reply(f"ID пользователя @{username} - {user.id}")
    except Exception as e:
        await message.reply(f"Не удалось найти пользователя @{username}. Ошибка: {e}")

# Функция для завершения работы модуля (если требуется)
async def on_shutdown():
    pass
