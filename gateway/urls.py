
from django.urls import path
from .views import LoginView, RegisterView, RefreshView, GetSecuredInfo
urlpatterns = [
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('refresh', RefreshView.as_view()),
    path('secured', GetSecuredInfo.as_view()),
]