# from aiogram import Dispatcher
# from aiogram.dispatcher import FSMContext
# from aiogram.types import Message
#
# from tgbot.models.keyboards import CancelButton, InlineKeyboard
# from tgbot.models.role import UserRole
# from tgbot.services.repository import TelegramUserRepo
#
#
# async def admin_change_plan_step_1(m: Message):
#     await AdminUpdateState.data.set()
#     keyboard = InlineKeyboard().init_markup(
#         [CancelButton(text="Назад в меню", callback_data="backto_welcome").get()]
#     )
#     await m.reply(text="Send me data in format tg_id:plan", reply_markup=keyboard)
#
#
# async def admin_change_plan_step_2(
#     m: Message, state: FSMContext, tg_user_repo: TelegramUserRepo
# ):
#     tg_id, plan = m.text.split("-")
#
#     if plan.upper() == "PREMIUM":
#         plan = PlanChoices.PREMIUM
#     elif plan.upper() == "DEFAULT":
#         plan = PlanChoices.DEFAULT
#
#     user = tg_user_repo.get(telegram_id=int(tg_id.strip()))
#     tg_user_repo.update(instance=user, values={"plan": plan})
#
#     await m.reply(
#         text="User's {} plan has been updated to {}.".format(
#             user.telegram_id, plan.value
#         )
#     )
#     await m.bot.send_message(
#         chat_id=user.telegram_id,
#         text="Ваша подписка была обновлена до уровня {}".format(plan.value),
#     )
#     await state.finish()
#
#
# def register_admin(dp: Dispatcher):
#     dp.register_message_handler(
#         admin_change_plan_step_1,
#         commands=["change_plan"],
#         state="*",
#         role=UserRole.ADMIN,
#     )
#     dp.register_message_handler(
#         admin_change_plan_step_2, state=AdminUpdateState.data, role=UserRole.ADMIN
#     )
#     # # or you can pass multiple roles:
#     # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
#     # # or use another filter:
#     # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
