from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import *
from .serializers import *
from datetime import datetime, date

class RecordsView(APIView):
  def post(self, request):
    if not request.user.is_authenticated:
      return Response({"message": "권한이 없습니다."})

    year  = request.data.get('year')
    month = request.data.get('month')
    day   = request.data.get('day')

    year  = int(year)
    month = int(month)
    day   = int (day)
    
    request_date = date(year, month, day)
    days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    weekday = request_date.weekday()

    user = request.user
    user_id = user.id
    data = request.data.copy()
    data.update({"user": user_id,
                    "dow": days[weekday]})

    serializer = RecordSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecordView(APIView):
  def get(self, request, record_id):
    record = get_object_or_404(Record, pk=record_id)
    serializer = RecordSerializer(record, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def patch(self, request, record_id):
    if not request.user.is_authenticated:
      return Response({"message": "수정 권한이 없습니다."})

    record = get_object_or_404(Record, pk=record_id)
    
    if record.user == request.user:
      serializer = RecordPatchSerializer(record, data=request.data)
      if serializer.is_valid():
        serializer.save()

      record = get_object_or_404(Record, user=request.user, pk=record_id)
      serializer = RecordSerializer(record, many=False)
      return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      return Response({"message": "권한이 없습니다."})
  
  def delete(self, request, record_id):
    if not request.user.is_authenticated:
      return Response({"message": "권한이 없습니다."})

    record = get_object_or_404(Record, pk=record_id)
    if request.user == record.user:
      record.delete()
      return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    else:
      return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)