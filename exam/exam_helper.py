from datetime import datetime
from wsgiref import validate
from .models import Exam
from university.models import Course, Unit, Classroom


def get_true_data(data_set):
    is_valid = True
    for field in data_set:
        if len(data_set[field]) == 0:
            is_valid = False
    return is_valid


def get_clean_data(data_set):
    exam_type = data_set.get('exam_type', 'default')
    course = data_set.get('course', 'default')
    exam_course = Course.objects.get(course_name=course)
    unit = data_set.get('unit',  'default')
    exam_unit = Unit.objects.get(unit=unit)
    start_date = data_set.get('start_date')
    exam_time = data_set.get('exam_time')
    start_date_time = convert_datetime(start_date, exam_time)
    duration = int(data_set.get('duration'))
    class_code = data_set.get('location')
    exam_location = Classroom.objects.get(class_code=class_code)
    new_exam = Exam(exam_type=exam_type, course=exam_course, unit=exam_unit,
                    start_date=start_date_time, duration=duration, location=exam_location)
    return new_exam


def date_converter(string_date):
    str_date_list = string_date.split('-')
    int_date_list = []
    for x in str_date_list:
        int_date_list.append(int(x))
    return int_date_list


def time_converter(string_time):
    str_time_list = string_time.split(':')
    int_time_list = []
    for x in str_time_list:
        int_time_list.append(int(x))
    return int_time_list


def datetime_merger(date_list, time_list):
    dt = date_list + time_list
    date_time = datetime(year=dt[0], month=dt[1],
                         day=dt[2], hour=dt[3], minute=dt[4])
    return date_time


def convert_datetime(string_date, string_time):
    date_list = date_converter(string_date)
    time_list = time_converter(string_time)
    date_time = datetime_merger(date_list, time_list)
    return date_time