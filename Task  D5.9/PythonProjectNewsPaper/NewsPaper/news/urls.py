from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, PostListSearch

urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('<int:pk>/', PostDetail.as_view(), name='post'),
    path('news/search/', PostListSearch.as_view(), name='news_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('news/update/<int:pk>', PostUpdate.as_view(), name='news_update'),
    path('articles/update/<int:pk>', PostUpdate.as_view(), name='articles_update'),
    path('news/delete/<int:pk>', PostDelete.as_view(), name='news_delete'),
    path('articles/delete/<int:pk>', PostDelete.as_view(), name='articles_delete'),
]