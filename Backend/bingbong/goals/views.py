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
from rest_framework.permissions import IsAuthenticated
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
    user = goal['user']
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
    if total_goal == 0:
      percentage = 0
    else:
      percentage = total_record/total_goal * 100

    data ={
      "user": user,
      "goal": goal,
      "record": {
        "date": date,
        "record_alcohol": record
      },
      "percentage":percentage
      ,
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
    user = goal['user']
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
    if total_goal == 0:
      percentage = 0
    else:
      percentage = total_record/total_goal * 100
    data ={
      "user": user,
    "goal": goal,
    "record": {
      "date": date,
      "record_alcohol": record
    },
    "percentage":percentage
      ,
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
      user = goal['user']
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
      if total_goal == 0:
        percentage = 0
      else:
        percentage = total_record/total_goal * 100
      data ={
      "user": user,
      "goal": goal,
      "record": {
        "date": date,
        "record_alcohol": record
      },
      "percentage":percentage
      ,
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
    if request.user == goal.user:
      goal.delete()
      return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    else:
      return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

class SocialView(APIView):
  def get(self, request):
    now   = datetime.now()
    year  = now.year
    month = now.month
    day   = now.day

    #목표
    goal = get_object_or_404(Goal, user=request.user, year=year, month=month)
    goal_serializer = GoalSerializer(goal)
    goal_data = goal_serializer.data
    
    #응원
    cheer = goal_data['cheer']
    #사용자 설정 목표
    soju_goal = Decimal(goal_data['soju_goal'])
    beer_goal = Decimal(goal_data['beer_goal'])
    mak_goal  = Decimal(goal_data['mak_goal'])
    wine_goal = Decimal(goal_data['wine_goal'])

    #기록
    records = Record.objects.filter(user=request.user, year=year, month=month)
    soju_record = 0.0
    beer_record = 0.0
    mak_record  = 0.0
    wine_record = 0.0

    for record in records:
      soju_record += record.soju_record
      beer_record += record.beer_record
      mak_record  += record.mak_record
      wine_record += record.wine_record
    
    #목표 달성율
    soju = {
      "goal"        : soju_goal,
      "record"      : soju_record,
      "percentage"  : soju_record/soju_goal if soju_goal != 0 else 0
    }

    beer = {
      "goal"        : beer_goal,
      "record"      : beer_record,
      "percentage"  : beer_record/beer_goal if beer_goal != 0 else 0
    }

    mak = {
      "goal"        : mak_goal,
      "record"      : mak_record,
      "percentage"  : mak_record/mak_goal if mak_goal != 0 else 0
    }

    wine = {
      "goal"        : wine_goal,
      "record"      : wine_record,
      "percentage"  : wine_record/wine_goal if wine_goal != 0 else 0
    }

    # 친구의 달성률
    # user의 친구 리스트 불러오기
    # user의 친구 정보 리스트로 받기

    # for 문
      # user의 친구 정보로 친구의 목표 정보 가져오기
      # 각 친구의 목표 정보 밑 친구의 정보 {}에 저장하기
      # {"username": "유저 이름", "achievement":~~}
    # 반복문 돌면서 친구의 달성률 계산



    data = {
      "cheer"   : cheer,
      "soju"    : soju,
      "beer"    : beer,
      "mak"     : mak,
      "wine"    : wine
      #"friends" : 
    }
    return Response()
  
class CheerView(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request):
    # request에서 입력받은 친구 정보로 해당 목표 모델 가져오기
    friend_id = request.data.get('friend_id')

    friend = get_object_or_404(User, id=friend_id)
    now = datetime.now()
    goal = get_object_or_404(Goal, user=friend, year=now.year, month=now.month)

    # 목표 정보 중 cheer만 +1 하기
    goal.cheer += 1
    goal.save()

    # 응원 성공 메시지 반환
    return Response({"message": "응원을 보냈습니다"}, status=status.HTTP_200_OK)