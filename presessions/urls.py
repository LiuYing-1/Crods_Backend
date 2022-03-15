from django.urls import path, include

from presessions import views

urlpatterns = [
    # API to Get All Presessions
    path('all-presessions/', views.AllPresessions.as_view()),
    # API to Post New Presession
    path('presessions/post/', views.PostNewPresession.as_view()),
]
