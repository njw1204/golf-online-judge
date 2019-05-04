from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import SolvePost

class CustomUserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label="이메일", help_text="비밀번호 찾기용으로 사용합니다.")

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")
        labels = {
            "username": "아이디"
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        if commit:
            # user.is_active = False
            user.save()
        return user

    def clean(self):
        super().clean()
        if User.objects.filter(email=self.cleaned_data.get("email")).exists():
            raise ValidationError({"email": "이미 등록된 이메일입니다."})
        return self.cleaned_data

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "아이디"

class SolvePostForm(forms.ModelForm):
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
        super().__init__(*args, **kwargs)
        self.fields["body"].strip = False

    def clean_body(self):
        body = self.cleaned_data["body"]
        if type(body) != str or len(body.strip()) == 0:
            raise ValidationError("코드가 너무 짧습니다.")
        body = body.replace("\r\n", "\n")
        return body
