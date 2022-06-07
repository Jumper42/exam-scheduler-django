def get_exams(courses):
    exams = []
    for course in courses:
        for exam in course.exams.all():
            exams.append(exam)
    return exams