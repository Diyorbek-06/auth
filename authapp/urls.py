from django.urls import path
from .views import RegisterView, LoginView, Profile, LogOutView, ChangePassword, AuthOne, AuthTwo, Main

urlpatterns = [
    path('main/', Main.as_view()),
    path('regis/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', Profile.as_view()),
    path('logout/', LogOutView.as_view()),
    path('change-password/', ChangePassword.as_view()),
    path('auth-one/', AuthOne.as_view()),
    path('auth-two/', AuthTwo.as_view()),
]