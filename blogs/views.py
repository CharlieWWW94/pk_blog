from distutils.log import error
from django.shortcuts import render
from .models import ProtectedBlog
from .forms import NewBlogForm
from enkrypt import BlogEncryptor
# Create your views here.

def nav(request):
    '''
    
    Renders page with new blog form. Upon post, saves form content to db.
    If user has requested encryption, the blog content is encrypted.

    '''
    if request.method == 'POST':
        
        new_blog = ProtectedBlog()
        new_blog.title = request.POST['title']
        new_blog.strapline = request.POST['strapline']
        new_blog.attributed_name = request.POST['author']
        new_blog.author = request.user.id

        try:
            new_blog.is_encrypted = bool(request.POST['is_encrypted'])
        except:
            new_blog.is_encrypted = False
        
        content = request.POST['blog_content']

        if new_blog.is_encrypted:
            
            blog_encryption = BlogEncryptor()
            encryption_keys = blog_encryption.generate_keys()
            encrypted_content = blog_encryption.encrypt(content)
            new_blog.blog_content = encrypted_content
        
        else:
            new_blog.blog_content = content

      
        new_blog.save()

        return render(request, 'success.html', {'user': 'We did it!'})
    
    new_form = NewBlogForm()
    return render(request, 'nav.html', {'new_form': new_form})