from telethon import events
from .. import loader, utils

@loader.tds
class UserIdModule(loader.Module):
    """Модуль для получения ID пользователя по его юзернейму"""
    strings = {"name": "UserIdModule"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    async def idcmd(self, message):
        """Команда: .id <юзернейм> - Получить ID пользователя по его юзернейму"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("Пожалуйста, укажите юзернейм пользователя.")
            return

        try:
            user = await self.client.get_entity(args)
            await message.edit(f"ID пользователя {args} : {user.id}")
        except Exception as e:
            await message.edit(f"Не удалось получить ID пользователя. Ошибка: {str(e)}")
