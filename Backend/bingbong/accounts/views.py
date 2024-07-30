from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer, LoginSerializer, MypageSerializer, ChangePasswordSerializer
from .models import Mypage
from .permissions import CustomReadOnly

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': SignupSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response({
            "detail": "로그인 성공",
            "refresh": data['refresh'],
            "access": data['access']
        }, status=status.HTTP_200_OK)

class DeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message" : "계정이 탈퇴되었습니다."}, status=status.HTTP_204_NO_CONTENT)

class MypageView(generics.RetrieveUpdateAPIView):
    queryset = Mypage.objects.all()
    serializer_class = MypageSerializer
    permission_classes = [CustomReadOnly]

    #현재 인증된 사용자의 Mypage객체를 반환
    def get_object(self):
        return Mypage.objects.get(user=self.request.user)

class AddFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_profile = Mypage.objects.get(user=request.user)
            friend_profile = Mypage.objects.get(user__id=user_id)

            if friend_profile in user_profile.friends.all():
                return Response({"detail": "이미 친구입니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            user_profile.friends.add(friend_profile)
            friend_profile.friends.add(user_profile)
            user_profile.save()
            return Response({"detail": "친구 추가 완료"}, status=status.HTTP_200_OK)
        
        except Mypage.DoesNotExist:
            return Response({"detail": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

class DeleteFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, friend_id):
        user = request.user
        user_page = get_object_or_404(Mypage, user=user)
        friend=get_object_or_404(User, pk=friend_id)
        friend_page = get_object_or_404(Mypage, user=friend)

        if friend_page in user_page.friends.all():
            user_page.friends.remove(friend_page)
            friend_page.friends.remove(user_page)
            return Response({"message": "삭제되었습니다."}, status=status.HTTP_200_OK)
        return Response({"message": "내 친구가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

class FriendsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        user_page = get_object_or_404(Mypage, user=user)
        
        friends_list=[]
        for friend in user_page.friends.all():
            user_friend = get_object_or_404(User, pk=friend.pk)
            user_friend_page = get_object_or_404(Mypage, user=user_friend)

            friend_selializer = MypageSerializer(user_friend_page)
            friend_data = friend_selializer.data
            friends_list.append({"friend_pk": friend.pk, "nickname":friend_data['nickname'], "email":user_friend.email})
        return Response({"friends_list": friends_list}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
