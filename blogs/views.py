from distutils.log import error
from django.shortcuts import render
from .models import ProtectedBlog
from .forms import NewBlogForm
# Create your views here.

def nav(request):

    if request.method == 'POST':
        
        new_blog = ProtectedBlog()
        new_blog.title = request.POST['title']
        new_blog.strapline = request.POST['strapline']

        try:
            new_blog.is_encrypted = bool(request.POST['is_encrypted'])
        except:
            new_blog.is_encrypted = False

        new_blog.blog_content = request.POST['blog_content']
        new_blog.author = request.POST['author']
        new_blog.save()

        return render(request, 'success.html', {'user': 'We did it!'})
    
    new_form = NewBlogForm()
    return render(request, 'nav.html', {'new_form': new_form})