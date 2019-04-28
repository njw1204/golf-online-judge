"""mainApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic.base import RedirectView
from . import views as mainViews

app_name = "mainApp"
urlpatterns = [
    path("", mainViews.IndexView.as_view(), name="index"),
    path("problems/<int:current_page>/", mainViews.ProblemListView.as_view(), name="problems"),
    path("problems/", RedirectView.as_view(url="/problems/1/", permanent=True)),
    path("<int:pk>/", mainViews.ProblemView.as_view(), name="problem"),
]
