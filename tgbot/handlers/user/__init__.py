from aiogram import Dispatcher

from .start import user_start
from .habit import user_habit, user_habit_name, cancel_operation, user_habit_complete, user_habit_status
from tgbot.models.role import UserRole
from tgbot.models.states import HabitState


def register_user(dp: Dispatcher):
    dp.register_message_handler(
        user_start,
        commands=["start"],
        state="*",
        role=[UserRole.ADMIN, UserRole.USER]
    )
    dp.register_callback_query_handler(
        user_habit,
        lambda c: "create_habit" == c.data.lower(),
        state="*",
        role=[UserRole.ADMIN, UserRole.USER]
    )
    dp.register_message_handler(
        user_habit_name,
        state=HabitState.name,
        role=[UserRole.ADMIN, UserRole.USER]
    )
    dp.register_callback_query_handler(
        user_habit_status,
        lambda c: c.data == "status_habit",
        role=[UserRole.ADMIN, UserRole.USER]
    )
    dp.register_callback_query_handler(
        user_habit_complete,
        lambda c: c.data.startswith("eventcomplete"),
        role=[UserRole.ADMIN, UserRole.USER]
    )
    dp.register_callback_query_handler(
        cancel_operation,
        lambda c: "cancel_habit_operation" == c.data.lower(),
        state="*",
        role=[UserRole.ADMIN, UserRole.USER]
    )
