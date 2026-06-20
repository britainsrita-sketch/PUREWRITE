import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- LOGGING SETUP ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- ENVIRONMENT VARIABLES ---
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/gladiatoracademy99")

# --- IMAGE LIST ---
IMAGES = [
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/10.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/99.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/88.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/77.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/66.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/55.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/44.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/33.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/22.jpeg",
    "https://raw.githubusercontent.com/agboolatunmise2020-ctrl/PureWrite/main/11.jpeg"
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command with button only (intro message removed)."""

    keyboard = [
        [InlineKeyboardButton("👉 جاهز، أرني النتائج", callback_data="get_pics")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👇",
        reply_markup=reply_markup
    )


async def send_media_and_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends images and final channel link."""

    query = update.callback_query
    await query.answer()

    chat_id = update.effective_chat.id

    media_group = [
        InputMediaPhoto(media=url) for url in IMAGES
    ]

    try:
        await context.bot.send_media_group(
            chat_id=chat_id,
            media=media_group
        )

        final_text = (
            "داخل القناة:\n"
            "• تحليل قبل أي صفقة\n"
            "• خطة كاملة (Entry / SL / TP)\n"
            "• تحديثات مباشرة خلال جلسات لندن و نيويورك\n\n"
            "الدخول مفتوح لفترة محدودة ⏳"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "👉 دخول القناة الرسمية",
                    url=CHANNEL_LINK
                )
            ]
        ]

        await context.bot.send_message(
            chat_id=chat_id,
            text=final_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except Exception as e:
        logger.error(f"Error sending images: {e}")

        await context.bot.send_message(
            chat_id=chat_id,
            text="Error loading images. Please check if files are on GitHub."
        )


def main():
    """Starts the bot."""

    if not TOKEN:
        print("Error: BOT_TOKEN not found in environment variables.")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(
            send_media_and_link,
            pattern="^get_pics$"
        )
    )

    print("Vantagerise Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
