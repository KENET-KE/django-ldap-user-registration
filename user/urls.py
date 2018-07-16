from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/success/', views.RegisterSuccessView.as_view(), name='register_success'),
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/success/', views.PasswordResetSuccessView.as_view(), name='password_reset_success'),
    ]
