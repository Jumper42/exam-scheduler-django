from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
# Create your models here.
from django.urls import reverse
from instructor.models import Instructor


class Address(models.Model):
    postal_code = models.CharField(max_length=5)
    street = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.street} {self.postal_code}, {self.city}\n/{self.country}'


class Building(models.Model):
    building = models.CharField(max_length=150, unique=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name="address")
    image = models.ImageField(upload_to="building_images")
    slug = models.SlugField(max_length=100, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.building)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.building

    def get_absolute_url(self):
        return reverse("building-detail", args=[self.slug])


class Classroom(models.Model):
    class_code = models.CharField(max_length=30, unique=True)
    capacity = models.IntegerField(validators=[MinValueValidator(30)])
    building = models.ForeignKey(
        Building, on_delete=models.SET_NULL, null=True, related_name="classes")

    def __str__(self):
        return f'{self.building} - {self.class_code} '


class Department(models.Model):
    department_name = models.CharField(max_length=150, unique=True)
    building = models.ForeignKey(Building,
                                 max_length=150, on_delete=models.SET_NULL, null=True, related_name="departments")
    slug = models.SlugField(max_length=100, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.department_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.department_name

    def get_absolute_url(self):
        return reverse("department-detail", args=[self.slug])



class Unit(models.Model):
    unit = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=100, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.unit)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.unit


class Course(models.Model):
    course_code = models.CharField(max_length=50, unique=True)
    course_name = models.CharField(max_length=150, unique=True)
    unit = models.ManyToManyField(Unit, related_name="courses")
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, related_name="courses")
    instructor = models.ForeignKey(
        Instructor, on_delete=models.SET_NULL, null=True, related_name="courses")
    slug = models.SlugField(max_length=100, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.course_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_name