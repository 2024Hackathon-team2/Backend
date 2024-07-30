from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import *
from .serializers import *
from datetime import datetime, date
import random

# Create your views here.
class TestStartView(APIView):
  def get(self, request):
    if not request.user.is_authenticated:
      return Response({"message": "로그인이 필요합니다."},status=status.HTTP_400_BAD_REQUEST)

    q_list = TestQuestion.objects.all()
    random_q = random.sample(q_list, 4)
    q1 = random_q[0]
    q2 = random_q[2]
    q3 = random_q[3]
    q4 = random_q[3]
    
    user = request.user
    user_id = user.id

    date = datetime.now()

    data = {
      "user": user_id,
      "date": date,
      "q1": q1,
      "q2": q2,
      "q3": q3,
      "q4": q4
    }
    

    serializer = TestResultSerializer(data=date)
    if serializer.is_valid():
      instance = serializer.save()
      pk = instance.pk
      return Response({"pk":pk,"data":serializer.data}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class TestAnswerView(APIView):
  def patch(self, request, pk):
    test_result = get_object_or_404(TestResult, pk=pk)

    if request.user != test_result.user:
      return Response({"message": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
    answer = request.POST.get('answer')

    if test_result.stage == 1:
      if test_result.q1.answer == answer:
        test_result.a1 = True
      else:
        test_result.a1 = False
    elif test_result.stage == 2:
        test_result.a2 = answer
    elif test_result.stage == 3:
        test_result.a3 = answer
    elif test_result.stage == 4:
        test_result.a4 = answer
    else:
      return Response({'error': 'Invalid stage'}, status=status.HTTP_400_BAD_REQUEST)
    
    stage = test_result.stage + 1


    