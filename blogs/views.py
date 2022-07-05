from django.shortcuts import render

# Create your views here.
def nav(request):
    return render(request, 'nav.html')