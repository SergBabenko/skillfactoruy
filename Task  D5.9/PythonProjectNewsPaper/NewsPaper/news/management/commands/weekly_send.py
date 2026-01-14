import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from news.models import Post


class Command(BaseCommand):
    help = 'Еженедельная рассылка новых статей подписчикам'

    def handle(self, *args, **options):
        last_week = timezone.now() - datetime.timedelta(days=7)

        subscribers = User.objects.filter(categories__isnull=False).distinct()

        for user in subscribers:
            posts = Post.objects.filter(
                category__in=user.categories.all(),
                created_at__gte=last_week
            ).distinct()

            if posts.exists():
                site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
                post_list_text = ""
                for p in posts:
                    post_list_text += f"\n- {p.title}: {site_url}{p.get_absolute_url()}"

                send_mail(
                    subject=f'Недельная рассылка по вашим любимым категориям: {user.username}',
                    message=f'Привет, {user.username} проверьте, что Вы пропустили за неделю:{post_list_text}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                )

                self.stdout.write(self.style.SUCCESS(f'Отправлено для {user.email}'))

