from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'image', 'status']
        widgets = {
            'status': forms.Select(choices=Post.STATUS_CHOICES),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
