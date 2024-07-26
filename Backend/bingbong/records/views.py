from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from .models import *
from .serializers import *
from datetime import datetime

class RecordView(APIView):
  def get(self, request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')

    record = Record.objects.filter(user=request.user, year=year, month=month)
    serializer = RecordSerializer(record, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self, request):
    if not request.user.is_authenticated:
      return Response({"message": "수정 권한이 없습니다."})
    

    record = get_object_or_404(Record, data=request.data)
    serializer = RecordSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save(user=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def patch(self, request):
    if not request.user.is_authenticated:
      return Response({"message": "수정 권한이 없습니다."})
    
    record = get_object_or_404(Record)
    
    if record.user == request.user:
      serializer = RecordPatchSerializer(record, data=request.data)
      if serializer.is_valid():
        serializer.save()
      year = request.GET.get('year')
      month = request.GET.get('month')
      day = request.GET.get('day')
      record = Record.objects.filter(user=request.user, year=year, month=month)
      serializer = RecordSerializer(record, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      return Response({"message": "수정 권한이 없습니다."})