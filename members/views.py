from django.http import HttpResponse
from django.template import loader
from .models import Member
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))
  
def details(request, id):
  mymember = Member.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
  }
  return HttpResponse(template.render(context, request))

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

@login_required(login_url='/login/')
def testing(request):
  template = loader.get_template('template.html')
  mymembers = Member.objects.all().values()
  users = User.objects.all()
  context = {
    'fruits': ['Apple', 'Banana', 'Cherry'], 
     'firstname': 'Linus',  
     'mymembers': users,
  }
  return HttpResponse(template.render(context, request))


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('testing')
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('testing')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})