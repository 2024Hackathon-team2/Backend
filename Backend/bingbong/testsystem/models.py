from django.db import models
from django.contrib.auth.models import User   #accounts 개발 전 user 모델 사용을 위한 import

class TestQuestion(models.Model):
  question = models.CharField(max_length=255)
  answer = models.IntegerField()

  def __str__(self):
    return str(self.pk)

class TestResult(models.Model):
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE
  )
  date = models.DateField()
  stage = models.IntegerField(default=1)
  q1 = models.ForeignKey(TestQuestion, related_name="q1", null=True, on_delete=models.SET_NULL)
  q2 = models.ForeignKey(TestQuestion, related_name="q2", null=True, on_delete=models.SET_NULL)
  q3 = models.ForeignKey(TestQuestion, related_name="q3", null=True, on_delete=models.SET_NULL)
  q4 = models.ForeignKey(TestQuestion, related_name="q4", null=True, on_delete=models.SET_NULL)
  a1 = models.BooleanField(null=True)
  a2 = models.BooleanField(null=True)
  a3 = models.BooleanField(null=True)
  a4 = models.BooleanField(null=True)
  score = models.IntegerField(null=True)
  level = models.IntegerField(null=True)

