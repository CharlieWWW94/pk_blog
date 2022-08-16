from distutils.log import error
from django.shortcuts import render
from .models import ProtectedBlog
from .forms import NewBlogForm, DecryptForm
from enkrypt import BlogEncryptor, KeyEncryptor
from .models import ProtectedBlog
from pickle import dumps, loads
# Create your views here.


def home(request):
    # displays homepage
    if request.method == 'POST':
        # redirect for completed decryption form.
        print("posty tonight!")
        id = request.POST['blog_id']
        return view_blog(request, id=id)
    else:
        form = DecryptForm
        return render(request, 'blogs/home.html', {'form': form})


def view_all(request):
    # Displays all blogs, in encrypted state on page
    blogs = ProtectedBlog.objects.all()
    print(blogs)
    print(
        f"This is the type of the date: {type(blogs[0].time_created)} and what the object consists of {blogs[0].time_created}")
    return render(request, 'blogs/all_blogs.html', {'results': reversed(blogs)})


def view_blog(request, id):
    '''
    Functionality to visit a blog's url. Initially presented as encrypted
    but on post request with correct encryption key will display decrypted post.
    '''
    # Presents user with a specific, encrypted blog post, decrypts if key offered.
    if request.method == 'POST':
        # loads given key as bytes object
        user_key = request.POST['user_key']
        print(user_key)
        user_key_processed = loads(eval(user_key))
        # Locate blog post in DB
        blog = ProtectedBlog.objects.filter(id=int(request.POST['blog_id']))[0]
        # Decrypt key
        key_decryption = KeyEncryptor()
        decoded_key = key_decryption.decrypt_key(
            eval(blog.private_key), user_key_processed)
        # Decrypt blog text
        blog_decryption = BlogEncryptor(given_key=decoded_key)
        blog_content = blog_decryption.decrypt(eval(blog.blog_content))
        blog.blog_content = blog_content
        print(f"This is the decrypted content: {blog.blog_content}")
        blog.is_encrypted = False
        # return webpage
        form = DecryptForm
        return render(request, 'blogs/blog.html', {'blog': blog, 'form': form})

    # Inital page render for blog post
    form = DecryptForm
    blog = ProtectedBlog.objects.filter(id=id)
    print(f"HERE IS THE BLOG YOU ARE LOOKING FOR: {blog[0].is_encrypted}")
    return render(request, 'blogs/blog.html', {'blog': blog[0], 'form': form})


def create_blog(request):
    '''
    Renders page with new blog form. Upon post, saves form content to db.
    If user has requested encryption, the blog content is encrypted, as is the aes key.
    '''

    if request.method == 'POST':
        # Adds data from form to a new blog object for the database.
        new_blog = ProtectedBlog()
        new_blog.title = request.POST['title']
        new_blog.strapline = request.POST['strapline']
        new_blog.attributed_name = request.POST['author']
        new_blog.author = request.user.id

        content = request.POST['blog_content']
        new_blog.blog_content = content

        if request.POST.get('is_encrypted') != None:
            # Encrypts the blog with AES, and then encrypts the key with RSA.
            # This means only users with the RSA Private Key can decrypt the content

            new_blog.is_encrypted = True
            blog_encryption = BlogEncryptor()
            new_blog.blog_content = blog_encryption.encrypt(content)
            key_encryption = KeyEncryptor()
            access_key = key_encryption.gen_pk_keys()
            # Access key as bytes - needed later for decryption.
            bytes_key = str(dumps(access_key))
            encrypted_key = key_encryption.encrypt_key(
                blog_encryption.get_key())
            new_blog.private_key = encrypted_key

        else:
            new_blog.is_encrypted = False
        # encrypted or unencrypted blog object saves to db:

        new_blog.save()

        return render(request, 'blogs/blog_created.html', {'key': bytes_key, 'url_id': new_blog.id})

    new_form = NewBlogForm()
    return render(request, 'blogs/create_blog.html', {'new_form': new_form})
