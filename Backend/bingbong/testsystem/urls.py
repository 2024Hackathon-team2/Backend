from django.urls import path, include
from .views import *

app_name = 'test'

urlpatterns = [
  path('', TestStartView.as_view(), name='test-view'),
]