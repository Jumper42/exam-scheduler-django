from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import UpdateView
from .forms import SignupForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Instructor
from django.contrib import messages
from .instructor_helper import get_exams
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, f'You signed up succesfully {user.first_name}!')
            return redirect("/")
        messages.error(request, "Unvalid informations")
    form = SignupForm()
    return render(request, "instructor/signup.html", {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = AuthenticationForm()
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                email = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(email=email, password=password)
                if user is not None:
                    print(user.is_instructor)
                    login(request, user)
                    messages.success(request, f"Welcome back {user.last_name}")
                    return redirect('/')
                else:
                    messages.error(request, 'User error')
                print(email, password)
            else:
                messages.error(request, "Invalid form")
        return render(request, 'instructor/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/login")


def profile_view(request, id):
    user = request.user
    context = {}
    if user.is_authenticated:
        requested_user = get_object_or_404(Instructor, pk=id)
        if requested_user.is_instructor:
            instructor = requested_user
            context['instructor'] = instructor
            context['courses'] = requested_user.courses.all()
            context['exams'] = get_exams(context['courses'])
            return render(request, 'instructor/profile_detail.html', context)
        else:
            return redirect('/')
    else:
        return redirect('/login')


def profile_list_view(request):
    if request.user.is_authenticated:
        instructors = Instructor.objects.filter(is_instructor=True)
        return render(request, 'instructor/profile_list.html', {'instructors': instructors})


class ProfileUpdateView(UpdateView):
    model = Instructor
    fields = ['email', 'first_name', 'last_name', 'phone', 'profile_image']
    template_name = 'instructor/profile_update.html'



def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = Instructor.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Exam Scheduler',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})