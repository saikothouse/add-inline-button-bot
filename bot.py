# coding=utf8
import traceback
import telegram
from telegram import InputMediaPhoto

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

MAIN_MENU, PUSH_NOTIF, START_FIND = range(3)

token = ''
CHANNEL_ONE = ''
CHANNEL_TWO = ''
CHANNEL_LOG = ''
bot = telegram.Bot(token=token)


async def find_games():
    pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.edit_message_text(text="LOOKING FOR THE GAMES OF THE DAY!!")
    # games_day = await find_games()
    games_day = [('HOME', 'AWAY', 'DATE'), ('HOME', 'AWAY', 'DATE'), ('HOME', 'AWAY', 'DATE')]
    for item in range(len(games_day)):
        date = games_day[item][2]
        try:
            media_group = []
            for num in range(3):
                media_group.append(
                    InputMediaPhoto(open('Game-%d.png' % num, 'rb'),
                                    caption=f'{games_day[item][0]} X {games_day[item][1]}\n Date:{date}' if num == 0 else ''))
                await bot.send_media_group(chat_id=CHANNEL_ONE, media=media_group)
                await bot.send_media_group(chat_id=CHANNEL_TWO, media=media_group, disable_notification=True)
                button = [[InlineKeyboardButton(text="🔔", callback_data=PUSH_NOTIF)]]
                await bot.send_message(text="Turn On notification", chat_id=CHANNEL_TWO,
                                       reply_markup=InlineKeyboardMarkup(button), disable_notification=True)

        except Exception:
            error_message = traceback.format_exc()
            text = f'{games_day[item][0]} X {games_day[item][1]}\n Date:{games_day[2]}'
            await bot.send_message(chat_id=CHANNEL_LOG, text=text)
            await bot.send_message(chat_id=CHANNEL_LOG, text=error_message)

    await bot.send_message(chat_id=CHANNEL_ONE, text="END!!!\nTHESE ARE THE GAMES OF TODAY!")


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Start Analysis", reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton("Start", callback_data="start_find")]]))
    return START_FIND


async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    await update.message.reply_text("Welcome, Enter your name to get started:")
    return MAIN_MENU


async def notification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query.data
    await update.callback_query.answer()
    msg_id = update.message.message_id
    print(msg_id)

    if "notification" in query:
        print("SEND NOTIFICATION")
    return PUSH_NOTIF


def main() -> None:
    application = Application.builder().token("6017856307:AAGBh0IB_sFo8_ael8-ScvsPDiRer-fcHJI").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_bot)],
        states={
            MAIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, menu),
            ],
            PUSH_NOTIF: [
                CallbackQueryHandler(notification),
            ],
            START_FIND: [
                CallbackQueryHandler(start),
            ],
        },
        fallbacks=[CommandHandler("start", start),
                   ],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
  
