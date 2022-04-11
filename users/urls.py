from django.urls import path

from . import views

urlpatterns = [
    # API - Get 3 Hot Users
    path('rank-users/', views.RankUserInfosByReputation.as_view()),
    # ex: users/register/
    path('users/register/', views.Register.as_view(), name='register'),
    # ex: users/login/
    path('users/login/', views.Login.as_view(), name='login'),
    # ex: users/update/
    path('users/<int:user_id>/update-email/', views.EmailUpdate.as_view(), name='update'),
    # ex: users/
    path('users/<int:user_id>/', views.UserInfoDetail.as_view(), name='user_info_detail'),
    # ex: users/posted/
    path('users/<int:user_id>/posted-problems/', views.UserPostedProblems.as_view(), name='user_posted_problems'),
    # Get User Address by Username
    path('users/<str:username>/email-address/', views.GetEmailAddressByUsername.as_view()),
    # Get User Accepted Solutions with Date
    path('users/<int:user_id>/accepted-solutions/', views.GetUserAcceptedSolutionsWithDate.as_view()),
]
