from telethon import events
from .. import loader, utils

@loader.tds
class ExampleModule(loader.Module):
    """Описание вашего модуля"""
    strings = {"name": "ExampleModule"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    async def examplecmd(self, message):
        """Команда: .example - Пример команды"""
        await message.edit("Привет! Это пример команды для Hikka.")

    @loader.unrestricted
    async def hello_cmd(self, message):
        """Команда: .hello - Приветствие"""
        await message.edit("Привет! Как дела?")

    @loader.unrestricted
    async def repeatcmd(self, message):
        """Команда: .repeat <текст> - Повторяет текст"""
        text = utils.get_args_raw(message)
        if not text:
            await message.edit("Нужно указать текст для повтора.")
            return
        await message.edit(text)
