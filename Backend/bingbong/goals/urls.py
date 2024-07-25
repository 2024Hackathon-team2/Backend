from django.urls import path, include
from .views import *

app_name = 'goals'

urlpatterns = [
  path('', GoalView.as_view(), name='goal-view'),
]