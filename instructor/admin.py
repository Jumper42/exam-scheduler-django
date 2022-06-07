from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import Instructor


class InstructorAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("first_name", "last_name", "email",
                    "last_login", "is_admin", "is_instructor", "department")
    search_fields = ("email",)
    readonly_fields = ("id", "date_joined", "last_login",)  

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ("first_name", "last_name",)

admin.site.register(Instructor, InstructorAdmin)
