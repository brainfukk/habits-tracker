from datetime import datetime, timedelta

from aiogram.types import CallbackQuery, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.utils.markdown import markdown_decoration
from aiogram.dispatcher import FSMContext

from tgbot.models.keyboards import WelcomeKeyboard
from tgbot.models.states import HabitState
from tgbot.models.keyboards import CancelButton
from tgbot.db.models import Event
from tgbot.services.repository import TelegramUserRepo, HabitRepo, EventRepo
from ...utils import notify_user


async def user_habit(c: CallbackQuery):
    await HabitState.name.set()

    markup = InlineKeyboardMarkup()
    markup.add(CancelButton("Отмена❌", callback_data="cancel_habit_operation").get())
    text = "🙌Отправь название привычки которую ты хочешь добавить..."

    await c.bot.edit_message_text(
        chat_id=c.from_user.id,
        message_id=c.message.message_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup
    )
    await c.bot.answer_callback_query(c.id)


async def user_habit_complete(c: CallbackQuery, tg_user_repo: TelegramUserRepo, event_repo: EventRepo):
    event = event_repo.get(id=c.data.split("_")[-1])
    user = tg_user_repo.get(telegram_id=c.from_user.id)
    event_repo.update(event, values={"is_completed": True})
    markup = InlineKeyboardMarkup()
    text = "*🙌Хэй Хэй!* \n📎Пора закреплять все свои привычки на сегодня!\n\n"

    habits = tg_user_repo.get_habits(user)
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

    await c.bot.answer_callback_query(c.id, "Выполнено✅", show_alert=True)
    await c.bot.edit_message_text(
        message_id=c.message.message_id,
        chat_id=c.from_user.id,
        text=text,
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )
    if event_repo.is_today_events_completed(user):
        await c.bot.send_message(
            chat_id=c.from_user.id,
            text="*👍Вау!*\nА ты крут... Ждем завтрешнего дня!\n\n\n*NEVER GIVE UP!*",
            parse_mode=ParseMode.MARKDOWN
        )


async def user_habit_name(msg: Message, state: FSMContext, habit_repo: HabitRepo, event_repo: EventRepo):
    habit = habit_repo.create(
        user_telegram_id=msg.from_user.id,
        name=msg.text.strip()
    )
    text = "✅Привычка создана успешно!"
    event_repo.create(
        habit_id=habit.id,
        content=msg.text.strip(),
    )
    await msg.reply(
        text=text,
        reply=False
    )
    await state.finish()


async def user_habit_status(c: CallbackQuery):
    await notify_user(c.from_user.id, c.bot)
    await c.bot.answer_callback_query(c.id)


async def cancel_operation(c: CallbackQuery, state: FSMContext, tg_user_repo: TelegramUserRepo):
    await state.finish()
    user = tg_user_repo.get_or_create(
        telegram_id=c.from_user.id,
        first_name=c.from_user.first_name,
        last_name=c.from_user.last_name,
        user_nickname=c.from_user.username,
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

    await c.bot.edit_message_text(
        message_id=c.message.message_id,
        chat_id=c.from_user.id,
        text=welcome_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    await c.bot.answer_callback_query(c.id)
