from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from mainApp.forms import CustomUserCreateForm

# Create your views here.
class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreateForm
    success_url = reverse_lazy("mainApp:index")

class IndexView(TemplateView):
    template_name = "mainApp/index.html"