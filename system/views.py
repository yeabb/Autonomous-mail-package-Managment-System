from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'system/index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('system:signin'))
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'system/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('system:index'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            return HttpResponse("Invalid username/password.")
    else:
        return render(request, 'system/signin.html')

@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('system:index'))
