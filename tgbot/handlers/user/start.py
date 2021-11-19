from aiogram.types import Message, ParseMode, CallbackQuery
from aiogram.utils.markdown import markdown_decoration
from tgbot.models.keyboards import WelcomeKeyboard
from tgbot.services.repository import TelegramUserRepo, EventRepo, HabitRepo


async def user_start(
    msg: Message,
    tg_user_repo: TelegramUserRepo,
):
    user = tg_user_repo.get_or_create(
        telegram_id=msg.from_user.id,
        first_name=msg.from_user.first_name,
        last_name=msg.from_user.last_name,
        user_nickname=msg.from_user.username,
        default="telegram_id",
    )

    keyboard = WelcomeKeyboard.get()
    habits = tg_user_repo.get_habits(user)

    welcome_text = markdown_decoration.bold("👋Привет {}!\n\n".format(user.full_name))
    if not len(habits):
        welcome_text += "😔У тебя все еще нет привычек которые нужно закреплять! \n\n\n🚀*Ускоряйся!*"
    else:
        welcome_text += "Список твоих привычек для закрепления: \n"
        for idx, habit in enumerate(habits):
            h_text = markdown_decoration.bold("{}. {}".format(
                idx + 1, habit.name.strip()
            ))
            welcome_text += h_text + "\n"
        welcome_text += "\n\n🚀*Полетели!*"

    await msg.bot.send_message(
        chat_id=msg.from_user.id,
        text=welcome_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
