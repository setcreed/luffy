from django.urls import path, re_path

from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view()),
    path('login/mobile/', views.LoginMobileAPIView.as_view()),
    path('sms/', views.SMSAPIView.as_view()),
    path('mobile/', views.MobileCheckAPIView.as_view()),
    path('register/mobile/', views.RegisterMobileAPIView.as_view()),
]
