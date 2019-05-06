from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib import messages
from django.db import transaction
from .forms import CustomUserCreateForm
from . import models as mainModels
from . import forms as mainForms
from . import utils
from judge import tasks, problem

# Create your views here.
class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreateForm
    success_url = reverse_lazy("mainApp:index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["cap-token"] = self.request.POST.get("g-recaptcha-response", "")
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        messages.info(self.request, self.object.username + "님, 회원가입을 환영합니다.")
        return redirect(self.get_success_url())


class IndexView(TemplateView):
    template_name = "mainApp/index.html"


class ProblemListView(TemplateView):
    template_name = "mainApp/problem-list.html"

    def dispatch(self, request, *args, **kwargs):
        problem_per_page = 10 # 한 페이지에 보여줄 문제수

        cache = mainModels.ProblemPost.objects.filter(show=True)
        kwargs["problem_total_count"] = cache.count() # 문제 총 개수
        kwargs["last_page"] = kwargs["problem_total_count"] // problem_per_page + 1 # 마지막 페이지 번호
        if kwargs["problem_total_count"] % problem_per_page == 0:
            kwargs["last_page"] -= 1

        # 현재 페이지가 유효범위 안에 있어야 함 or 문제가 하나도 없으면 OK
        if not (1 <= kwargs["current_page"] <= kwargs["last_page"]) \
            and not (kwargs["current_page"] == 1 and kwargs["last_page"] == 0):
            messages.info(request, "문제가 존재하지 않습니다.")
            return redirect("mainApp:index")

        kwargs["pages"] = range(1, kwargs["last_page"] + 1)

        show_start_range = (kwargs["current_page"] - 1) * problem_per_page
        show_end_range = show_start_range + problem_per_page
        kwargs["problems"] = cache.order_by("pk")[show_start_range:show_end_range] # 현재 페이지에 보여줄 문제 목록

        return super().dispatch(request, *args, **kwargs)


class ProblemView(TemplateView):
    template_name = "mainApp/problem.html"

    def dispatch(self, request, *args, **kwargs):
        # 현재 문제가 존재해야 됨
        result = mainModels.ProblemPost.objects.filter(pk=kwargs["pk"])
        if not result.exists():
            messages.info(request, "문제가 존재하지 않습니다.")
            return redirect("mainApp:index")

        kwargs["problem"] = result[0]
        kwargs["full_absolute_url"] = request.build_absolute_uri(result[0].get_absolute_url())
        return super().dispatch(request, *args, **kwargs)


class ProblemSubmitView(CreateView):
    template_name = "mainApp/problem-submit.html"
    form_class = mainForms.SolvePostForm

    def dispatch(self, request, *args, **kwargs):
        try:
            self.kwargs["problem"] = mainModels.ProblemPost.objects.filter(pk=self.kwargs["problem_pk"]).first()
            if not request.user.is_authenticated:
                messages.info(request, "로그인을 해주세요.")
                return redirect(self.kwargs["problem"].get_absolute_url())
        except:
            return redirect("mainApp:problems", current_page=1)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["problem"] = self.kwargs["problem"]
        return context

    def get_success_url(self):
        return self.kwargs["problem"].get_absolute_status_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["ip"] = utils.get_real_ip(self.request)
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_pk = self.request.user
        self.object.problem_pk = self.kwargs["problem"]
        self.object.ip = utils.get_real_ip(self.request)
        self.object.save()
        tasks.activate_judge() # 채점 시스템 가동
        return redirect(self.get_success_url(), pk=self.kwargs["problem_pk"])


class ProblemStatusView(TemplateView):
    template_name = "mainApp/problem-status.html"

    def get(self, request, *args, **kwargs):
        submit_per_page = 10 # 한 페이지에 보여줄 제출수

        single_mode = False
        if "problem_pk" in kwargs:
            # problem_pk에 해당하는 문제가 존재하면 그에 맞는 채점 현황만 로드
            result = mainModels.ProblemPost.objects.filter(pk=kwargs["problem_pk"])
            if result.exists():
                submits = mainModels.SolvePost.objects.filter(problem_pk=result.first(), show=True).order_by("-pk")
                kwargs["heading"] = str(kwargs["problem_pk"]) + "번 문제 채점 현황"
                single_mode = True

        if not single_mode:
            # 그런 문제가 없으면 전체 채점 현황을 로드
            submits = mainModels.SolvePost.objects.filter(show=True).order_by("-pk")
            kwargs["heading"] = "전체 채점 현황"

        kwargs["single_mode"] = single_mode
        kwargs["total_count"] = submits.count() # 제출 총 개수
        kwargs["last_page"] = kwargs["total_count"] // submit_per_page + 1 # 마지막 페이지 번호
        if kwargs["total_count"] % submit_per_page == 0:
            kwargs["last_page"] -= 1

        # 현재 페이지가 유효범위 안에 있어야 함 or 제출 현황이 하나도 없으면 OK
        if not (1 <= kwargs["current_page"] <= kwargs["last_page"]) \
            and not (kwargs["current_page"] == 1 and kwargs["last_page"] == 0):
            return redirect("mainApp:index")

        kwargs["pages"] = range(1, kwargs["last_page"] + 1)
        show_start_range = (kwargs["current_page"] - 1) * submit_per_page
        show_end_range = show_start_range + submit_per_page
        kwargs["submits"] = submits[show_start_range:show_end_range]

        return super().get(request, *args, **kwargs)


class ProblemMakeView(CreateView):
    template_name = "mainApp/problem-make.html"
    form_class = mainForms.CreateProblemForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["cap-token"] = self.request.POST.get("g-recaptcha-response", "")
        return kwargs

    def form_valid(self, form):
        try:
            with transaction.atomic():
                self.object = form.save()
                problem.save_testcase(self.object.pk, form.cleaned_data["input_file"], form.cleaned_data["output_file"])
        except:
            messages.warning(self.request, "파일 업로드에 실패했습니다.")
            return render(self.request, self.template_name, {"form": form})
        messages.info(self.request, "문제가 생성되었습니다.")
        return redirect("mainApp:problem", pk=self.object.pk)
