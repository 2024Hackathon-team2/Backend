from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import Goal
from .serializers import *
from records.models import *
from records.serializers import *
from datetime import datetime
from decimal import Decimal
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
    # 사용자 id, 목표 연도, 목표 월, 목표 소주량, 목표 맥주량, 목표 막걸리량, 목표 와인량, 목표 총 합
      
    goal = get_object_or_404(Goal, user=request.user, year=year, month=month)
    serializer = GoalSerializer(goal)
    goal = serializer.data
    soju_goal = Decimal(goal['soju_goal'])
    beer_goal = Decimal(goal['beer_goal'])
    mak_goal = Decimal(goal['mak_goal'])
    wine_goal = Decimal(goal['wine_goal'])
    total_goal = soju_goal + beer_goal + mak_goal + wine_goal
    goal = {
      "total_goal": total_goal,
      "soju_goal": soju_goal,
      "beer_goal": beer_goal,
      "mak_goal": mak_goal,
      "wine_goal": wine_goal

    }
    

    # 현재까지 마신 잔수의 합
    date = []
    total_soju = Decimal('0.0')
    total_beer = Decimal('0.0')
    total_mak = Decimal('0.0')
    total_wine = Decimal('0.0')
    total_record = Decimal('0.0')

    records = Record.objects.filter(user=request.user, year=year, month=month)
    for a in records:
      date.append(a.day)
      total_soju += a.soju_record
      total_beer += a.beer_record
      total_mak += a.mak_record
      total_wine += a.wine_record
    total_record = total_soju + total_beer + total_mak + total_wine
    
    record = {
      "total_record":total_record,
      "total_soju":total_soju,
      "total_beer":total_beer,
      "total_mak":total_mak,
      "total_wine":total_wine
    }

    # 남은 잔수의 합
    remainder = Decimal(total_goal) - total_record

    data ={
      "goal": goal,
      "record": {
        "date": date,
        "record_alcohol": record
      },
      "remainder": remainder
    }

    return Response(data, status=status.HTTP_200_OK)
  
  def post(self, request):
    #주종, 주량, 유저
    if not request.user.is_authenticated:
      return Response({"message": "수정 권한이 없습니다."})
    now = datetime.now()
    year = now.year
    month = now.month
    user = request.user
    goal = get_object_or_404(Goal, user=request.user, year=year, month=month)
    serializer = GoalSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
    goal = get_object_or_404(Goal, user=request.user, year=year, month=month)
    serializer = GoalSerializer(goal)
    goal = serializer.data
    soju_goal = Decimal(goal['soju_goal'])
    beer_goal = Decimal(goal['beer_goal'])
    mak_goal = Decimal(goal['mak_goal'])
    wine_goal = Decimal(goal['wine_goal'])
    total_goal = soju_goal + beer_goal + mak_goal + wine_goal
    goal = {
      "total_goal": total_goal,
      "soju_goal": soju_goal,
      "beer_goal": beer_goal,
      "mak_goal": mak_goal,
      "wine_goal": wine_goal
    }


    # 현재까지 마신 잔수의 합
    date = []
    total_soju = Decimal('0.0')
    total_beer = Decimal('0.0')
    total_mak = Decimal('0.0')
    total_wine = Decimal('0.0')
    total_record = Decimal('0.0')
    records = Record.objects.filter(user=request.user, year=year, month=month)
    for a in records:
      date.append(a.day)
      total_soju += a.soju_record
      total_beer += a.beer_record
      total_mak += a.mak_record
      total_wine += a.wine_record
      total_record = total_soju + total_beer + total_mak + total_wine
    
    record = {
      "total_record":total_record,
      "total_soju":total_soju,
      "total_beer":total_beer,
      "total_mak":total_mak,
      "total_wine":total_wine
    }

      # 남은 잔수의 합
    remainder = Decimal(total_goal) - total_record

    data ={
    "goal": goal,
    "record": {
      "date": date,
      "record_alcohol": record
    },
      "remainder": remainder
    }
    return Response(data, status=status.HTTP_200_OK)
    

  def patch(self, request):
    if not request.user.is_authenticated:
      return Response({"message": "수정 권한이 없습니다."})
    now = datetime.now()
    year = now.year
    month = now.month
    user = request.user

    goal = get_object_or_404(Goal, user=request.user, year=year, month=month)
    
    if goal.user == request.user:
      serializer = GoalPatchSerializer(goal, data=request.data)
      if serializer.is_valid():
        serializer.save()
      
      goal = get_object_or_404(Goal, user=request.user, year=year, month=month)
      serializer = GoalSerializer(goal)
      goal = serializer.data
      soju_goal = Decimal(goal['soju_goal'])
      beer_goal = Decimal(goal['beer_goal'])
      mak_goal = Decimal(goal['mak_goal'])
      wine_goal = Decimal(goal['wine_goal'])
      total_goal = soju_goal + beer_goal + mak_goal + wine_goal
      goal = {
        "total_goal": total_goal,
        "soju_goal": soju_goal,
        "beer_goal": beer_goal,
        "mak_goal": mak_goal,
        "wine_goal": wine_goal
      }
    

      # 현재까지 마신 잔수의 합
      date = []
      total_soju = Decimal('0.0')
      total_beer = Decimal('0.0')
      total_mak = Decimal('0.0')
      total_wine = Decimal('0.0')
      total_record = Decimal('0.0')

      records = Record.objects.filter(user=request.user, year=year, month=month)
      for a in records:
        date.append(a.day)
        total_soju += a.soju_record
        total_beer += a.beer_record
        total_mak += a.mak_record
        total_wine += a.wine_record
      total_record = total_soju + total_beer + total_mak + total_wine
    
      record = {
        "total_record":total_record,
        "total_soju":total_soju,
        "total_beer":total_beer,
        "total_mak":total_mak,
        "total_wine":total_wine
      }

      # 남은 잔수의 합
      remainder = Decimal(total_goal) - total_record

      data ={
      "goal": goal,
      "record": {
        "date": date,
        "record_alcohol": record
      },
        "remainder": remainder
      }
      return Response(data, status=status.HTTP_200_OK)
    else:
      return Response({"message": "수정 권한이 없습니다."})
    
  def delete(self, request):
    now = datetime.now()
    year = now.year
    month = now.month
    user = request.user

    goal = get_object_or_404(Goal, user=request.user, year=year, month=month)
    if request.uesr == goal.user:
      goal.delete()
      return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    else:
      return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

class SocialView(APIView):
  def get(self, request):

    return Response()