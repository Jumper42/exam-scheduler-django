from django.contrib import admin
from .models import Exam
# Register your models here.


class ExamAdmin(admin.ModelAdmin):
    list_display = ("exam_type", "course",
                   "unit", "start_date", "location")
    readonly_fields = ("id",)

admin.site.register(Exam, ExamAdmin)
