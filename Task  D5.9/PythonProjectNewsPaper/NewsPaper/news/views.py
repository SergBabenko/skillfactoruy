from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime
from django.shortcuts import render

class PostList(ListView):

    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'

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
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    # def post(request, pk):
    #    post = Post.objects.get(pk=pk)
    #    return render(request, 'post.html', {'post': post})