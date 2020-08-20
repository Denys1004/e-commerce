from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from reg_log.forms import CreateUserForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Create your views here.
def register(request):
  form = CreateUserForm()

  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      form.save()
      user = form.cleaned_data.get('username')
      messages.success(request, 'Welcome ' + user + ' You successfuly registered')

  context = {
    'form': form 
  }
  return render(request, 'reg_log/register.html', context)
@login_required
def user_logout(request):
  logout(request)
  return redirect('/')
  
def user_login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
      login(request, user)
      return redirect('/')
    else:
      messages.info(request, 'Username or password is wrong!')

  return render(request, 'reg_log/user_login.html')
