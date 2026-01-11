from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum
from django.urls import reverse_lazy


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):

        posts_rating = self.post_set.aggregate(sum_rating = Sum('rating'))['sum_rating'] or 0

        posts_rating *= 3

        comments_rating = self.user.comment_set.aggregate(sum_rating=Sum('rating'))['sum_rating'] or 0

        comments_to_posts_rating = Comment.objects.filter(post__author__user=self.user).aggregate(sum_rating=Sum('rating'))['sum_rating'] or 0

        self.rating = posts_rating + comments_rating + comments_to_posts_rating
        self.save()

    def __str__(self):
        return f'{self.user.username} (Rating: {self.rating})'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    TYPE_CHOICES = (("News", "Новость"),("Articles", "Статья"))
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=100, choices=TYPE_CHOICES, default="News")
    category = models.ManyToManyField(Category, through="PostCategory")
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(default=0)



    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) <= 124:
            return self.text
        else:
            return self.text[:124] + "..."

    def __str__(self):
        return f'{self.title}: {self.preview()}'

    def get_absolute_url(self):
        return reverse_lazy('post', kwargs={'pk': self.pk})

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'