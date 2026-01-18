import os
from telegram import Bot
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
TELEGRAM_WEBHOOK_URL = os.getenv('TELEGRAM_WEBHOOK_URL')

bot = Bot(token=TELEGRAM_BOT_TOKEN)


def get_application():
    """Получить Application для бота"""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Команды
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))

    # Текстовые сообщения
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    return application


async def start_command(update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        f"Добро пожаловать на @akulllamx_blog\n\n"
        f"Здесь я делюсь статьями по IoT и Python.\n\n"
        f"Команды: /help"
    )


async def help_command(update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    await update.message.reply_text(
        "🔧 Доступные команды:\n"
        "/start - Начало\n"
        "/help - Помощь\n"
        "/latest - Последние посты\n"
    )


async def handle_message(update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    await update.message.reply_text("Спасибо за сообщение! 😊")
