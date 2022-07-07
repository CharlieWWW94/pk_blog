from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
# Create your views here.



def register(request):
    if request.method == "POST":
        reg_form = UserCreationForm(request.POST)
        if reg_form.is_valid():
            reg_form.save()
            return render(request, 'success.html')
    reg_form = UserCreationForm()
    return render(request, 'registration/signup.html', {'reg_form': reg_form})