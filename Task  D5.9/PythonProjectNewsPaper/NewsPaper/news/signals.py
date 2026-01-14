from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_save
from django.utils import timezone
from .models import Category, Post, PostCategory

@receiver(m2m_changed, sender=PostCategory)
def new_post_notify(sender, instance, action, pk_set, **kwargs):

    if action == 'post_add':
        user = User.objects.get(pk__in=pk_set)
        categories = instance.category.all()
        subscribers = []
        for cat in categories:
            subscribers.extend(cat.subscribers.all())

        subscribers = list(set(subscribers))

        for user in subscribers:
            if user.email:
                send_mail(
                    subject=f'Новый пост в категории: {instance.title}',
                    message = f'Привет, {user.username} В категориях {", ".join([c.name for c in categories])} появился новый пост.\
                    Ссылка: SITE_URL{instance.get_absolute_url()}',
                    from_email = settings.DEFAULT_FROM_EMAIL,
                    recipient_list = [user.email],
                )




@receiver(pre_save, sender=Post)
def post_restriction_notice(sender, instance, *args, **kwargs):
    if instance.pk:
        return
    before_datetime = timezone.now() - timedelta(days=1)
    posts_count = Post.objects.filter(author=instance.author, created_at__gte=before_datetime).count()
    if posts_count >= 3:
        raise PermissionDenied('Лимит создания постов исчерпан, Ваш лимит 3 поста в сутки!')


@receiver(m2m_changed, sender=Category.subscribers.through)
def subscribers_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        user=User.objects.get(pk__in=pk_set)
        send_mail(
            subject='Новая подписка',
            message=f'Привет, {user.username} Вы подписались на категорию: {instance.name}, \
            Список ваших подписок: {[cat.name for cat in user.categories.all()]}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
    if action == 'post_remove':
        user=User.objects.get(pk__in=pk_set)
        send_mail(
            subject='Отмена подписки',
            message=f'Привет, {user.username} Вы отписались от категории: {instance.name}, \
            Список ваших подписок: {[cat.name for cat in user.categories.all()]}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
