from django.urls import path
from .views import SignupView, LoginView, MypageView, AddFriendView, ChangePasswordView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('mypage/<int:pk>/', MypageView.as_view()),
    path('add-friend/<int:user_id>/', AddFriendView.as_view(), name='add-friend'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]