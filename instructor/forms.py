from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Instructor


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=250, help_text="Required. Add a valid email address !")

    class Meta:
        model = Instructor
        fields = ('first_name', 'last_name', 'phone','email', 'password1', 'password2')

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label="Upload Image")