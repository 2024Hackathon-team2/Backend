from rest_framework import serializers
from .models import *

class TestResultSerializer(serializers.ModelSerializer):
  class Meta:
    model = TestResult
    fields = '__all__'