from rest_framework import serializers
from .models import Post, Comment, Reaction
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar', 'bio')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'is_approved', 'created_at')
        read_only_fields = ('author', 'is_approved')


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'content', 'excerpt', 'status',
                  'featured_image', 'author', 'comments', 'comments_count',
                  'views_count', 'created_at', 'updated_at', 'published_at',
                  'is_synced_to_telegram')
        read_only_fields = ('author', 'slug', 'is_synced_to_telegram')
