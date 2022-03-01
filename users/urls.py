from django.urls import path

from . import views

urlpatterns = [
    # ex: users/register/
    path('users/register/', views.Register.as_view(), name='register'),
    # ex: users/login/
    path('users/login/', views.Login.as_view(), name='login'),
    # ex: users/
    path('users/<int:user_id>/', views.UserInfoDetail.as_view(), name='user_info'),
]
