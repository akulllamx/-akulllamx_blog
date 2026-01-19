from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

from .models import Post, Comment
from .forms import CommentForm, PostForm


def home(request):
    """Главная страница с последними постами"""
    posts = Post.objects.filter(
        status='published'
    ).exclude(slug='').order_by('-published_at')[:6]
    return render(request, 'home.html', {'posts': posts})


class PostListView(ListView):
    """Список всех постов"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(
            status='published'
        ).exclude(slug='').order_by('-published_at')


class PostDetailView(DetailView):
    """Детальный вид одного поста"""
    model = Post
    template_name = 'blog/post_detail.html'
    slug_field = 'slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Увеличиваем счетчик просмотров
        self.object.views_count += 1
        self.object.save(update_fields=['views_count'])

        context['comments'] = self.object.comments.filter(is_approved=True)
        return context


@login_required(login_url='/admin/login/')
def create_post(request):
    """Создание нового поста (только для администраторов)"""
    if not request.user.is_staff:
        raise Http404("У вас нет прав на это действие.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})


@login_required
def edit_post(request, slug):
    """Редактирование поста"""
    post = get_object_or_404(Post, slug=slug)
    if not request.user.is_staff:
        raise Http404("У вас нет прав на редактирование")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, slug):
    """Удаление поста"""
    post = get_object_or_404(Post, slug=slug)
    if not request.user.is_staff:
        raise Http404("У вас нет прав на удаление")

    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')

    return render(request, 'blog/delete_post.html', {'post': post})


@login_required
@require_POST
def add_comment(request, post_id):
    """Добавить комментарий"""
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content')
    if content:
        Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            is_approved=True
        )
    return redirect('blog:post_detail', slug=post.slug)


@require_POST
@csrf_exempt  # Осторожно! Лучше использовать CSRF-токен
def add_reaction(request, post_id):
    """API для добавления реакций"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)

    post = get_object_or_404(Post, id=post_id)
    reaction_type = request.POST.get('reaction_type', 'like')

    # Логика сохранения реакции (пример)
    # Reaction.objects.get_or_create(user=request.user, post=post, defaults={'reaction': reaction_type})

    return JsonResponse({'success': True})

