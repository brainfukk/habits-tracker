from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class InlineKeyboard:
    def __init__(self, *args, **kwargs):
        self._markup = InlineKeyboardMarkup(*args, **kwargs)

    def init_markup(self, buttons=None):
        if buttons is None:
            buttons = []
        self._markup.add(*buttons)
        return self._markup


class CancelButton:
    def __init__(self, text: str, callback_data: str):
        self._aiogram_btn = InlineKeyboardButton(text=text, callback_data=callback_data)

    def get(self):
        return self._aiogram_btn


class PageButton:
    def __init__(self, text, callback_data: str):
        self._aiogram_btn = InlineKeyboardButton(text=text, callback_data=callback_data)

    def get(self):
        return self._aiogram_btn


class WelcomeKeyboard:
    @staticmethod
    def get():
        buttons = [
            InlineKeyboardButton(text="Создать привычку🤓", callback_data="create_habit"),
            InlineKeyboardButton(text="Статус привычек🟢", callback_data="status_habit"),
        ]
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        return keyboard
