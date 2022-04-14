from django.urls import path, include

from problems import views

urlpatterns = [
    path('latest-problems/', views.LatestProblemsList.as_view()),
    path('all-problems/', views.GetAllProblems.as_view()),
    path('problems/search/', views.search),
    path('problems/post/', views.PostNewProblem.as_view()),
    path('problems/<int:problem_id>/update/', views.problemUpdate.as_view()),
    path('problems/<slug:tag_slug>/<slug:problem_slug>/', views.ProblemDetail.as_view()),
    path('problems/<int:status>/', views.ProblemsByStatus.as_view()),
    path('problems/<slug:tag_slug>/', views.TagDetail.as_view()),
]


