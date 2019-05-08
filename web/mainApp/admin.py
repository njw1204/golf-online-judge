from django.contrib import admin
from . import models as mainModels

# Register your models here.
# admin.site.register(models.ProblemPost)

@admin.register(mainModels.ProblemPost)
class ProblemPostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "creator", "time_limit", "created_date"]
    list_display_links = ["id", "title"]

@admin.register(mainModels.SolvePost)
class SolvePostAdmin(admin.ModelAdmin):
    list_display = ["id", "user_pk", "problem_pk", "result", "show", "ip", "created_date"]
    list_display_links = ["id"]
