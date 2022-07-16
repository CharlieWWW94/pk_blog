from . import views
from django.urls import path
from .forms import NewBlogForm


urlpatterns = [
    path('new_blog/', views.create_blog),
    path('all_blogs/', views.view_all),
    path('blog/<str:id>', views.view_blog)
]