from dataclasses import field
from django.shortcuts import render
from .models import Building, Course, Department
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View


class BuildingListView(ListView):
    model = Building
    context_object_name = 'buildings'
    ordering = ['building']


class BuildingDetailView(DetailView):
    model = Building


class DepartmentListView(View):
    def get(self, request):
        context = {}
        context['departments'] = Department.objects.all()
        return render(request, 'university/department_list.html', context)

    def post(self, request):
        pass


class DepartmentDetailView(DetailView):
    model = Department
    


def course_list(request):
    context = {}
    courses = Course.objects.all()
    context['courses'] = courses.order_by("course_name")
    if request.method == 'POST':
        order_method = request.POST['order_by']
        context['courses'] = courses.order_by(order_method)
    return render(request, 'university/course_list.html', context)