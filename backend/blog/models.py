from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify  # Для создания слагов


User = get_user_model()

class Post(models.Model):
    """Модель для хранения постов."""
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # Синхронизация с Telegram
    telegram_message_id = models.BigIntegerField(null=True, blank=True)
    is_synced_to_telegram = models.BooleanField(default=False)

    # Медиа
    featured_image = models.ImageField(
        upload_to='blog/featured/', null=True, blank=True
    )

    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    views_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-published_at']  # По дате публикации по убыванию


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
