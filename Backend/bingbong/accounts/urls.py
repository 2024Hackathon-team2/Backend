from django.urls import path
from .views import SignupView, LoginView, LogoutView, MypageView, AddFriendView, ChangePasswordView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('mypage/<int:pk>/', MypageView.as_view()),
    path('add-friend/<int:user_id>/', AddFriendView.as_view(), name='add-friend'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]