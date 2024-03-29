from distutils.log import error
from json import load
import re
from django.shortcuts import render
from .models import ProtectedBlog, ProtectedBlog2
from .forms import NewBlogForm2, DecryptForm, VerifyForm
from enkrypt import BlogEncryptor, KeyEncryptor, RSASign
from .models import ProtectedBlog
import pickle
from pickle import dumps, loads
# Create your views here.


def home(request):
    # displays homepage and allows for blog lookups upon posting
    if request.method == 'POST':
        # redirect for completed decryption form.
        id = request.POST['blog_id']
        return view_blog(request, id=id)
    else:
        form = DecryptForm
        return render(request, 'blogs/home.html', {'form': form})


def view_all(request):
    # Displays all blogs, in encrypted state on page
    blogs = ProtectedBlog2.objects.all()
    return render(request, 'blogs/all_blogs.html', {'results': reversed(blogs)})


def view_blog(request, id):
    '''
    Functionality to visit a blog's url. Initially presented as encrypted
    but on post request with correct encryption key will display decrypted post.
    '''

    if request.method == 'POST':

        if request.POST.get('user_key'):

            return decrypt_helper(request)

        elif request.POST.get('public_key'):

            return verify_helper(request)

    # Inital page render for blog post
    form = DecryptForm
    blog = ProtectedBlog2.objects.filter(id=id)
    return render(request, 'blogs/blog.html', {'blog': blog[0], 'form': form})


def create_blog(request):
    '''
    Renders page with new blog form. Upon post, saves form content to db.
    If user has requested encryption, the blog content is encrypted, as is the aes key.
    '''

    if request.method == 'POST':
        # Adds data from form to a new blog object for the database.
        new_blog = ProtectedBlog2()
        new_blog.title = request.POST['title']
        new_blog.strapline = request.POST['strapline']
        new_blog.attributed_name = request.POST['author']
        new_blog.author = request.user.username

        content = request.POST['blog_content']
        new_blog.blog_content = content

        if request.POST.get('is_verified'):
            # Creates RSA signature from blog content and saves to db. Creates public key for verification later.
            new_blog.is_signed = True
            rsa_signer = RSASign()
            new_blog.rsa_signature = rsa_signer.sign_post(
                given_post=new_blog.blog_content)
            public_key = rsa_signer.get_pub_key()

        if request.POST.get('is_encrypted'):
            # Encrypts user's blog post and adds encrypted version to ProtectedBlog object
            new_blog.is_encrypted = True
            blog_encryption = BlogEncryptor()
            new_blog.blog_content = blog_encryption.encrypt(content)
            aes_Key = blog_encryption.get_key()

        else:
            new_blog.is_encrypted = False
        # encrypted or unencrypted blog object saves to db:

        new_blog.save()

        return render(request, 'blogs/blog_created.html', {'key': aes_Key, 'url_id': new_blog.id, 'public_key': public_key})

    new_form = NewBlogForm2()
    return render(request, 'blogs/create_blog.html', {'new_form': new_form})


### HELPER FUNCTIONS _ TO BE MOVED TO OWN FILE UPON REFACTORING ###


def decrypt_helper(request):

    '''A helper function that allows for blog post decryption - implemented to avoid excessively large view functions'''

    user_key = request.POST['user_key']
    user_key_processed = eval(user_key)

    # Locate blog post in DB
    blog = ProtectedBlog2.objects.filter(
        id=int(request.POST['blog_id']))[0]

    # Decrypt blog text
    blog_decryption = BlogEncryptor(user_key_processed)
    blog_content = blog_decryption.decrypt(eval(blog.blog_content))
    blog.blog_content = blog_content
    blog.is_encrypted = False

    # return webpage
    form = VerifyForm
    return render(request, 'blogs/blog.html', {'blog': blog, 'form': form, 'verification': 'Not yet verified'})


def verify_helper(request):

    '''A helper function that allows for blog post decryption - implemented to avoid excessively large view functions'''

    # Locate blog post
    blog = ProtectedBlog2.objects.filter(
        id=int(request.POST['blog_id']))[0]

    blog_content = request.POST['content']
    public_key = request.POST['public_key']

    # Verify blog post
    verifier = RSASign(public_key=public_key)

    verification_status = verifier.verify_post(
        signed_message=blog_content, given_signature=blog.rsa_signature)

    blog.is_encrypted = False
    blog.blog_content = blog_content

    # Return webpage
    return render(request, 'blogs/blog.html', {'blog': blog, 'form': None, 'verification': verification_status})
