# from django.shortcuts import render, get_object_or_404
# from django.views.generic import ListView, DetailView
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.views.decorators.http import require_POST
# from .models import Post, Comment
# from .forms import CommentForm, PostForm
#
#
# def home(request):
#     """Главная страница с последними постами"""
#     posts = Post.objects.filter(status='published').order_by('-published_at')[:6]
#     return render(request, 'home.html', {'posts': posts})
#
#
# class PostListView(ListView):
#     """Список всех постов"""
#     model = Post
#     template_name = 'blog/post_list.html'
#     context_object_name = 'posts'
#     paginate_by = 10
#
#     def get_queryset(self):
#         return Post.objects.filter(status='published').order_by('-published_at')
#
#
# class PostDetailView(DetailView):
#     """Детальный вид одного поста"""
#     model = Post
#     template_name = 'blog/post_detail.html'
#     slug_field = 'slug'
#     context_object_name = 'post'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Увеличиваем счетчик просмотров
#         self.object.views_count += 1
#         self.object.save(update_fields=['views_count'])
#
#         context['comments'] = self.object.comments.filter(is_approved=True)
#         return context
#
#
# @login_required
# def create_post(request):
#     """Создание нового поста (только для администраторов)"""
#     if not request.user.is_staff:
#         return render(request, '403.html', status=403)
#
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             # Здесь будет отправка в Telegram
#             return redirect('blog:post_detail', slug=post.slug)
#     else:
#         form = PostForm()
#
#     return render(request, 'blog/create_post.html', {'form': form})
#
#
# @login_required
# @require_POST
# def add_comment(request, post_id):
#     """Добавить комментарий"""
#     post = get_object_or_404(Post, id=post_id)
#
#     if request.method == 'POST':
#         content = request.POST.get('content')
#         if content:
#             comment = Comment.objects.create(
#                 post=post,
#                 author=request.user,
#                 content=content,
#                 is_approved=True  # Можно сделать модерацию позже
#             )
#             # Отправляем в Telegram
#             return redirect('blog:post_detail', slug=post.slug)
#
#     return redirect('blog:post_detail', slug=post.slug)
#
#
# def add_reaction(request, post_id):
#     """API для добавления реакций"""
#     if not request.user.is_authenticated:
#         return JsonResponse({'error': 'Not authenticated'}, status=401)
#
#     post = get_object_or_404(Post, id=post_id)
#     reaction_type = request.POST.get('reaction_type', 'like')
#
#     # Здесь добавляешь логику для создания реакции
#     return JsonResponse({'success': True})

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post


def home(request):
    """Главная страница"""
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})


def post_list(request):
    """Список всех постов"""
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, slug):
    """Детальный вид поста"""
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404("Пост не найден")
    return render(request, 'blog/post_detail.html', {'post': post})

