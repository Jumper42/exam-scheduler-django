from django.db import models
from university.models import Course, Unit, Classroom
from datetime import timedelta
# Create your models here.


class Exam(models.Model):
    exam_type = models.CharField(max_length=50,
                                 choices=[('Midterm', 'Midterm',), ('Final', 'Final', ), ('Make-up', 'Make-up',)])
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="exams")
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name="exams")
    start_date = models.DateTimeField()
    duration = models.IntegerField(null=True)
    end_date = models.DateTimeField(blank=True, null=True, editable=False)
    location = models.ForeignKey(
        Classroom, on_delete=models.SET_NULL, null=True, related_name="exams")

    def __str__(self):
        return self.course.course_name

    def save(self, *args, **kwargs):
        self.end_date = self.start_date + timedelta(minutes=self.duration)
        super().save(*args, **kwargs)

    class Meta:
        models.UniqueConstraint(
            fields=['start_date', 'location'], name="Date and Location")
        models.UniqueConstraint(fields=['course', 'exam_type', 'unit'], name="Course, Type, Unit")
