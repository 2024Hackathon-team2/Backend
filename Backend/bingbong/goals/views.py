from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import Goal
from .serializers import *
from records.models import *
from records.serializers import *
from accounts.models import *
from datetime import datetime
from decimal import Decimal
from webpush import send_user_notification
import json
# from permissions import CustomReadOnly # modelviewset으로 바꿀지 고민 중...
# https://newbiecs.tistory.com/316 참고해서 공부하고 코드 변경해보기

class GoalView(APIView):
  def get(self, request):
    now = datetime.now()
    year = now.year
    month = now.month

    year = request.query_params.get('year', now.year)
    month = request.query_params.get('month', now.month)

    try:
      year = int(year)
      month = int(month)
    except ValueError:
      return Response({"message": "연도와 달은 정수여야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

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
      date.append({'day': a.day, 'id': a.id})
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
      "year": year,
      "month": month,
      "before":{
          "year": year-1 if month == 1 else year,
          "month": 12 if month == 1 else month-1
        },
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
  
  # def post(self, request):
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
      date.append({'day': a.day, 'id': a.id})
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
      "year":year,
      "month":month,
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
        date.append({'day': a.day, 'id': a.id})
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
        "year":year,
        "month":month,
        "before":{
          "year": year if month != 1 else year-1,
          "month": 12 if month == 1 else month-1
        },
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
    
    #사용자 id, 응원
    user = request.user
    user_id = user.id
    cheer = goal_data['cheer']
    #사용자 설정 목표
    soju_goal = Decimal(goal_data['soju_goal'])
    beer_goal = Decimal(goal_data['beer_goal'])
    mak_goal  = Decimal(goal_data['mak_goal'])
    wine_goal = Decimal(goal_data['wine_goal'])

    #기록
    records = Record.objects.filter(user=request.user, year=year, month=month)
    soju_record = Decimal(0.0)
    beer_record = Decimal(0.0)
    mak_record  = Decimal(0.0)
    wine_record = Decimal(0.0)

    for record in records:
      record_serializer = RecordSerializer(record)
      record_data = record_serializer.data
      soju_record += Decimal(record_data['soju_record'])
      beer_record += Decimal(record_data['beer_record'])
      mak_record  += Decimal(record_data['mak_record'])
      wine_record += Decimal(record_data['wine_record'])
    
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
    friends_list = []
    user = get_object_or_404(Mypage, user=request.user)
    for friend in user.friends.all():
      # user의 친구 정보로 친구의 목표 정보 가져오기
      user_friend = get_object_or_404(User, pk=friend.pk)
      friend_total_goal = Decimal(0.0)
      goal = get_object_or_404(Goal, year=year, month=month, user=user_friend)
      goal_serializer = GoalSerializer(goal)
      goal_data = goal_serializer.data
      friend_total_goal = Decimal(goal_data['soju_goal']) + Decimal(goal_data['beer_goal']) + Decimal(goal_data['mak_goal']) + Decimal(goal_data['wine_goal'])

      records = Record.objects.filter(user=user_friend, year=year, month=month)
      friend_total_record = Decimal(0.0)
      for record in records:
        record_serializer = RecordSerializer(record)
        record_data = record_serializer.data
        friend_total_record += Decimal(record_data['soju_record']) + Decimal(record_data['beer_record']) + Decimal(record_data['mak_record']) + Decimal(record_data['wine_record'])
      
      percentage = friend_total_record/friend_total_goal if friend_total_goal!=0 else 0
      
      friends_list.append({"friend":user_friend.id, "goal": friend_total_goal, "record": friend_total_record, "percentage": percentage})
      # 각 친구의 목표 정보 밑 친구의 정보 {}에 저장하기
      # {"username": "유저 이름", "achievement":~~}
    # 반복문 돌면서 친구의 달성률 계산



    data = {
      "cheer"   : cheer,
      "soju"    : soju,
      "beer"    : beer,
      "mak"     : mak,
      "wine"    : wine,
      "friends" : friends_list
    }
    return Response(data, status=status.HTTP_200_OK)
  
class CheerView(APIView):
  def post(self, request, friend_id):
    # request에서 입력받은 친구 정보로 해당 목표 모델 가져오기
    user = request.user
    user_page = get_object_or_404(Mypage, user = user)
    friend = get_object_or_404(User, pk=friend_id)
    friend_page = get_object_or_404(Mypage, user=friend)

    if friend_id not in user_page.friends:
      return Response({"message":"내 친구가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

    now = datetime.now()
    year = now.year
    month = now.month

    # 목표 정보 중 cheer만 +1 하기
    goal = get_object_or_404(Goal, user=friend, year=year, month=month)
    goal.cheer += 1
    goal.save()

    # 친구에게 웹 푸시 알림가게 하기
    body_messeage = "{}({})님이 {}님께 음주 목표를 달성하면 좋겠다는 응원을 보냈어요. 건강한 음주 습관을 위해 이번 달도 화이팅!".format(user_page.nickname, user.email, friend_page.nickname)
    payload = {"head": "친구에게 응원을 받았어요!🎉",
              "body": body_messeage,
              "icon": "https://i.imgur.com/dRDxiCQ.png",
              "url": "http://127.0.0.1:8000/goals/" #배포하는 사이트의 url에 맞춰 변경 예정
              }
    payload = json.dumps(payload)

    send_user_notification(user=friend, payload=payload)

    return Response({"message": "응원을 보냈습니다."}, status=status.HTTP_200_OK)
  