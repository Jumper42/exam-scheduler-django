from django.contrib import admin
from .models import Address, Course, Unit, Department, Classroom, Building
# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_code", "course_name", "department", "instructor",)
    list_filter = ("department", "instructor",)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("department_name", "building",)


class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("class_code", "capacity", "building",)
    list_filter = ("building",)


admin.site.register(Course, CourseAdmin)
admin.site.register(Unit)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Building)
admin.site.register(Address)