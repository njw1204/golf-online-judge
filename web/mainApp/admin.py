from django.contrib import admin
from . import models as mainModels

# Register your models here.
# admin.site.register(models.ProblemPost)

@admin.register(mainModels.ProblemPost)
class ProblemPostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "body", "time_limit", "created_date"]
    list_display_links = ["id", "title"]