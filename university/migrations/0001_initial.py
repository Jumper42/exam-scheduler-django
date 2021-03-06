# Generated by Django 4.0.4 on 2022-06-03 08:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postal_code', models.CharField(max_length=5)),
                ('street', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.CharField(max_length=150, unique=True)),
                ('image', models.ImageField(upload_to='building_images')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=100)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='university.address')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=100)),
                ('building', models.ForeignKey(max_length=150, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='departments', to='university.building')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=50, unique=True)),
                ('course_name', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=100)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='university.department')),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to=settings.AUTH_USER_MODEL)),
                ('unit', models.ManyToManyField(related_name='courses', to='university.unit')),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_code', models.CharField(max_length=30, unique=True)),
                ('capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(30)])),
                ('building', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classes', to='university.building')),
            ],
        ),
    ]
