from django.urls import path

from . import views

urlpatterns = [
    # ex: register/
    path('users/register/', views.Register.as_view(), name='register'),
    # ex: login/
    path('users/login/', views.Login.as_view(), name='login'),
]
