from django.urls import path

from .views import UserGetTokenView, UserSignupView

urlpatterns = [
    path('signup/', UserSignupView.as_view()),
    path('token/', UserGetTokenView.as_view())
]
