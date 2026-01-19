from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify  # Для создания слагов


User = get_user_model()

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    ]

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='URL')
    content = models.TextField(verbose_name='Содержание')
    excerpt = models.TextField(max_length=300, blank=True, verbose_name='Краткое описание')
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='Изображение')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Статус'
    )
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            # Генерируем slug только из латиницы
            self.slug = slugify(self.title, allow_unicode=False)
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель для комментариев."""
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    content = models.TextField()

    # Синхронизация с Telegram
    telegram_message_id = models.BigIntegerField(null=True, blank=True)
    is_synced_to_telegram = models.BooleanField(default=False)

    # Модерация
    is_approved = models.BooleanField(default=False)  # False - ожидает модерации

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Комментарий от {self.author.username} к посту {self.post.title}"

    class Meta:
        ordering = ['-created_at']  # По дате создания по убыванию


class Reaction(models.Model):
    """Модель для реакций на посты."""
    REACTION_CHOICES = [
        ('like', '👍 Like'),
        ('love', '❤️ Love'),
        ('haha', '😂 Haha'),
        ('wow', '😮 Wow'),
        ('sad', '😢 Sad'),
        ('angry', '😠 Angry'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'user']  # Одиночная реакция на пост
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.reaction_type} на {self.post.title}"
