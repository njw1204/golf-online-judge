from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import CustomUserCreateForm
from . import models as mainModels

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


class ProblemListView(TemplateView):
    template_name = "mainApp/problem-list.html"

    def dispatch(self, request, *args, **kwargs):
        problem_per_page = 3 # 한 페이지에 보여줄 문제수

        kwargs["problem_total_count"] = mainModels.ProblemPost.objects.count() # 문제 총 개수
        kwargs["last_page"] = kwargs["problem_total_count"] // problem_per_page + 1 # 마지막 페이지 번호
        if kwargs["problem_total_count"] % problem_per_page == 0:
            kwargs["last_page"] -= 1

        # 현재 페이지가 유효범위 안에 있어야 함
        if not (1 <= kwargs["current_page"] <= kwargs["last_page"]):
            return redirect("mainApp:index")

        kwargs["pages"] = range(1, kwargs["last_page"] + 1)

        show_start_range = (kwargs["current_page"] - 1) * problem_per_page
        show_end_range = show_start_range + problem_per_page
        kwargs["problems"] = mainModels.ProblemPost.objects.order_by("pk")[show_start_range:show_end_range] # 현재 페이지에 보여줄 문제 목록

        return super().dispatch(request, *args, **kwargs)


class ProblemView(TemplateView):
    template_name = "mainApp/problem.html"

    def dispatch(self, request, *args, **kwargs):
        # 현재 문제가 존재해야 됨
        result = mainModels.ProblemPost.objects.filter(pk=kwargs["pk"])
        if not result.exists():
            return redirect("mainApp:index")

        kwargs["problem"] = result[0]
        return super().dispatch(request, *args, **kwargs)
