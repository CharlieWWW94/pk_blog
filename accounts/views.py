from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as new_login

from blogs.models import ProtectedBlog



def register(request):
    '''
    Allows users to sign up by creating username and password.
    This should be updated with email verification in future.
    '''
    if request.method == "POST":
        reg_form = UserCreationForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            return render(request, 'success.html')
    
    reg_form = UserCreationForm()
    return render(request, 'registration/signup.html', {'reg_form': reg_form})


def login(request):
    '''
    Manages user logins by consulting with db - all default Django authentication.
    '''
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            new_login(request, user)
            if request.user.is_authenticated:
                return render(request, 'success.html', {'user':username})

    login_form = AuthenticationForm()
    return render(request, 'registration/login.html', {'login_form': login_form})

def dashboard(request, username):
    
    if request.user.is_authenticated:
        user_blogs = ProtectedBlog.objects.filter(author = request.user.id)
        print(user_blogs)
        return render(request, 'dashboard.html', {'user_blogs': user_blogs})
        