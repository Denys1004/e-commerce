from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from reg_log.forms import CreateUserForm

# Create your views here.
def register(request):
  form = CreateUserForm()

  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      form.save()

  context = {
    'form': form 
  }
  return render(request, 'reg_log/register.html', context)
