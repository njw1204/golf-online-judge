from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

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
    time_limit = models.PositiveSmallIntegerField(validators=(MinValueValidator(1), MaxValueValidator(10),), default=1)
    code_limit = models.PositiveSmallIntegerField(validators=(MinValueValidator(10), MaxValueValidator(1000),), default=1000)
    creator = models.ForeignKey("auth.User", null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(auto_now_add=True)
    show = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("mainApp:problem", kwargs={"pk": self.pk})

    def get_absolute_status_url(self):
        return reverse("mainApp:problem-status", kwargs={"problem_pk": self.pk, "current_page": 1})

class SolvePost(models.Model):
    LANG_CHOICES = (
        (1, "python3"),
    )
    RESULT_CHOICES = (
        (1, "Pass"),
        (2, "Fail"),
        (3, "Wait")
    )

    user_pk = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    problem_pk = models.ForeignKey("ProblemPost", on_delete=models.CASCADE)
    body = models.TextField(max_length=100000)
    lang = models.PositiveSmallIntegerField(choices=LANG_CHOICES, default=1)
    result = models.PositiveSmallIntegerField(choices=RESULT_CHOICES, default=3)
    show = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
