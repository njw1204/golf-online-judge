from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        if commit:
            user.is_active = False
            user.save()
        return user

    def clean(self):
        if User.objects.filter(email=self.cleaned_data.get("email")).exists():
            raise ValidationError("이미 가입된 이메일입니다.")
        return self.cleaned_data