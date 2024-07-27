from django.contrib.auth.models import User
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

class MypageView(generics.RetrieveUpdateAPIView):
    queryset = Mypage.objects.all()
    serializer_class = MypageSerializer
    permission_classes = [CustomReadOnly]

class AddFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # JWT 인증 확인
        if not request.user.is_authenticated:
            raise AuthenticationFailed("User is not authenticated")

        try:
            user_profile = Mypage.objects.get(user=request.user)
            friend_profile = Mypage.objects.get(user__id=user_id)

            if friend_profile in user_profile.friends.all():
                return Response({"detail": "이미 친구입니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            user_profile.friends.add(friend_profile)
            user_profile.save()
            return Response({"detail": "친구 추가 완료"}, status=status.HTTP_200_OK)
        
        except Mypage.DoesNotExist:
            return Response({"detail": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
