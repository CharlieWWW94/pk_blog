from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as new_login



def register(request):
    if request.method == "POST":
        reg_form = UserCreationForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            return render(request, 'success.html')
    reg_form = UserCreationForm()
    return render(request, 'registration/signup.html', {'reg_form': reg_form})


def login(request):

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