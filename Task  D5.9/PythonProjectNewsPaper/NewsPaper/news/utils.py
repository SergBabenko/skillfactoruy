import random
from .models import Post

post_types = [ 'News', 'Articles' ]

authors_ids = [1, 2, 3, 4, 5, 6]

def gen_post():
    for i in range(5, 50):
        kwargs = {'author_id':random.choice(authors_ids),
                  'post_type':random.choice(post_types),
                  "title": F"Заголовок поста {i}",
                  "text": F"Содержание поста {i}"
        }

        Post.objects.create(**kwargs)
    print("Все посты успешно созданы!")

def add_or_change(context, request_path):

    if "create" in request_path:
        title = "Добавление "
    else:
        title = "Редактирование "

    if "delete" in request_path:
        title = "Удаление "

    if "news" in request_path:
        title += "Новости"
    else:
        title += "Статьи"

    context['add_or_change'] = title
    return context