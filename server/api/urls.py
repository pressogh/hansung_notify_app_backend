from django.urls import path, include
from .views import *

urlpatterns = [
    path("auth/register", RegistrationAPI.as_view()),
    path("auth/login", LoginAPI.as_view()),
    path('auth/user/<int:user_pk>', UserAPI.as_view()),
    path('auth/profile/<int:user_pk>', ProfileUpdateAPI.as_view()),
    path('user/file', fileAPI.as_view()),
    path('user/homework', homeworkAPI.as_view()),
    path('user/quiz', quizAPI.as_view()),
    path('user/notice', noticeAPI.as_view()),
    path('user/class', classAPI.as_view()),
]