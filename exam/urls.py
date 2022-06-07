from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('exams', views.exam_list, name='exam-list-page'),
    path('exam-create', views.exam_create, name="exam-create-page"),
    path('exam/delete/<slug:pk>', login_required(views.ExamDeleteView.as_view()), name="exam-delete")
]