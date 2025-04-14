from django.urls import path
from .views import RegisterView, LoginView, Profile, LogOutView

urlpatterns = [
    path('regis/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', Profile.as_view()),
    path('logout/', LogOutView.as_view()),

]