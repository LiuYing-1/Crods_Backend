from django.urls import path, include

from emails import views

urlpatterns = [
    # API - Get User Emails by Email Address
    path('emails/<str:receiver_address>/', views.GetEmailsByReceiverAddress.as_view()),
    # API - Get User Sent Emails by Email Address
    path('emails/<str:sender_address>/sent/', views.GetSentEmailsBySenderAddress.as_view()),
    # API - Get Email by ID
    path('emails/email/<int:pk>/', views.GetEmailById.as_view()),
    # API - Set Email Status from Unread to Read
    path('emails/email/<int:pk>/change-status/', views.ChangeEmailStatusToRead.as_view()),
    # API - Check User Email Address Whether Valid
    path('emails/<str:receiver_address>/check-valid/', views.CheckValidAddress.as_view()),
    # API - Send Email to Target User
    path('emails/email/post/', views.WriteEmailToOthers.as_view()),
]