from django.urls import path

from comments import views

urlpatterns = [
    # API - Get All Comments for A Problem
    path('comments/<int:problem_id>/', views.GetCommentsByProblemId.as_view()),
    # API - Post New Comment for the problem
    path('comments/post/', views.PostNewComment.as_view()),
    # API - Get All Replies for A Comment
    path('comments/<int:comment_id>/replies/', views.GetRepliesByCommentId.as_view()),
    # API - Post New Reply for the comment
    path('comments/replies/post/', views.PostNewReply.as_view()),
    # API - Get Comment by ID
    path('comments/comment/<int:comment_id>/', views.GetCommentById.as_view()),
    # API - Get Reply by ID
    path('comments/reply/<int:reply_id>/', views.GetReplyById.as_view()),
    # API - Like Operation
    path('comments/like/', views.LikeOperation.as_view()),
]
