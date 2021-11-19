from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.services.repository import (
    TelegramUserRepo,
    HabitRepo,
    EventRepo
)


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, session):
        super().__init__()
        self.session = session

    async def pre_process(self, obj, data, *args):
        try:
            self.session.connection()
            data["session"] = self.session
            data["tg_user_repo"] = TelegramUserRepo(session=self.session)
            data["habit_repo"] = HabitRepo(session=self.session)
            data["event_repo"] = EventRepo(session=self.session)

        except Exception as e:
            print(e)
            self.session.rollback()
            await self.pre_process(obj, data, *args)

    async def post_process(self, obj, data, *args):
        session = data.get("session")
        if session:
            session.close()
