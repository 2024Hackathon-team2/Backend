from django.urls import path
from .views import SignupView, LoginView, MypageView, AddFriendView, ChangePasswordView, DeleteView

app_name = 'accounts'
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('mypage/', MypageView.as_view(), name='mypage'),
    path('add-friend/', AddFriendView.as_view(), name='add-friend'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('delete/', DeleteView.as_view(), name='delete-account')
]