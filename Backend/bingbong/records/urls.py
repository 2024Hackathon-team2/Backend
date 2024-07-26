from django.urls import path, include
from .views import *

app_name = 'records'

urlpatterns = [
  path('', RecordView.as_view(), name='record-view'),
]