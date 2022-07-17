from . import views
from django.urls import path
from .forms import NewBlogForm
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('new_blog/', views.create_blog),
    path('all_blogs/', views.view_all),
    path('blog/<str:id>', views.view_blog)
]

urlpatterns += staticfiles_urlpatterns()