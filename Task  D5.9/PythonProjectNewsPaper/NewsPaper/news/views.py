from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm
from .models import Post, Category
from datetime import datetime, timedelta
from django_filters.views import FilterView
from .filters import PostFilter
from .utils import add_or_change



class PostList(ListView):

    model = Post
    ordering = '-created_at'
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostListSearch(FilterView):

    model = Post
    ordering = '-created_at'
    template_name = 'news/search_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    filterset_class = PostFilter

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.post_filtered = PostFilter(self.request.GET, queryset=queryset)
    #     return self.post_filtered.qs

    #def posts(request):
    #    posts = Post.objects.all()
    #    return render(request, 'posts.html', {'posts': posts})

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.now()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_post'] = None
        # context['filter'] = self.post_filtered
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    # def post(request, pk):
    #    post = Post.objects.get(pk=pk)
    #    return render(request, 'post.html', {'post': post})

class PostCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/add_or_change.html'
    permission_required = 'news.add_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        before_datetime = timezone.now() - timedelta(days=1)
        posts_count = Post.objects.filter(author=self.request.user.author, created_at__gte=before_datetime).count()
        context['posts_limit'] = posts_count < 300
        return add_or_change(context, self.request.path)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.author
        if 'articles' in self.request.path:
            post.post_type = 'Articles'
        post.save()

        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/add_or_change.html'
    permission_required = 'news.change_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return add_or_change(context, self.request.path)

class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy("posts")
    permission_required = 'news.delete_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return add_or_change(context, self.request.path)

class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'news/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return add_or_change(context, self.request.path)

@login_required
def subscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unsubscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER'))
