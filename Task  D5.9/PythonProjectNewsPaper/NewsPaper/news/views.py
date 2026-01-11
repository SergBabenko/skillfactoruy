from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm
from .models import Post
from datetime import datetime
from django_filters.views import FilterView
from .filters import PostFilter
from .utils import add_or_change

class PostList(ListView):

    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostListSearch(FilterView):

    model = Post
    ordering = '-created_at'
    template_name = 'search_list.html'
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
    template_name = 'post.html'
    context_object_name = 'post'

    # def post(request, pk):
    #    post = Post.objects.get(pk=pk)
    #    return render(request, 'post.html', {'post': post})

class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_or_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return add_or_change(context, self.request.path)

class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'add_or_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return add_or_change(context, self.request.path)

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy("posts")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return add_or_change(context, self.request.path)
