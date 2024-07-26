from django.urls import path
from .views import SignupView, LoginView, LogoutView, MypageView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('mypage/<int:pk>/', MypageView.as_view()),
]