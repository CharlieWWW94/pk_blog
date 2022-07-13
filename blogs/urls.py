from . import views
from django.urls import path
from .forms import NewBlogForm


urlpatterns = [
    path('home/', views.nav)
]