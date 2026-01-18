# Импорт инструментов для создания таблиц в базе данных
from django.db import models
# Импорт стандартного пользователя Django
from django.contrib.auth.models import AbstractUser
# AbstractUser: Это база. В ней уже есть поля:
# username, password, email, first_name и last_name.
# Мы берем её за основу, чтобы не писать всё с нуля.


class CustomUser(AbstractUser):
    """Расширенная модель пользователя"""
    telegram_id = models.BigIntegerField(
        'Telegram_id',  # 'Telegram_id' - это название поля
        null=True,  # null=True - значит, что поле может быть пустым
        blank=True,  # blank=True - значит, что поле может быть пустым
        unique=True  # unique=True - значит, что поле должно быть уникальным
    )
    telegram_username = models.CharField(
        'Telegram_username',
        max_length=255,
        null=True,
        blank=True
    )
    avatar = models.ImageField(
        'Аватар',  # 'Аватар' - это название поля
        upload_to='avatars/',  # Путь к папке, куда будут сохраняться аватарки
        null=True,
        blank=True
    )
    bio = models.TextField(
        'О себе',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']  # Сортировка по убыванию даты создания
