from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import Goal
from .serializers import *
from datetime import datetime
# from permissions import CustomReadOnly # modelviewset으로 바꿀지 고민 중...
# https://newbiecs.tistory.com/316 참고해서 공부하고 코드 변경해보기

class GoalView(APIView):
  def get(self, request):
    now = datetime.now()
    year = now.year
    month = now.month
    user = request.user
    user_id = user.id
    # 없으면 목표가 전부 0이게 새로 생성
    if not Goal.objects.filter(user=user, year=year, month=month).exists():
      data = {
          "user":       user_id,
          "year":       year,
          "month":      month
          # 'soju_goal':  0,
          # 'beer_goal':  0,
          # 'mak_goal':   0,
          # 'wine_goal':  0
        }
      serializer = GoalSerializer(data=data)
      if serializer.is_valid():
        serializer.save()
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    # 사용자의 목표 정보
    # 사용자 id, 목표 연도, 목표 월, 목표 소주량, 목표 맥주량, 목표 막걸리량, 목표 와인량
    goal = get_object_or_404(Goal, user=request.user, year=year, month=month)
    serializer = GoalSerializer(goal)

    # 목표 잔수의 합

    # 현재까지 마신 잔수의 합

    # 남은 잔수의 합

    # 음주 기록을 한 날짜


    return Response(serializer.data, status=status.HTTP_200_OK)
  
  # def post(self, request):
  #   #주종, 주량, 유저
  #   serializer = GoalSerializer(data=request.data)

  def patch(self, request):
    now = datetime.now()
    year = now.year
    month = now.month
    user = request.user

    goal = get_object_or_404(Goal, user=request.user, year=year, month=month)
    
    if goal.user == request.user:
      serializer = GoalPatchSerializer(goal, data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)