from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('mypage/', MypageView.as_view(), name='mypage'),
    path('add-friend/<int:user_id>/', AddFriendView.as_view(), name='add-friend'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('delete/', DeleteView.as_view(), name='delete-account'),
    path('delete-friend/<int:friend_id>', DeleteFriendView.as_view(), name='delete-friend'),
    path('friends/', FriendsView.as_view()),
]