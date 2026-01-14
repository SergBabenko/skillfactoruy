import datetime
from django.utils import timezone
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Post


@shared_task
def send_notification_task(post_id):
    try:
        instance = Post.objects.get(pk=post_id)
        categories = instance.category.all()

        subscribers_emails = User.objects.filter(
            categories__in=categories,
            email__isnull=False
        ).exclude(email='').values_list('email', flat=True).distinct()

        category_names = ", ".join([c.name for c in categories])

        for email in subscribers_emails:
            send_mail(
                subject=f'Новый пост: {instance.title}',
                message=f'В категориях {category_names} появился новый пост.\n'
                        f'Ссылка: {settings.SITE_URL}{instance.get_absolute_url()}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
    except Post.DoesNotExist:
        pass


@shared_task
def weekly_newsletter_task():
    last_week = timezone.now() - datetime.timedelta(days=7)
    subscribers = User.objects.filter(categories__isnull=False).distinct()
    site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')

    for user in subscribers:
        posts = Post.objects.filter(
            category__in=user.categories.all(),
            created_at__gte=last_week
        ).distinct()

        if posts.exists():
            post_list_text = "\n".join([f"- {p.title}: {site_url}{p.get_absolute_url()}" for p in posts])

            send_mail(
                subject=f'Еженедельная подборка для {user.username}',
                message=f'Привет, {user.username}! Посмотрите, что нового появилось за неделю:{post_list_text}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )