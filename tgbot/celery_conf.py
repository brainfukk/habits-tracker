from datetime import datetime, timedelta

from celery import Celery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.core.config import CeleryConfigDocker
from tgbot.db.database import session_scope
from tgbot.services.repository import TelegramUserRepo, EventRepo
from tgbot.db.models import Event
from tgbot.services.bot import sync_send_message


celery_app = Celery("tasks")
celery_app.config_from_object(CeleryConfigDocker)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        timedelta(minutes=15), notify_users.s(), name="Notify users every 15min"
    )


@celery_app.task
def notify_users():
    with session_scope() as session:
        user_repo = TelegramUserRepo(session=session)
        event_repo = EventRepo(session=session)
        users = user_repo.list()

        for user in users:
            text = "*🙌Хэй Хэй!* \n📎Пора закреплять все свои привычки на сегодня!\n\n"
            markup = InlineKeyboardMarkup()
            habits = user_repo.get_habits(user)

            if event_repo.is_today_events_completed(user):
                continue

            for idx, habit in enumerate(habits):
                event = event_repo.filter([
                    Event.habit_id == habit.id,
                    Event.created_at >= datetime.now() - timedelta(days=1),
                    Event.created_at <= datetime.now(),
                ])
                if not len(event):
                    event = event_repo.create(
                        habit_id=habit.id,
                        content=habit.name,
                    )

                event = event[0] if isinstance(event, list) else event
                event_emoji = "✅"
                if not event.is_completed:
                    event_emoji = "❌"
                    markup.add(InlineKeyboardButton(
                        text="{}... ✅".format(event.content[:20]),
                        callback_data="eventcomplete_{}".format(event.id),
                    ))
                text += "{}*{}. {}*\n".format(event_emoji, idx + 1, event.content)
            sync_send_message(
                chat_id=user.telegram_id,
                text=text,
                reply_markup=markup
            )
