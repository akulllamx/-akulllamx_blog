import os
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
bot = Bot(token=TELEGRAM_BOT_TOKEN)


def send_post_to_telegram(post):
    """Отправить пост в Telegram канал"""
    try:
        message_text = (
            f"<b>{post.title}</b>\n\n"
            f"{post.excerpt or post.content[:200]}\n\n"
            f"<a href='https://yourdomain.com/blog/{post.slug}/'>Читать полностью →</a>\n\n"
            f"#blog #akulllamx_blog"
        )

        message = bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID,
            text=message_text,
            parse_mode='HTML',
            disable_web_page_preview=False
        )

        return message.message_id
    except TelegramError as e:
        print(f"Ошибка отправки поста в Telegram: {e}")
        return None


def send_comment_to_telegram(comment):
    """Отправить комментарий в тред поста"""
    try:
        if not comment.post.telegram_message_id:
            return None

        message_text = (
            f"💬 Новый комментарий от @{comment.author.telegram_username or comment.author.username}:\n\n"
            f"{comment.content}"
        )

        message = bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID,
            text=message_text,
            reply_to_message_id=comment.post.telegram_message_id,
            parse_mode='HTML'
        )

        return message.message_id
    except TelegramError as e:
        print(f"Ошибка отправки комментария в Telegram: {e}")
        return None
