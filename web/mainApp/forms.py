from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.utils import timezone
from judge import problem
from .models import SolvePost, ProblemPost
from . import utils

class CustomUserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label="이메일", help_text="비밀번호 찾기용으로 사용합니다.")

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")
        labels = {
            "username": "아이디"
        }

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop("cap-token")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        if commit:
            # user.is_active = False
            user.save()
        return user

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("이미 가입된 아이디입니다.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("이미 등록된 이메일입니다.")
        return email

    def clean(self):
        super().clean()
        if not utils.verify_recaptcha(self.token):
            raise ValidationError("reCAPTCHA 인증 실패")
        return self.cleaned_data


class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "아이디와 비밀번호를 정확하게 입력해주세요.",
        'inactive': "활성화되지 않은 계정입니다.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "아이디"

    def clean_username(self):
        username = self.cleaned_data.get("username")
        real_username = User.objects.filter(username__iexact=username).values("username")
        if real_username.exists():
            return real_username.first()["username"]
        else:
            return username


class SolvePostForm(forms.ModelForm):
    POST_DURATION = 30 # x초 동안 한번 제출 가능

    class Meta:
        model = SolvePost
        fields = ("lang", "body")
        labels = {
            "lang": "언어 선택",
            "body": "코드",
        }
        error_messages = {
            "body" : {
                "required" : "코드가 너무 짧습니다.",
                "max_length" : "코드가 너무 깁니다.",
            }
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.ip = kwargs.pop("ip")
        self.problem = kwargs.pop("problem")
        super().__init__(*args, **kwargs)
        self.fields["body"].strip = False
        self.fields["body"].help_text = "시간 제한 : %d초 / 길이 제한 : %d바이트" % (self.problem.time_limit, self.problem.code_limit)

    def clean_body(self):
        body = self.cleaned_data["body"]
        if type(body) != str or len(body) == 0:
            raise ValidationError("코드가 너무 짧습니다.")
        body = body.replace("\r\n", "\n")
        if len(body) > self.problem.code_limit:
            raise ValidationError("코드가 너무 깁니다.")
        return body

    def clean(self):
        super().clean()
        now_time = timezone.now()
        base_time = now_time - timezone.timedelta(seconds=SolvePostForm.POST_DURATION)
        query = SolvePost.objects.filter(Q(user_pk=self.user) | Q(ip=self.ip), created_date__gt=base_time)
        if query.exists():
            before_time = query.first().created_date
            next_time = before_time + timezone.timedelta(seconds=SolvePostForm.POST_DURATION)
            diff_time = next_time - now_time
            raise ValidationError("%d초 후 제출할 수 있습니다." % diff_time.seconds)
        return self.cleaned_data


class CreateProblemForm(forms.ModelForm):
    MAX_FILE_SIZE = utils.MB(10)
    input_output_help = "실제 채점에 사용하는 %s입니다. (UTF-8, 최대 " + str(utils.to_MB(MAX_FILE_SIZE, True)) + "MB)<br />1개의 파일만 쓸 수 있다는 점을 고려해 제작해주세요.<br />(추천 방법) 하나의 파일이 여러 개의 테스트 케이스를 포함하도록 문제 설계"
    input_file = forms.FileField(max_length=255, allow_empty_file=True, label="Input File", help_text=input_output_help % "입력")
    output_file = forms.FileField(max_length=255, allow_empty_file=True, label="Output File", help_text=input_output_help % "출력")

    class Meta:
        model = ProblemPost
        fields = ("title", "time_limit", "code_limit", "body", "input_explain", "output_explain", "example_in", "example_out")
        labels = {
            "title": "문제 이름",
            "time_limit": "시간 제한",
            "code_limit": "코드 길이 제한",
            "body": "본문",
            "input_explain": "입력 조건 및 설명",
            "output_explain": "출력 조건 및 설명",
            "example_in": "예제 입력",
            "example_out": "예제 출력",
        }
        help_texts = {
            "title": "문제 목록에 노출되는 이름입니다.",
            "time_limit": "정수만 허용됩니다. 최소 1초, 최대 10초까지 가능합니다.",
            "code_limit": "정수만 허용됩니다. 최소 10바이트, 최대 1000바이트까지 가능합니다.",
            "example_in": "문제에 공개되는 예제 입력입니다.",
            "example_out": "문제에 공개되는 예제 출력입니다.",
        }

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop("cap-token")
        super().__init__(*args, **kwargs)

    def clean_input_file(self):
        return self.file_validation(self.cleaned_data["input_file"],
                                    "Input File은 최대 %dMB까지 업로드 가능합니다." % utils.to_MB(CreateProblemForm.MAX_FILE_SIZE, True))

    def clean_output_file(self):
        return self.file_validation(self.cleaned_data["output_file"],
                                    "Output File은 최대 %dMB까지 업로드 가능합니다." % utils.to_MB(CreateProblemForm.MAX_FILE_SIZE, True))

    def file_validation(self, file, error_string):
        if file.size > CreateProblemForm.MAX_FILE_SIZE:
            self.add_error(None, error_string)
        return file

    def clean(self):
        super().clean()
        if not utils.verify_recaptcha(self.token):
            raise ValidationError("reCAPTCHA 인증 실패")
        return self.cleaned_data
