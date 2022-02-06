from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup/', RegisterView.as_view()),
    path('loginweb/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user/', UserView.as_view()),
    path('login/', obtain_auth_token,
         name='api_token_auth'),
]
