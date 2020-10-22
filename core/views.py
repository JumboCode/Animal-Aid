from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def pass_reset(request):
    return render(request, 'core/passreset.html')