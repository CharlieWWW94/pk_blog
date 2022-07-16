from distutils.log import error
from django.shortcuts import render
from .models import ProtectedBlog
from .forms import NewBlogForm
from enkrypt import BlogEncryptor, KeyEncryptor
from .models import ProtectedBlog
# Create your views here.

def view_all(request):
    #Displays all blogs, in encrypted state on page
    blogs = ProtectedBlog.objects.all()
    return render(request, 'blogs/all_blogs.html', {'results': blogs})

def view_blog(request, id):
    #Presents user with a specific, encrypted blog post
    blog = ProtectedBlog.objects.filter(id=id)
    print(blog)
    return render(request, 'blogs/blog.html', {'blog': blog})



def create_blog(request):
    '''
    
    Renders page with new blog form. Upon post, saves form content to db.
    If user has requested encryption, the blog content is encrypted.

    '''
    
    if request.method == 'POST':
        #Saves data from form to a new blog object in the database.
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
            #Encrypts the blog with AES, and then encrypts the key with RSA.
            #This means only users with the RSA Private Key can decrypt the content
            
            blog_encryption = BlogEncryptor()
            new_blog.blog_content = blog_encryption.encrypt(content)

            key_encryption = KeyEncryptor()
            access_key = key_encryption.gen_pk_keys()
            encrypted_key = key_encryption.encrypt_key(blog_encryption.get_key())
            new_blog.private_key = encrypted_key
        
        else:
            new_blog.blog_content = content

        new_blog.save()
        return render(request, 'success.html', {'user': 'We did it!'})
    
    new_form = NewBlogForm()
    return render(request, 'blogs/create_blog.html', {'new_form': new_form})