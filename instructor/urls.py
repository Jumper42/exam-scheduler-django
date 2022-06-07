from django.urls import path
from . import views
urlpatterns = [
    path('sign_up', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name="logout"),
    path('profiles', views.profile_list_view, name="profile_list"),
    path('password_reset', views.password_reset_request, name="password_reset"),
    path('profile/edit/<slug:pk>', views.ProfileUpdateView.as_view(), name="update-profile"),
    path('profile/<int:id>', views.profile_view, name="profile"),
]