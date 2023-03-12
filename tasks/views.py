from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TasksForm
from .models import Task
# Create your views here.
def home (request):
    return render(request, 'home.html')

def signup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                     username=request.POST['username'],password=request.POST
                     ['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                 return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'El Ususario ya Existe'   
                })
        return HttpResponse('Password no Coincide')    
    
def tasks(request):
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'tasks.html', {'tasks': tasks})

def create_task(request):
     
     if request.method == 'GET':
        return render(request, 'create_task.html', {
          'form': TasksForm     
        })
     else:
        try:
            form = TasksForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user    
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {  
            'form': TasksForm,
            'error': 'Igrese datos validos'
            })

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    form = TasksForm(instance=task)
    return render(request, 'task_datail.html', {'task':task,'form': form})

def salir(request):
     logout(request)
     return redirect('home')  

def signin(request):
    if request.method == 'GET' :
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'] , password=request.POST
            ['password'])
        if user is None:
            return render(request, 'signin.html', {
                 'form': AuthenticationForm,
                 'error': 'User o Password no es valido'
            })
        else:
            login(request, user)
            return redirect('tasks')    