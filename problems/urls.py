from django.urls import path, include

from problems import views

urlpatterns = [
    path('latest-problems/', views.LatestProblemsList.as_view()),
    path('problems/<slug:tag_slug>/<slug:problem_slug>/', views.ProblemDetail.as_view()),
]


