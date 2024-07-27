from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import SignupSerializer, LoginSerializer, MypageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Mypage
from .permissions import CustomReadOnly


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({"detail": "로그인 성공", "token":token.key}, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"detail": "로그아웃되었습니다."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "로그아웃할 수 없습니다. 토큰이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
    
class MypageView(generics.RetrieveUpdateAPIView):
    queryset = Mypage.objects.all()
    serializer_class = MypageSerializer
    permission_classes = [CustomReadOnly]

class AddFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try: 
            user_profile = Mypage.objects.get(user=request.user)
            friend_profile=Mypage.objects.get(user__id=user_id)

            if friend_profile in user_profile.friends.all():
                return Response({"detail": "이미 친구입니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            user_profile.friends.add(friend_profile)
            user_profile.save()
            return Response({"detail" : "친구 추가 완료"}, status=status.HTTP_200_OK)
        
        except Mypage.DoesNotExist:
            return Response({"detail":"사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

