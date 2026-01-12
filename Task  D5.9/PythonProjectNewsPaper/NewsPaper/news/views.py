from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm
from .models import Post
from datetime import datetime
from django_filters.views import FilterView
from .filters import PostFilter
from .utils import add_or_change
from sign.utils import request_object


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
        return add_or_change(context, self.request.path)

    def form_valid(self, form):
        response = super().form_valid(form)
        group_subscribers = request_object('subscribers')
        subscribers_user = group_subscribers.user_set.values_list('email', flat=True)
        send_mail(
            subject="Уведомление по подписке",
            message="Появилась новая публикация",
            from_email="Server@server.ru",
            recipient_list=subscribers_user,
        )

class PostUpdate(PermissionRequiredMixin, UpdateView):
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
