from django.urls import path, include

from distributions import views

urlpatterns = [
    # API - To Get All Distributions Sent by the Poster
    path('all-distributions/', views.GetAllDistributions.as_view()),
    # API - Post New Distribution
    path('distributions/post/', views.PostNewDistribution.as_view()),
    # API - Get Distribution by ID
    path('distributions/<int:distribution_id>/', views.GetDistributionById.as_view()),
]