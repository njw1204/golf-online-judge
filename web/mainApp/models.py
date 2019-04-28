from django.db import models
from django.forms import ValidationError

# Create your models here.

def isValidTimeLimit(time_limit_value):
    if type(time_limit_value) is not int or not (1 <= time_limit_value <= ProblemPost.MAX_TIME_LIMIT):
        raise ValidationError("시간 제한이 올바르지 않습니다.")

class ProblemPost(models.Model):
    MAX_TIME_LIMIT = 10
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=100000, blank=True)
    input_explain = models.TextField(max_length=100000, blank=True)
    output_explain = models.TextField(max_length=100000, blank=True)
    example_in = models.TextField(max_length=1000, blank=True)
    example_out = models.TextField(max_length=1000, blank=True)
    time_limit = models.PositiveSmallIntegerField(validators=[isValidTimeLimit])
    created_date = models.DateTimeField(auto_now_add=True)
