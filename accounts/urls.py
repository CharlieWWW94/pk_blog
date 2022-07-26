from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name='register'),
    path("logmeout/", views.log_me_out, name='log_me_out'),
    path("login/", views.login, name='login'),
    path("<str:username>/", views.dashboard, name='dashboard'),
    path("logout", views.logout, name='logout')
]