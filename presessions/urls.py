from django.urls import path, include

from presessions import views

urlpatterns = [
    # API to Get All Presessions
    path('all-presessions/', views.AllPresessions.as_view()),
    # API to Get Presession by ID
    path('presessions/<int:presession_id>/', views.GetPresessionByID.as_view()),
    # API to Post New Presession
    path('presessions/post/', views.PostNewPresession.as_view()),
    # API to Update Presession
    path('presessions/<int:presession_id>/update/', views.UpdatePresession.as_view()),
]
