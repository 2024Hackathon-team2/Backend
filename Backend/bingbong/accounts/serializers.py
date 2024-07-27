from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token 
from rest_framework.validators import UniqueValidator
from .models import Mypage

# 회원가입 시리얼라이저
class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')  # 'username' 필드를 제외

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
        )
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],  # 이메일을 'username'으로 사용
            email=validated_data['email'],
            password=validated_data['password'],
        )
        Token.objects.create(user=user)  # 토큰 생성
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {"error": "일치하는 회원 정보가 없습니다."}
        )
    
class MypageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mypage
        fields = ("nickname", "image", "friends")
