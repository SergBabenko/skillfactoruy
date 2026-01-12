from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import confirm_logout, user_profile, RegisterFormView, be_author

urlpatterns = [
    path('register/', RegisterFormView.as_view(template_name='sign/register.html'), name='register'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('sign/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('confirm/logout/', confirm_logout, name='confirm_logout'),
    path('profile/', user_profile, name='user_profile'),
    path('be_author/', be_author, name='be_author'),

]