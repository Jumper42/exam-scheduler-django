from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("User should have email address.")
        if not first_name:
            raise ValueError("Users should have first name")
        if not last_name:
            raise ValueError("Users should have last name")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Instructor(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=90, unique=True)
    first_name = models.CharField(verbose_name="first name", max_length=200)
    last_name = models.CharField(verbose_name="last name", max_length=200)
    department = models.ForeignKey("university.Department", on_delete=models.SET_NULL,
                                   null=True, default="", blank=True, verbose_name="department")
    phone = models.CharField(verbose_name="phone", max_length=20)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name="last login", auto_now=True)
    is_instructor = models.BooleanField(default=False, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(
        upload_to="profile_images", blank=True, null=True, default="/default_images/default_profile.png")

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse("profile", args=[self.id])

    def __str__(self):
        return self.full_name()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


##/user_madia/default_images/default_profile.png