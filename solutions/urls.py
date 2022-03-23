from django.urls import path, include

from solutions import views

urlpatterns = [
    # Get Solution By User_Id (Picker)
    path('solutions/<int:picker_id>/', views.GetSolutionsByPickerId.as_view()),
    # Get Solution By Solution_Id
    path('solutions/solution/<int:solution_id>/', views.GetSolutionById.as_view()),
    # Get Solution By Problem_Id
    path('solutions/problem/<int:problem_id>/', views.GetSolutionByProblemId.as_view()),
    # Update Solution
    path('solutions/solution/<int:solution_id>/update/', views.UpdateSolution.as_view()),
]
