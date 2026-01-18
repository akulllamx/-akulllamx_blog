from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Comment
from apps.telegram_bot.utils import send_post_to_telegram, send_comment_to_telegram


@receiver(post_save, sender=Post)
def post_published(sender, instance, created, **kwargs):
    """Автоматически отправить пост в Telegram при публикации"""
    if instance.status == 'published' and not instance.is_synced_to_telegram:
        # Отправляем пост в Telegram канал
        message_id = send_post_to_telegram(instance)

        if message_id:
            instance.telegram_message_id = message_id
            instance.is_synced_to_telegram = True
            instance.save(update_fields=['telegram_message_id', 'is_synced_to_telegram'])


@receiver(post_save, sender=Comment)
def comment_posted(sender, instance, created, **kwargs):
    """Отправить комментарий в Telegram тред"""
    if created and instance.is_approved and not instance.is_synced_to_telegram:
        message_id = send_comment_to_telegram(instance)

        if message_id:
            instance.telegram_message_id = message_id
            instance.is_synced_to_telegram = True
            instance.save(update_fields=['telegram_message_id', 'is_synced_to_telegram'])


# apps/apps.py
from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blog'

    def ready(self):
        import apps.blog.signals  # Подключаем signals
