from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .exam_helper import get_clean_data, get_true_data
from .models import Exam
from university.models import Classroom, Unit
from django.contrib import messages
from django.views.generic import DeleteView
# Create your views here.


def home_page(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        exams = Exam.objects.all().order_by("start_date")[:3]
        context['user'] = user
        context['exams'] = exams
        return render(request, 'exam/home_page.html', context)
    else:
        return redirect('/login')


def exam_create(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        if user.is_instructor:
            context['courses'] = user.courses.all()
            context['classrooms'] = Classroom.objects.all()
            context['exam_types'] = Exam.exam_type.field.choices    
            if request.method == 'POST':
                is_valid = get_true_data(request.POST)
                if is_valid:
                    new_exam = get_clean_data(request.POST)
                    new_exam.save()
                    messages.success(request, 'New exam added succesfuly')
                    return redirect('/exams')
                else:
                    messages.error(request, 'Please fill all fields')
                    return redirect('/exam-create')
            return render(request, 'exam/exam_create.html', context)


def exam_list(request):
    context = {}
    default_exams = Exam.objects.all()
    if request.user.is_authenticated:
        context['exams'] = default_exams.order_by('start_date')
        if request.method == 'POST':
            order_method = request.POST['order_by']
            filter_method = request.POST['filter_by']
            print(filter_method)
            if filter_method:
                selected_unit = Unit.objects.get(id=int(filter_method))
                context['exams'] = default_exams.order_by(order_method).filter(unit=selected_unit)
            else:    
                context['exams'] = default_exams.order_by(order_method)
            return render(request, 'exam/exam_list.html', context)
        return render(request, 'exam/exam_list.html', context)

class ExamDeleteView(DeleteView):
    model = Exam
    success_url = reverse_lazy('exam-list-page')
 