from distutils.log import error
from django.shortcuts import render
from .models import ProtectedBlog
from .forms import NewBlogForm
from enkrypt import BlogEncryptor, KeyEncryptor
from .models import ProtectedBlog
# Create your views here.

def home(request):
    #displays homepage
    return render(request, 'blogs/home.html')



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
    If user has requested encryption, the blog content is encrypted, as is the aes key.
    '''

    if request.method == 'POST':
        #Adds data from form to a new blog object for the database.
        new_blog = ProtectedBlog()
        new_blog.title = request.POST['title']
        new_blog.strapline = request.POST['strapline']
        new_blog.attributed_name = request.POST['author']
        new_blog.author = request.user.id

        content = request.POST['blog_content']
        new_blog.blog_content = content

        if request.POST.get('is_encrypted') != None:
            #Encrypts the blog with AES, and then encrypts the key with RSA.
            #This means only users with the RSA Private Key can decrypt the content
            
            new_blog.is_encrypted = True
            blog_encryption = BlogEncryptor()
            new_blog.blog_content = blog_encryption.encrypt(content)
            key_encryption = KeyEncryptor()
            access_key = key_encryption.gen_pk_keys()
            encrypted_key = key_encryption.encrypt_key(blog_encryption.get_key())
            new_blog.private_key = encrypted_key
        
        #encrypted or unencrypted blog object saves to db:
        new_blog.is_encrypted = False
        new_blog.save()
        print(str(access_key))
        print(type(access_key))
        decrypted_key = key_encryption.decrypt_key(encrypted_key, access_key)
        print(f"Here is the decrypted key, as evidence:{decrypted_key}")
        blog_decryptor = BlogEncryptor(decrypted_key)
        print(f"Here is the decrypted blog as evidence: {blog_decryptor.decrypt(new_blog.blog_content)}")
        return render(request, 'blogs/blog_created.html', {'key': access_key, 'url_id': new_blog.id})
    
    new_form = NewBlogForm()
    return render(request, 'blogs/create_blog.html', {'new_form': new_form})