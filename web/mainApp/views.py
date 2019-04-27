from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from mainApp.forms import CustomUserCreateForm

# Create your views here.
class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreateForm
    success_url = reverse_lazy("mainApp:index")

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return redirect(self.get_success_url())


class IndexView(TemplateView):
    template_name = "mainApp/index.html"